import re
import discord
from helper import player_builder
from helper.footer import _FOOTER
### FOR STREAMING

def Get_CBB_Play_Embed(play, home_abbr, away_abbr, home_url, away_url, home_score, away_score, injury_url):
    type_of_play = play["TypeOfPlay"]
    time_remaining = play["TimeRemaining"]
    possession = play["Possession"]
    result = play["Result"]
    desc = f"Current Score: {home_abbr} {home_score} - {away_abbr} {away_score}"
    embed_url = ""
    if possession == home_abbr:
        embed_url = home_url
    else:
        embed_url = away_url
    if type_of_play == "Injury":
        embed_url = injury_url
    embed = discord.Embed(colour=discord.Colour.orange(),description=desc,title="Play")
    embed.add_field(name="Type of Play", value=f"{type_of_play}", inline=False)
    embed.add_field(name=f"Possessions Remaining: {time_remaining}", value=f"Possession: {possession}", inline=False)
    embed.add_field(name="Result", value=f"{result}", inline=False)    
    embed.set_thumbnail(url=embed_url)
    return embed

def Get_FBA_Play_Embed(play, home_abbr, away_abbr, home_url, away_url, home_score, away_score, result):
    play_num = play["PlayNumber"]
    home_score = play["HomeTeamScore"]
    away_score = play["AwayTeamScore"]
    quarter = play["Quarter"]
    time_remaining = play["TimeRemaining"]
    distance = play["Distance"]
    line_of_scrimmage = play["LineOfScrimmage"]
    play_type = play["PlayType"]
    play_name = play["PlayName"]
    off_formation = play["OffensiveFormation"]
    def_formation = play["DefensiveFormation"]
    point_of_attack = play["PointOfAttack"]
    def_tendency = play["DefensiveTendency"]
    blitz_number = play["BlitzNumber"]
    lb_cov = play["LBCoverage"]
    db_cov = play["CBCoverage"]
    s_cov = play["SCoverage"]
    res_yards = play["ResultYards"]
    time_remaining = play["TimeRemaining"]
    possession = play["Possession"]
    distance = play["Distance"]
    down_input = play["Down"]
    down = get_down(down_input)
    if play_type == "Kick Off":
        down = ""
    line_of_scrimmage = play["LineOfScrimmage"]
    desc = f"Current Score: {home_abbr} {home_score} - {away_abbr} {away_score}"
    embed_url = ""
    if possession == home_abbr:
        embed_url = home_url
    else:
        embed_url = away_url
    embed = discord.Embed(colour=discord.Colour.dark_gold(),description=desc,title=f"Play {play_num}")
    embed.add_field(name=f"Possessions Remaining: {time_remaining}, {quarter}Q", value=f"Possession: {possession}", inline=False)
    embed.add_field(name=f"{down} and {distance}", value=f"Line of Scrimmage: {line_of_scrimmage}", inline=False)
    embed.add_field(name="Play Type", value=f"{play_type}", inline=False)
    embed.add_field(name="Play Name", value=f"{play_name}", inline=True)
    embed.add_field(name="Point of Attack", value=f"{point_of_attack}", inline=True)
    embed.add_field(name="Defensive Tendency", value=f"{def_tendency}", inline=True)
    embed.add_field(name="Offensive Formation", value=f"{off_formation}", inline=True)
    embed.add_field(name="Defensive Formation", value=f"{def_formation}", inline=True)
    embed.add_field(name="Blitz Number", value=f"{blitz_number}", inline=False)
    embed.add_field(name="LB Coverage", value=f"{lb_cov}", inline=True)
    embed.add_field(name="CB Coverage", value=f"{db_cov}", inline=True)
    embed.add_field(name="S Coverage", value=f"{s_cov}", inline=True)
    embed.add_field(name="Resulting Yards", value=f"{res_yards}", inline=False)
    embed.add_field(name="Result", value=f"{result}", inline=False)    
    embed.set_thumbnail(url=embed_url)
    return embed

def get_down(down):
    if down == "1" or down == 1:
        return "1st Down"
    elif down == "2"or down == 2:
        return "2nd Down"
    elif down == "3"or down == 3:
        return "3rd Down"
    elif down == "4"or down == 4:
        return "4th Down"
    return "IT'S 5TH DOWN EVERYBODY!"

