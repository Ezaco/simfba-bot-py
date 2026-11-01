import re
import discord
import asyncio
from concurrent.futures import ThreadPoolExecutor
from api_requests import GetLaxWeekGames, GetLaxGame, GetLaxLogoUrl
from helper import embed_builder, message_sender, util
import logos_util

SECONDS_PER_ACTION = {
    "goal": 10,
    "shot": 4,
    "penalty": 8,
    "injury": 8,
    "period": 5,
    "faceoff": 3,
    "turnover": 3,
    "timeout": 4,
}
DEFAULT_SECONDS = 2
INTRO_SECONDS = 8
TAG_SECONDS = 3
AD_SECONDS = 5
OUTRO_SECONDS = 15
SEND_SECONDS_PER_MESSAGE = 0.3          # rough time Discord takes to accept a message, on top of the pauses

# The broadcast networks, in the order the week's games are dealt out to them: (key, name shown in the stream).
NETWORKS = [
    ("flo", "FloSports"),
    ("laxtv", "Lacrosse TV"),
    ("abc", "ABC"),
    ("espnu", "ESPNU"),
]
NETWORK_NAMES = dict(NETWORKS)

# Networks that are streaming right now. Each network can only run once at a time, but different ones run together.
streaming_now = set()

# The messages the stream posts are also how it finds its place again after a restart (see read_progress), so the
# texts it reads back live here, in one place, next to the ones it writes.
FINAL_TITLE = "... and that's the game, folks! Thank you for watching!"
CLOSING_TEXT = "That's all the games for the week, thank you for watching!"
INTRO_FOOTER = re.compile(r"Week (\d+) \| Game (\d+) of (\d+) \| ID (\d+)")
PLAY_TITLE = re.compile(r"^Play (\d+):")
RESUME_HISTORY_LIMIT = 1500             # a game is about 700 messages, so this reaches back past the start of the current one

def play_delay(play):
    if play["isGoal"]:
        return SECONDS_PER_ACTION["goal"]
    if play["isInjury"]:
        return SECONDS_PER_ACTION["injury"]
    # The engine files notes like "BU receives the boundary restart" as shots with no outcome. They are not
    # shots (a real one always has a goal, save, miss, block or pipe), so they get a normal pause.
    if play["actionType"] == "shot" and play["outcomeType"] is None:
        return DEFAULT_SECONDS
    return SECONDS_PER_ACTION.get(play["actionType"], DEFAULT_SECONDS)

def ad_follows(play):
    # Goals and timeouts are the natural breaks in a game, so they are where the ads run.
    return play["isGoal"] or play["actionType"] == "timeout"

def team_label(team):
    return f"{team['name']} {team['nickname']}".strip()

def games_for_network(game_ids, network_key):
    """The share of the week's games a network streams: every fourth game by id, dealt out in NETWORKS order.

    The rule needs nothing but the ids, so each network works out its own share without talking to the others,
    and the four shares always cover the week exactly once however the commands are started.
    """
    keys = [key for key, _ in NETWORKS]
    return sorted(game_ids)[keys.index(network_key)::len(keys)]

def estimate_game_seconds(game, plays):
    """How long a game takes to stream: the pauses plus a rough allowance for Discord's send time."""
    stream_plays = embed_builder.Get_LAX_Stream_Plays(plays)
    seconds = INTRO_SECONDS + OUTRO_SECONDS
    if game.get("homeDiscordMention") or game.get("awayDiscordMention"):
        seconds += TAG_SECONDS
    ads = 0
    for play in stream_plays:
        seconds += play_delay(play)
        if ad_follows(play):
            seconds += AD_SECONDS
            ads += 1
    messages = len(stream_plays) + ads + 2
    return seconds + messages * SEND_SECONDS_PER_MESSAGE

def format_duration(seconds):
    minutes = int(round(seconds / 60))
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes:02d}m" if hours else f"{minutes}m"

def fetch_games(game_ids):
    def fetch(game_id):
        try:
            return GetLaxGame(game_id)
        except Exception as e:
            print(f"Could not load SimLAX game {game_id}: {e}")
            return False
    with ThreadPoolExecutor(max_workers=8) as pool:
        return dict(zip(game_ids, pool.map(fetch, game_ids)))

async def read_progress(chan, bot_id):
    """Where this channel's last stream got to, read from the bot's own messages, newest first.

    Walks back to the most recent game intro (its footer names the week and game) and notes on the way whether the
    game's final score or the closing line came after it, and the last play that was posted. Returns None when no
    intro is in reach, which the caller treats as 'start from the top'.
    """
    closing = False
    game_finished = False
    last_play = None
    ad_posted = False                     # whether an ad came after the last play, which matters when that play was a goal or timeout
    async for message in chan.history(limit=RESUME_HISTORY_LIMIT):
        if message.author.id != bot_id:
            continue
        if message.content and message.content.startswith(CLOSING_TEXT):
            closing = True
            continue
        for embed in message.embeds:
            title = embed.title or ""
            footer = embed.footer.text if embed.footer and embed.footer.text else ""
            intro = INTRO_FOOTER.search(footer) if title.startswith("Streaming") else None
            if intro:
                return {"week": int(intro.group(1)), "game_id": int(intro.group(4)), "closing": closing,
                        "game_finished": game_finished, "last_play": last_play, "ad_posted": ad_posted}
            if title.startswith(FINAL_TITLE):
                game_finished = True
            elif last_play is None:
                play = PLAY_TITLE.match(title)
                if play:
                    last_play = int(play.group(1))
                elif title.startswith("AD"):
                    ad_posted = True
    return None