def Get_Hockey_Play_Embed(play, home_abbr, away_abbr, home_url, away_url, home_score, away_score, injury_url, penalty_url):
    period = play["Period"]
    zone = play["Zone"]
    event = play["Event"]
    penalty = play["Penalty"]
    severity = play["Severity"]
    time_remaining = play["TimeOnClock"]
    time_consumed = play["SecondsConsumed"]
    team_id = play["TeamID"]
    possession = home_abbr
    if team_id == play["AwayTeamID"]:
        possession = away_abbr
    result = play["Result"]
    desc = f"Current Score: {home_abbr} {home_score} - {away_abbr} {away_score}"
    embed_url = ""
    if possession == home_abbr:
        embed_url = home_url
    else:
        embed_url = away_url
    if event == "Penalty Check":
        embed_url = penalty_url
    if event == "Injury":
        embed_url = injury_url
    embed = discord.Embed(colour=discord.Colour.light_gray(),description=desc,title="Play")
    embed.add_field(name=f"Period: {period}", value=f"Time: {time_remaining}", inline=True)
    embed.add_field(name=f"Time Passed", value=f"{time_consumed}", inline=True)
    embed.add_field(name="Zone", value=f"{zone}", inline=True)
    embed.add_field(name="Event", value=f"{event}", inline=False)

    if event == "Penalty Check":
        embed.add_field(name="Case", value=f"{penalty}", inline=True)
        embed.add_field(name="Severity", value=f"{severity}", inline=True)
    embed.add_field(name="Result", value=f"{result}", inline=False)    
    embed.set_thumbnail(url=embed_url)
    return embed


def _lax_clock(seconds):
    seconds = max(int(seconds), 0)
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def _lax_period_label(period):
    if period <= 4:
        return f"Q{period}"
    if period == 5:
        return "OT"
    return f"{period - 4}OT"


def _lax_play_label(play):
    action = str(play["actionType"]).replace("_", " ").title()
    outcome = play["outcomeType"]
    if play["actionType"] == "shot" and outcome:
        return f"{action}: {str(outcome).replace('_', ' ').title()}"
    return action


def _lax_team_colour(team, default):
    primary = ((team or {}).get("colors") or {}).get("primary")
    try:
        return discord.Colour.from_str(primary)
    except (TypeError, ValueError):
        return default


def _lax_game_label(game):
    labels = []
    if game["gameContext"] == "preseason":
        labels.append("Preseason")
    if game["isNt"]:
        labels.append("National Tournament")
    elif game["isCt"]:
        labels.append("Conference Tournament")
    elif game["isConferenceGame"]:
        labels.append("Conference Matchup")
    if game["isNeutral"]:
        labels.append("Neutral Site")
    if game["gameName"]:
        labels.insert(0, game["gameName"])
    return " | ".join(labels) or "Non-Conference Matchup"


def Get_LAX_Team_Embed(profile, logo_url, player_years=None):
    # player_years maps a player id to their class year (1 = Fr ... 5 = 5th); players missing from it show no year.
    player_years = player_years or {}
    preview = profile["preview"]
    team = preview["team"]
    conference = (team["conference"] or {}).get("name")
    location = ", ".join(part for part in (team["city"], team["state"]) if part)
    desc = f"University based in {location}."
    if conference:
        desc += f" Members of the {conference}."
    try:
        colour = discord.Colour.from_str(team["colors"]["primary"])
    except (TypeError, ValueError):
        colour = discord.Colour.blue()
    embed = discord.Embed(colour=colour, description=desc, title=f"{team['name']} {team['nickname']}".strip())
    embed.add_field(name="Coach", value=(team["coach"] or "").strip() or "AI", inline=False)
    if team["venue"]:
        embed.add_field(name="Venue", value=team["venue"], inline=False)
    grades = [(label, preview[key]) for label, key in (("Overall", "overallGrade"), ("Offense", "offenseGrade"), ("Defense", "defenseGrade")) if preview[key]]
    if grades:
        embed.add_field(name="Team Grades", value=" | ".join(f"{label}: {grade}" for label, grade in grades), inline=False)
    standing = profile.get("standing")
    record = f"{preview['currentWins']}-{preview['currentLosses']}"
    if standing:
        record += f" ({standing['conferenceWins']}-{standing['conferenceLosses']})"
    embed.add_field(name="Current Record", value=record, inline=True)
    embed.add_field(name="All-Time Record", value=f"{preview['overallWins']}-{preview['overallLosses']}", inline=True)
    # Before a team has played, every conference is tied at 0-0 and ranked alphabetically, so a rank would mean nothing.
    if standing and standing["totalWins"] + standing["totalLosses"] > 0:
        embed.add_field(name="Conference Standing", value=f"#{standing['rank']} of {standing['conferenceTeamCount']} in the {standing['conferenceName']}", inline=False)
    for label, years in (("Conference Titles", preview["conferenceChampionshipYears"]), ("National Titles", preview["nationalChampionshipYears"])):
        if years:
            embed.add_field(name=label, value=f"{len(years)} ({', '.join(str(year) for year in years[-5:])})", inline=True)
    if preview["topPlayers"]:
        players = "\n".join(
            f"{player['position']} {player['firstName']} {player['lastName']}{_lax_year_label(player_years.get(player['id']))} - {player['overallGrade']}"
            for player in preview["topPlayers"]
        )
        embed.add_field(name="Top Players", value=players, inline=False)
    for title, games in (("Recent Results", profile["recentGames"]), ("Upcoming Games", profile["upcomingGames"])):
        if not games:
            continue
        embed.add_field(name="​", value=f"**{title}**", inline=False)
        for game in games:
            home, away = game["homeTeam"], game["awayTeam"]
            name = f"Week {game['week']}: {away['name']} at {home['name']}"
            value = _lax_game_label(game)
            if game["status"] == "Final":
                is_home = home["id"] == team["id"]
                team_score, opp_score = (game["homeScore"], game["awayScore"]) if is_home else (game["awayScore"], game["homeScore"])
                result = "W" if team_score > opp_score else "L" if team_score < opp_score else "T"
                value = f"{result} {home['name']} {game['homeScore']} - {away['name']} {game['awayScore']} | {value}"
            embed.add_field(name=name[:256], value=value[:1024], inline=False)
    embed.set_thumbnail(url=logo_url)
    return embed


_LAX_YEARS = {1: "Fr", 2: "So", 3: "Jr", 4: "Sr", 5: "5th"}


def _lax_year_label(year):
    return f" ({_LAX_YEARS.get(year, year)})" if year else ""


def _lax_stream_team_colour(team, default):
    # For the slim team info the croot and class responses carry ("primaryColor"). Play embeds use
    # _lax_team_colour above, which reads the full team's colors; keep the two names distinct.
    primary = (team or {}).get("primaryColor")
    try:
        return discord.Colour.from_str(primary)
    except (TypeError, ValueError):
        return default


def Get_LAX_Rankings_Embed(data, logo_url):
    embed = discord.Embed(colour=discord.Colour.dark_gold(), title="SimCLAX Recruiting Class Rankings")
    if data["totalSignees"] == 0:
        # Until someone signs, every class scores 0 and the order is just alphabetical, so there is nothing to rank.
        embed.description = "No team has signed a recruit yet, so there are no class rankings to show."
        return embed
    lines = [
        f"**{entry['rank']}. {entry['team']['name']}** ({entry['conference']}) - {entry['score']:.1f} | "
        f"{entry['signees']} signees | {entry['fiveStars']}/{entry['fourStars']}/{entry['threeStars']}"
        for entry in data["rankings"]
    ]
    embed.description = f"Top {len(lines)} of {data['teamCount']} classes\n*Score | signees | 5/4/3-star signees*\n\n" + "\n".join(lines)
    embed.set_thumbnail(url=logo_url)
    embed.set_footer(text="Simulation Sports Network")
    return embed


def Get_LAX_Flex_Embed(data, logo_url):
    one, two = data["teamOne"], data["teamTwo"]
    name_one, name_two = one["team"]["name"], two["team"]["name"]
    if data["gamesPlayed"] == 0:
        embed = discord.Embed(colour=discord.Colour.dark_gold(), description="",
                              title=f"{name_one} and {name_two} have never played against each other")
        embed.set_thumbnail(url=logo_url)
        return embed
    winner = data["latestWinner"]
    desc = f"Current Streak: {winner['name']} with {data['currentStreak']} {'win' if data['currentStreak'] == 1 else 'wins'}" if winner else "The most recent game was a tie"
    embed = discord.Embed(colour=discord.Colour.dark_gold(), description=desc,
                          title=f"Comparison Between {name_one} and {name_two}")
    for side in (one, two):
        name = side["team"]["name"]
        embed.add_field(name=f"{name} Wins", value=side["wins"], inline=True)
        embed.add_field(name=f"{name} Losses", value=side["losses"], inline=True)
        embed.add_field(name=f"{name} Best Streak", value=side["bestStreak"], inline=True)
        if side["largestMargin"] > 0:
            embed.add_field(name=f"{name} Largest Margin of Victory", value=f"{side['largestMargin']}, {side['largestMarginSeason']}", inline=False)
    embed.set_thumbnail(url=logo_url)
    return embed


def _lax_recruit_description(recruit):
    origin = ", ".join(part for part in (recruit["state"], recruit["country"]) if part)
    return f"{recruit['stars']} Star {recruit['archetype']} {recruit['position']} from {origin}"


def Get_LAX_Croot_Embed(recruit, logo_url):
    committed = recruit["committedTeam"]
    embed = discord.Embed(colour=_lax_stream_team_colour(committed, discord.Colour.dark_gold()),
                          description=_lax_recruit_description(recruit),
                          title=f"{recruit['firstName']} {recruit['lastName']} {recruit['id']}")
    embed.add_field(name="Overall", value=recruit["overall"], inline=True)
    embed.add_field(name="Potential", value=recruit["potential"], inline=True)
    embed.add_field(name="Recruiting Status", value=recruit["recruitingStatus"], inline=True)
    embed.add_field(name="Signing Expectation", value=recruit["signingExpectation"], inline=True)
    if committed:
        status = f"Committed to {committed['name']} {committed['nickname']}".strip()
    else:
        status = recruit["recruitStatus"]
    embed.add_field(name="Status", value=status, inline=True)

    # Like CFB: signed recruits show real odds, unsigned ones only a rough read on each team's chances.
    in_the_running = [leader for leader in recruit["leaders"] if leader["odds"] > 0][:12]
    embed.add_field(name="Leading Teams", value="​" if in_the_running else "No teams are in the running yet.", inline=False)
    for leader in in_the_running:
        value = f"Odds {leader['odds']}%" if committed else leader["prediction"]
        embed.add_field(name=leader["abbreviation"], value=value, inline=True)
    embed.set_thumbnail(url=logo_url)
    embed.set_footer(text="Simulation Sports Network")
    return embed