def resume_decision(progress, week, game_ids):
    """What to do given where the channel's last stream stopped. Returns (action, position, last_play).

    fresh: nothing usable, so start from the top | done: that week already finished here |
    finish: every game was played but the closing line was not | next: carry on with the game after position |
    midgame: carry on inside the game at position, after play last_play.
    """
    if progress is None or progress["week"] != week or progress["game_id"] not in game_ids:
        return "fresh", 0, None
    position = game_ids.index(progress["game_id"])
    if progress["closing"]:
        return "done", position, None
    if progress["game_finished"]:
        return ("next", position + 1, None) if position + 1 < len(game_ids) else ("finish", position, None)
    return "midgame", position, progress["last_play"]

async def stream_lax_network(network_key, chan, season=None, week=None, report=None, resume=True, bot_id=None):
    """One network's share of the week, played back to back in its own channel.

    report, if given, is an async function that gets the plan and any problem (the command's reply).
    With resume on (and the bot's id known) a rerun picks up where the channel's last stream stopped.
    """
    name = NETWORK_NAMES[network_key]

    async def say(text):
        if report:
            await report(text)
        else:
            await message_sender.SendMessage(chan, text)

    if network_key in streaming_now:
        await say(f"{name} is already streaming.")
        return
    streaming_now.add(network_key)
    try:
        week_data = GetLaxWeekGames(season, week)
        if not week_data:
            await say("Couldn't load SimLAX games. Please check the API and try again.")
            return
        week_ids = [game["id"] for game in week_data["games"]]
        if not week_ids:
            await say(f"No simulated SimLAX games are ready to stream for week {week_data['week']}.")
            return
        mine = games_for_network(week_ids, network_key)
        if not mine:
            await say(f"{name} has no games this week (only {len(week_ids)} to share between {len(NETWORKS)} networks).")
            return

        details = await asyncio.to_thread(fetch_games, mine)
        loaded = [game_id for game_id in mine if details.get(game_id)]
        if not loaded:
            await say(f"Couldn't load any of {name}'s games. Please check the API and try again.")
            return
        skipped = len(mine) - len(loaded)

        # Work out whether this is a rerun that should carry on from where the channel stopped. If anything about
        # reading the channel fails or does not add up, the stream simply starts from the top.
        action, position, last_play, progress = "fresh", 0, None, None
        if resume and bot_id is not None:
            try:
                progress = await read_progress(chan, bot_id)
                action, position, last_play = resume_decision(progress, week_data["week"], loaded)
            except Exception as e:
                print(f"Could not read {name}'s channel history, starting from the top: {e}")
        if action == "done":
            await say(f"{name} already finished week {week_data['week']} in this channel. Use restart to stream it again.")
            return
        if action == "finish":
            await message_sender.SendMessage(chan, CLOSING_TEXT)
            await say(f"{name} had played every game; I posted the closing line.")
            return

        # The plan (how many games, how long) goes to the bot's console, not to Discord; the command's reply stays
        # the plain "Loading ... games for the week...". Only a problem is worth telling the channel about.
        remaining = loaded[position:]
        total = sum(estimate_game_seconds(details[game_id]["game"], details[game_id]["plays"]) for game_id in remaining)
        print(f"{name}: {'resuming' if action != 'fresh' else 'streaming'} {len(remaining)} of {len(week_ids)} games this week, about {format_duration(total)}")
        if skipped:
            await say(f"{skipped} of {name}'s games could not be loaded.")

        injury_url = logos_util.GetIcon("Injury")
        penalty_url = logos_util.GetIcon("Penalty")
        if action == "fresh":
            matchups = [f"{team_label(details[game_id]['game']['homeTeam'])} vs {team_label(details[game_id]['game']['awayTeam'])}" for game_id in loaded]
            slate = f"**{name}** - Week {week_data['week']} slate:\n" + "\n".join(f"- {matchup}" for matchup in matchups)
            await message_sender.SendMessage(chan, slate[:1900])
        else:
            await message_sender.SendMessage(chan, f"**{name}** is back on the air - picking up at game {position + 1} of {len(loaded)}.")
        await asyncio.sleep(5)
        for index, game_id in enumerate(loaded):
            if index < position:
                continue
            resuming_this_game = action == "midgame" and index == position
            try:
                await stream_lax_game(
                    chan, game_id, injury_url, penalty_url, name, details.pop(game_id),
                    footer=f"Week {week_data['week']} | Game {index + 1} of {len(loaded)} | ID {game_id}",
                    resumed=resuming_this_game, skip_through=last_play if resuming_this_game else None,
                    last_play_ad_posted=bool(progress and progress["ad_posted"]) if resuming_this_game else True,
                )
            except Exception as e:
                print(f"SimLAX stream failed for game {game_id}: {e}")
        await message_sender.SendMessage(chan, CLOSING_TEXT)
    finally:
        streaming_now.discard(network_key)