def Get_LAX_Class_Embed(data, logo_url):
    team = data["team"]
    name = f"{team['name']} {team['nickname']}".strip()
    embed = discord.Embed(colour=_lax_stream_team_colour(team, discord.Colour.dark_gold()),
                          description=f"**Total Recruits:** {data['signees']}",
                          title=f"{team['name']} Recruiting Class")
    # With no signees every class scores 0 and the server breaks the tie alphabetically, so a rank would mean nothing.
    rank = f"#{data['rank']} of {data['teamCount']}" if data["signees"] > 0 else "Unranked"
    embed.add_field(name="Class Rank", value=rank, inline=True)
    embed.add_field(name="Class Score", value=round(data["score"], 2), inline=True)
    embed.add_field(name="Signees by Stars", value=f"5-Star: {data['fiveStars']} | 4-Star: {data['fourStars']} | 3-Star: {data['threeStars']}", inline=True)
    if not data["recruits"]:
        embed.add_field(name="No Signees", value=f"{name} has not signed any croots", inline=False)
    for recruit in data["recruits"][:20]:
        embed.add_field(
            name=f"{recruit['firstName']} {recruit['lastName']} {recruit['id']}"[:256],
            value=f"{recruit['stars']} Star {recruit['archetype']} {recruit['position']} from {recruit['state'] or recruit['country']}"
                  f"\nOverall: {recruit['overall']} \nPotential: {recruit['potential']}",
            inline=False,
        )
    embed.set_thumbnail(url=logo_url)
    return embed


def _lax_player_description(player):
    year = _LAX_YEARS.get(player["year"], str(player["year"]))
    origin = ", ".join(part for part in (player["state"], player["country"]) if part)
    return f"{player['stars']} Star {year} {player['archetype']} {player['position']} from {origin}"


def _lax_percent(value):
    return "-" if value is None else f"{value:.1f}%"


def _lax_stat_fields(stats, is_goalie):
    # Stats that do not apply to the player (no faceoffs, no penalties, ...) are left out, as CFB does.
    fields = [("Games Played", stats["gamesPlayed"])]
    if is_goalie:
        fields += [("Saves", stats["saves"]), ("Goals Allowed", stats["goalsAllowed"]),
                   ("Save %", _lax_percent(stats["savePercentage"])),
                   ("GAA", "-" if stats["goalsAgainstAverage"] is None else f"{stats['goalsAgainstAverage']:.2f}")]
        if stats["outletAttempts"] > 0:
            fields += [("Outlet Attempts", stats["outletAttempts"]), ("Outlets Completed", stats["outletsCompleted"]),
                       ("Outlet Turnovers", stats["outletTurnovers"])]
        return fields
    fields += [("Goals", stats["goals"]), ("Assists", stats["assists"]), ("Points", stats["points"]),
               ("Shots", stats["shots"]), ("Shots on Goal", stats["shotsOnGoal"]),
               ("Shot %", _lax_percent(stats["shootingPercentage"])),
               ("Ground Balls", stats["groundBalls"]), ("Caused TOs", stats["causedTurnovers"]),
               ("Turnovers", stats["turnovers"])]
    if stats["faceoffsTaken"] > 0:
        fields += [("Faceoffs Won", stats["faceoffsWon"]), ("Faceoffs Taken", stats["faceoffsTaken"]),
                   ("Faceoff %", _lax_percent(stats["faceoffPercentage"]))]
    if stats["penalties"] > 0:
        fields.append(("Penalties", stats["penalties"]))
    if stats["manUpGoals"] > 0:
        fields.append(("Man-Up Goals", stats["manUpGoals"]))
    return fields


def _lax_season_line(stats, is_goalie):
    if is_goalie:
        gaa = "-" if stats["goalsAgainstAverage"] is None else f"{stats['goalsAgainstAverage']:.2f}"
        return f"GP {stats['gamesPlayed']} | Sv {stats['saves']} | GA {stats['goalsAllowed']} | Sv% {_lax_percent(stats['savePercentage'])} | GAA {gaa}"
    line = f"GP {stats['gamesPlayed']} | G {stats['goals']} | A {stats['assists']} | Pts {stats['points']} | Sh% {_lax_percent(stats['shootingPercentage'])}"
    if stats["faceoffsTaken"] > 0:
        line += f" | FO% {_lax_percent(stats['faceoffPercentage'])}"
    return line


def _lax_no_stats_field(embed):
    embed.add_field(name="No Stats Yet", value="Stats appear once this player's games have been published.", inline=False)


def Get_LAX_Player_Stats_Embed(data, stats, logo_url):
    player = data["player"]
    is_goalie = stats["category"] == "goalie"
    season_rows = [row for row in stats["seasons"] if row["season"] == stats["currentSeason"]]
    embed = discord.Embed(colour=discord.Colour.gold(), description=_lax_player_description(player),
                          title=f"{player['firstName']} {player['lastName']} {player['position']}")
    if data["team"]:
        embed.set_author(name=f"{data['team']['name']} {data['team']['nickname']}".strip(), icon_url=logo_url)
    for row in season_rows:
        year = stats["seasonYears"].get(str(row["season"]), row["season"])
        label = f"{year} Season" + (f" ({row['teamAbbreviation']})" if len(season_rows) > 1 else "")
        embed.add_field(name=label, value="Regular season", inline=False)
        for name, value in _lax_stat_fields(row, is_goalie):
            embed.add_field(name=name, value=value, inline=True)
    if not season_rows:
        _lax_no_stats_field(embed)
    embed.set_thumbnail(url=logo_url)
    embed.set_footer(text="Simulation Sports Network")
    return embed


def Get_LAX_Player_Career_Embed(data, stats, logo_url):
    player = data["player"]
    is_goalie = stats["category"] == "goalie"
    embed = discord.Embed(colour=discord.Colour.gold(), description=_lax_player_description(player),
                          title=f"{player['firstName']} {player['lastName']} {player['position']} {player['id']}")
    if data["team"]:
        embed.set_author(name=f"{data['team']['name']} {data['team']['nickname']}".strip(), icon_url=logo_url)
    for row in stats["seasons"][-24:]:
        year = stats["seasonYears"].get(str(row["season"]), row["season"])
        class_year = _LAX_YEARS.get(row["year"], str(row["year"]))
        embed.add_field(name=f"{year} {row['teamAbbreviation']} ({class_year})", value=_lax_season_line(row, is_goalie), inline=False)
    if stats["seasons"]:
        embed.add_field(name="Career", value=_lax_season_line(stats["career"], is_goalie), inline=False)
    else:
        _lax_no_stats_field(embed)
    embed.set_thumbnail(url=logo_url)
    embed.set_footer(text="Simulation Sports Network")
    return embed


def Get_LAX_Player_Embed(data, logo_url):
    player = data["player"]
    team = data["team"]
    embed = discord.Embed(colour=discord.Colour.gold(), description=_lax_player_description(player), title=f"{player['firstName']} {player['lastName']}")
    if team:
        embed.set_author(name=f"{team['name']} {team['nickname']}".strip(), icon_url=logo_url)
    for attribute in player_builder.GetLaxPriorityFields(player):
        embed.add_field(name=attribute["name"], value=attribute["value"], inline=attribute["inline"])
    embed.set_thumbnail(url=logo_url)
    embed.set_footer(text="Simulation Sports Network")
    return embed


_LAX_SUB_LINE = re.compile(r"^(.+?) (OUT|IN): (.+)$")


def _lax_is_routine(play):
    return play["outcomeType"] == "complete" and play["actionType"] in ("pass", "move")


def _lax_in_backcourt(play):
    return (play["fieldArea"] or "").startswith("defensive")


def Get_LAX_Stream_Plays(plays):
    # Cut-off moves and routine passes/moves in the possessing team's own defensive zones are
    # skipped, and all but the last of a run of the same routine pass/move by one team.
    # Substitutions are not posted on their own: each stoppage's rows (both teams, one clock) are folded into
    # the message of the play before it as play["AttachedSubstitutions"], a list with one list of rows per
    # stoppage. Substitutions before the first streamed play (the opening line change) ride on that first play
    # instead; only a game with no streamed plays at all would post them as messages of their own.
    candidates = [
        play for play in plays
        if not (play["actionType"] == "move" and play["outcomeType"] == "stopped")
        and not (_lax_is_routine(play) and _lax_in_backcourt(play))
    ]
    stream_plays = []
    stoppage = None
    leading = []
    for idx, play in enumerate(candidates):
        if play["actionType"] == "substitution":
            same_stoppage = (
                stoppage is not None
                and candidates[idx - 1]["actionType"] == "substitution"
                and stoppage["period"] == play["period"]
                and stoppage["timeRemaining"] == play["timeRemaining"]
            )
            if same_stoppage:
                stoppage["rows"].append(play)
                continue
            stoppage = {"period": play["period"], "timeRemaining": play["timeRemaining"], "rows": [play]}
            last = stream_plays[-1] if stream_plays else None
            if last is None:
                leading.append(stoppage["rows"])
                continue
            if "AttachedSubstitutions" not in last:
                last = {**last, "AttachedSubstitutions": []}          # copy, so the API data is never modified
                stream_plays[-1] = last
            last["AttachedSubstitutions"].append(stoppage["rows"])
            continue
        stoppage = None
        next_play = candidates[idx + 1] if idx + 1 < len(candidates) else None
        if (
            next_play is not None
            and _lax_is_routine(play)
            and _lax_is_routine(next_play)
            and play["actionType"] == next_play["actionType"]
            and play["possessionTeamId"] == next_play["possessionTeamId"]
        ):
            continue
        if leading:
            play = {**play, "AttachedSubstitutions": leading}
            leading = []
        stream_plays.append(play)
    for rows in leading:
        stream_plays.append({**rows[0], "Substitutions": rows})
    return stream_plays