async def stream_lax_week_all(channels, season=None, week=None, report=None, resume=True, bot_id=None):
    """Start every network at once. channels maps each network key to its Discord channel."""
    results = await asyncio.gather(
        *(stream_lax_network(key, channels[key], season, week, report, resume, bot_id) for key, _ in NETWORKS),
        return_exceptions=True,
    )
    for (key, _), result in zip(NETWORKS, results):
        if isinstance(result, Exception):
            print(f"SimLAX stream failed on {NETWORK_NAMES[key]}: {result!r}")

async def post_ad(chan):
    ad = util.PickAd()
    ad_embed = discord.Embed(colour=discord.Colour.light_gray(), title=util.AdTitleText(ad), description=util.AdDescriptionText(ad))
    ad_embed.set_thumbnail(url=logos_util.GetAd(ad))
    await message_sender.SendEmbedMessage(chan, embed=ad_embed)
    await asyncio.sleep(AD_SECONDS)

async def stream_lax_game(chan, game_id, injury_url, penalty_url, network=None, data=None, footer=None, resumed=False, skip_through=None, last_play_ad_posted=True):
    """Stream one game. footer marks the intro so a restart can find its place; resumed means the intro is already
    posted and plays up to skip_through already went out, so carry on after them (posting the ad the last of them
    was owed, if the restart came before it)."""
    data = data or GetLaxGame(game_id)
    if not data:
        print(f"Could not load SimLAX game {game_id}")
        return
    game = data["game"]
    plays = data["plays"]
    home = game["homeTeam"]
    away = game["awayTeam"]
    home_label = team_label(home)
    away_label = team_label(away)
    home_url = GetLaxLogoUrl(home["logoFileName"])
    away_url = GetLaxLogoUrl(away["logoFileName"])
    home_tag = game.get("homeDiscordMention")
    away_tag = game.get("awayDiscordMention")
    home_coach = home_tag or (home["coach"] or "AI").strip()
    away_coach = away_tag or (away["coach"] or "AI").strip()
    contending_teams_str = f"Home Team: {home_label} | Coach: {home_coach}"
    contending_teams_str += f"\nAway Team: {away_label} | Coach: {away_coach}"

    stream_plays = embed_builder.Get_LAX_Stream_Plays(plays)
    # Where the restart left off, as a position in this game's plays. If the play it names is not in the game any
    # more (the game was re-simulated), the old position means nothing, so the game starts again from its intro.
    skip_index = None
    if resumed and skip_through is not None:
        skip_index = next((index for index, play in enumerate(stream_plays) if play["playNumber"] == skip_through), None)
        if skip_index is None:
            resumed = False

    if not resumed:
        title = f"Streaming {home_label} Match Live on {network}!" if network else f"Streaming {home_label} Match!"
        init_embed = discord.Embed(colour=discord.Colour.blue(), description=contending_teams_str, title=title)
        if game["gameName"]:
            init_embed.add_field(name="Match Name", value=game["gameName"], inline=False)
        if home["venue"] and not game["isNeutral"]:
            init_embed.add_field(name="Venue", value=home["venue"], inline=False)
        init_embed.set_thumbnail(url=home_url)
        if footer:
            init_embed.set_footer(text=footer)
        if home_tag or away_tag:
            await message_sender.SendMessage(chan, contending_teams_str)
            await asyncio.sleep(TAG_SECONDS)
        await message_sender.SendEmbedMessage(chan, init_embed)
        await asyncio.sleep(INTRO_SECONDS)

    home_score = 0
    away_score = 0
    for index, play in enumerate(stream_plays):
        home_score = play["homeTeamScore"]
        away_score = play["awayTeamScore"]
        if skip_index is not None and index <= skip_index:
            # Already posted before the restart; the score above still carries on from it.
            if index == skip_index and ad_follows(play) and not last_play_ad_posted:
                await post_ad(chan)
            continue
        play_embed = embed_builder.Get_LAX_Play_Embed(play, home, away, home_url, away_url, injury_url, penalty_url)
        await message_sender.SendEmbedMessage(chan, play_embed)
        await asyncio.sleep(play_delay(play))
        if ad_follows(play):
            await post_ad(chan)

    final_url = home_url if home_score > away_score else away_url
    final_embed = discord.Embed(colour=discord.Colour.blue(), description=contending_teams_str, title=FINAL_TITLE)
    final_embed.add_field(name="Final Score", value=f"{home_label}: {home_score} | {away_label}: {away_score}", inline=False)
    final_embed.add_field(name="Results", value="Check the Interface for the box score & a post-game discussion once results are published!", inline=False)
    final_embed.set_thumbnail(url=final_url)
    await message_sender.SendEmbedMessage(chan, final_embed)
    await asyncio.sleep(OUTRO_SECONDS)