def _lax_substitution_summary(stoppages, home):
    """One line per team per stoppage, e.g. 'BU out: M Andrew Handel | in: M Phillip Walter', home team first."""
    home_abbr = home["abbreviation"] or home["name"]
    lines = []
    for rows in stoppages:
        teams = {}
        for row in rows:
            for line in row["playRemark"].splitlines():
                match = _LAX_SUB_LINE.match(line.strip())
                if match:
                    teams.setdefault(match.group(1), {"OUT": [], "IN": []})[match.group(2)].append(match.group(3))
        if not teams:
            lines.append(" ".join(row["playRemark"].replace("\n", " ") for row in rows))
            continue
        for abbr, names in sorted(teams.items(), key=lambda item: item[0] != home_abbr):
            lines.append(f"**{abbr}** out: {', '.join(names['OUT']) or '-'} | in: {', '.join(names['IN']) or '-'}")
    text = "\n".join(lines)
    return text if len(text) <= 1024 else text[:1021] + "..."


def Get_LAX_Substitution_Embed(play, home, away, home_url, away_url):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        description=f"**{home['name']} {play['homeTeamScore']} - {away['name']} {play['awayTeamScore']}**",
        title=f"Play {play['playNumber']}: Substitution",
    )
    embed.add_field(name="Period", value=_lax_period_label(play["period"]), inline=True)
    embed.add_field(name="Game Clock", value=_lax_clock(play["timeRemaining"]), inline=True)
    embed.add_field(name="Shot Clock", value=str(round(play["shotClockRemaining"])), inline=True)

    # play["Substitutions"] holds every substitution row made at this stoppage, for both teams
    teams = {}
    for row in play["Substitutions"]:
        for line in row["playRemark"].splitlines():
            match = _LAX_SUB_LINE.match(line.strip())
            if match:
                teams.setdefault(match.group(1), {"OUT": [], "IN": []})[match.group(2)].append(match.group(3))
    if teams:
        home_abbr = home["abbreviation"] or home["name"]
        ordered = sorted(teams.items(), key=lambda item: item[0] != home_abbr)
        for direction in ("OUT", "IN"):
            for abbr, names in ordered:
                embed.add_field(name=f"{abbr} {direction}:", value="\n".join(names[direction]) or "Not recorded", inline=True)
            for _ in range(3 - len(ordered)):
                embed.add_field(name="​", value="​", inline=True)
    else:
        embed.add_field(name="Result", value="\n\n".join(row["playRemark"] for row in play["Substitutions"])[:1024], inline=False)
    embed.set_thumbnail(url=home_url if play["possessionTeamId"] == home["id"] else away_url)
    return embed


def Get_LAX_Play_Embed(play, home, away, home_url, away_url, injury_url, penalty_url):
    if play.get("Substitutions"):
        return Get_LAX_Substitution_Embed(play, home, away, home_url, away_url)
    in_possession_home = play["possessionTeamId"] == home["id"]
    possession = home if in_possession_home else away
    embed_url = home_url if in_possession_home else away_url
    colour = _lax_team_colour(possession, discord.Colour.light_gray())
    if play["isGoal"]:
        colour = discord.Colour.green()
        if play["actionTeamId"] is not None:
            embed_url = home_url if play["actionTeamId"] == home["id"] else away_url
    elif play["isInjury"]:
        colour = discord.Colour.red()
        embed_url = injury_url
    elif play["isPenalty"]:
        colour = discord.Colour.yellow()
        embed_url = penalty_url
    embed = discord.Embed(
        colour=colour,
        description=f"**{home['name']} {play['homeTeamScore']} - {away['name']} {play['awayTeamScore']}**",
        title=f"Play {play['playNumber']}: {_lax_play_label(play)}",
    )
    embed.add_field(name="Period", value=_lax_period_label(play["period"]), inline=True)
    embed.add_field(name="Game Clock", value=_lax_clock(play["timeRemaining"]), inline=True)
    embed.add_field(name="Shot Clock", value=str(round(play["shotClockRemaining"])), inline=True)
    remark = play["playRemark"]
    if len(remark) > 1024:
        remark = remark[:1021] + "..."
    embed.add_field(name="Result", value=remark, inline=False)
    if play["fieldPos"]:
        embed.add_field(name="Field", value=f"```text\n{play['fieldPos']}\n```", inline=False)
    if play.get("AttachedSubstitutions"):
        embed.add_field(name="Substitutions", value=_lax_substitution_summary(play["AttachedSubstitutions"], home), inline=False)
    embed.set_thumbnail(url=embed_url)
    return embed


_BB_EVENT_LABELS = {
    "Tipoff": "Tip-Off",
    "Ot_tipoff": "Overtime Tip-Off",
    "Steal": "Steal",
    "Turnover": "Turnover",
    "Move": "Dribble Move",
    "Pass_ball": "Pass",
    "Heave": "Heave",
    "Free_throw": "Free Throw",
    "Shot_three": "Three-Pointer",
    "Shot_corner_three": "Corner Three",
    "Shot_inside": "Inside Shot",
    "Shot_paint": "Shot in the Paint",
    "Shot_midrange": "Mid-Range Jumper",
    "QuarterOver": "End of Quarter",
    "HalfOver": "Halftime",
    "GameOver": "End of Game",
    "OvertimeStart": "Overtime Start",
    "OvertimeOver": "End of Overtime",
    "Timeout": "Timeout",
    "Rebound": "Rebound",
    "Inbound": "Inbound",
}

_BB_SHOT_EVENTS = {"Shot_three", "Shot_corner_three", "Shot_inside", "Shot_paint", "Shot_midrange", "Heave", "Free_throw"}
_BB_MADE_OUTCOMES = {"Shot_made", "Shot_foul_made", "Heave_made", "Ft_made"}
_BB_MISSED_OUTCOMES = {"Shot_missed", "Shot_foul_missed", "Shot_blocked", "Shot_foul_blocked", "Heave_missed", "Ft_missed"}
_BB_TURNOVER_OUTCOMES = {"Pass_intercepted", "Steal_success", "Out_of_bounds_turnover", "Offensive_charge", "Shot_clock_violation", "Move_trapped"}
_BB_FOUL_OUTCOMES = {"Shot_foul_made", "Shot_foul_missed", "Shot_foul_blocked", "Move_foul", "Pass_foul", "Offensive_charge"}


def _bb_label(value):
    return str(value).replace("_", " ").strip()


def _bb_colour(event, outcome):
    if outcome in _BB_MADE_OUTCOMES:
        return discord.Colour.green()
    if outcome in _BB_MISSED_OUTCOMES:
        return discord.Colour.red()
    if outcome in _BB_TURNOVER_OUTCOMES:
        return discord.Colour.dark_orange()
    if event in ("QuarterOver", "HalfOver", "GameOver", "OvertimeStart", "OvertimeOver", "Timeout"):
        return discord.Colour.dark_gray()
    return discord.Colour.blue()

def Get_Timeout_Embed():
    # Decide which ad to play
    title = ""
    description = ""
    embed = discord.Embed(
        colour= discord.Colour.yellow(),
        description=description,
        title=title,
    )
    return embed

def Get_Basketball_Intro_Embed(game, title, description, thumbnail_url):
    embed = discord.Embed(colour=discord.Colour.orange(), description=description, title=title)
    match_name = (game.get("GameLabel") or "").strip()
    if match_name:
        embed.add_field(name="Match Name", value=match_name, inline=False)
    arena = game.get("Arena") or ""
    location = ", ".join(part for part in (game.get("City"), game.get("State")) if part)
    if arena or location:
        embed.add_field(name=arena or "Venue", value=location or "​", inline=False)
    for side in ("Home", "Away"):
        pace = (game.get(f"{side}Pace") or "").strip()
        offense = (game.get(f"{side}OffensiveFormation") or "").strip()
        defense = (game.get(f"{side}DefensiveFormation") or "").strip()
        if pace or offense or defense:
            embed.add_field(name=f"{side} Pace", value=pace or "-", inline=True)
            embed.add_field(name=f"{side} Offense", value=offense or "-", inline=True)
            embed.add_field(name=f"{side} Defense", value=defense or "-", inline=True)
    embed.set_thumbnail(url=thumbnail_url)
    return embed


def Get_Basketball_Play_Embed(play, home_team, away_team, home_url, away_url, home_score, away_score, injury_url, penalty_url):
    event = play["Event"]
    outcome = play["Outcome"]
    quarter = play["Quarter"]
    time_remaining = play["TimeOnClock"]
    shot_clock = play["ShotClock"]
    seconds_consumed = play["SecondsConsumed"]
    play_num = play["PlayNumber"]
    injury_id = play["InjuryID"]
    penalty_id = play["PenaltyID"]

    stream_result = play["Result"]
    if not stream_result:
        result = play["StreamResult"] or []
        stream_result = "".join(result)
    if not stream_result:
        stream_result = _bb_label(outcome)

    is_home = play["TeamID"] == play["HomeTeamID"]
    possession = home_team if is_home else away_team
    embed_url = home_url if is_home else away_url
    if injury_id > 0:
        embed_url = injury_url
    elif outcome in _BB_FOUL_OUTCOMES and penalty_url:
        embed_url = penalty_url

    if event == "Substitution":
        return Get_Basketball_Substitution_Embed(play, home_team, away_team, home_score, away_score, embed_url)

    event_label = _BB_EVENT_LABELS.get(event, _bb_label(event))
    quarter_label = f"Q{quarter}" if quarter <= 4 else f"OT{quarter - 4}"

    embed = discord.Embed(
        colour=_bb_colour(event, outcome),
        description=f"**{home_team} {home_score} - {away_team} {away_score}**",
        title=f"Play {play_num}: {event_label}",
    )
    embed.add_field(name="Period", value=quarter_label, inline=True)
    embed.add_field(name="Game Clock", value=time_remaining, inline=True)
    embed.add_field(name="Shot Clock", value=str(shot_clock), inline=True)

    if injury_id > 0:
        embed.add_field(
            name="Injury",
            value=f"Type {play['InjuryType']}, out {play['InjuryDuration']} game(s)",
            inline=False,
        )
    if penalty_id > 0:
        embed.add_field(name="Penalty", value=f"Penalty ID {penalty_id}", inline=False)

    embed.add_field(name="Result", value=stream_result, inline=False)

    court = _FOOTER.get((play["XAxis"], play["YAxis"]), "TIPOFF")
    embed.add_field(name="Court", value=f"```text\n{court}\n```", inline=False)
    embed.set_thumbnail(url=embed_url)
    return embed


def Get_Basketball_Substitution_Embed(play, home_team, away_team, home_score, away_score, embed_url):
    # play["Substitutions"] holds every substitution row made at this stoppage, for both teams
    rows = play["Substitutions"]
    quarter = play["Quarter"]
    quarter_label = f"Q{quarter}" if quarter <= 4 else f"OT{quarter - 4}"

    embed = discord.Embed(
        colour=_bb_colour(play["Event"], play["Outcome"]),
        description=f"**{home_team} {home_score} - {away_team} {away_score}**",
        title=f"Play {play['PlayNumber']}: Substitution",
    )
    embed.add_field(name="Period", value=quarter_label, inline=True)
    embed.add_field(name="Game Clock", value=play["TimeOnClock"], inline=True)
    embed.add_field(name="Shot Clock", value=str(play["ShotClock"]), inline=True)

    team_ids = sorted({row["TeamID"] for row in rows}, key=lambda team_id: team_id != play["HomeTeamID"])
    teams = []
    for team_id in team_ids:
        team_rows = [row for row in rows if row["TeamID"] == team_id]
        fallback = home_team if team_id == play["HomeTeamID"] else away_team
        teams.append((team_rows[0].get("TeamAbbr") or fallback, team_rows))

    for direction, key in (("OUT", "SubstitutedPlayer"), ("IN", "SubstitutePlayer")):
        for abbr, team_rows in teams:
            names = [row.get(key) for row in team_rows if row.get(key)]
            embed.add_field(name=f"{abbr} {direction}:", value="\n".join(names) or "Not recorded", inline=True)
        for _ in range(3 - len(teams)):
            embed.add_field(name="\u200b", value="\u200b", inline=True)

    embed.set_thumbnail(url=embed_url)
    return embed


def Get_Basketball_Play_Delay(play):
    event = play["Event"]
    if event in ("Tipoff", "Ot_tipoff", "QuarterOver", "HalfOver", "GameOver", "OvertimeStart", "OvertimeOver"):
        return 6
    if event in _BB_SHOT_EVENTS or event == "Timeout":
        return 4
    return 2


_BB_ROUTINE_OUTCOMES = {"Move_success", "Pass_success"}
_BB_SKIPPED_OUTCOMES = {"Move_cutoff", "No_passing_lane"}


def _bb_is_routine(play):
    return play["Outcome"] in _BB_ROUTINE_OUTCOMES


def _bb_in_backcourt(play, home_team_id):
    # Home attacks toward +x and away toward -x; the frontcourt starts at |x| >= 1
    if play["TeamID"] == home_team_id:
        return play["XAxis"] <= 0
    return play["XAxis"] >= 0


def Get_Basketball_Stream_Plays(plays, home_team_id):
    # Everything is streamed except cut-off moves, no-lane passes, inbounds, routine backcourt
    # moves/passes, and all but the last of a run of the same routine move/pass.
    # Back-to-back substitution rows at the same clock are merged into one play.
    candidates = [
        play for play in plays
        if play["Outcome"] not in _BB_SKIPPED_OUTCOMES
        and play["Event"] != "Inbound"
        and not (_bb_is_routine(play) and _bb_in_backcourt(play, home_team_id))
    ]
    stream_plays = []
    for idx, play in enumerate(candidates):
        if play["Event"] == "Substitution":
            last = stream_plays[-1] if stream_plays else None
            if (
                last is not None
                and last["Event"] == "Substitution"
                and last["Quarter"] == play["Quarter"]
                and last["TimeOnClock"] == play["TimeOnClock"]
            ):
                last["Substitutions"].append(play)
            else:
                stream_plays.append({**play, "Substitutions": [play]})
            continue
        next_play = candidates[idx + 1] if idx + 1 < len(candidates) else None
        if (
            next_play is not None
            and _bb_is_routine(play)
            and _bb_is_routine(next_play)
            and play["Event"] == next_play["Event"]
            and play["TeamID"] == next_play["TeamID"]
        ):
            continue
        stream_plays.append(play)
    return stream_plays
