import discord
import os
import csv
from api_requests import RevealBBGameResultsOnInterface, StreamBasketballGames
from helper import embed_builder, message_sender, util
import constants
import logos_util
import id_util
import asyncio

async def stream_game(chan, channel: str, week: str, day: str, league: str):
    day_uppercase = day.upper()
    is_pro = league == 'nba'
    streams = StreamBasketballGames(is_pro,channel)
    injury_url = logos_util.GetIcon("Injury")
    penalty_url = logos_util.GetIcon("Penalty")
    for game in streams:
        total_rows = game["Streams"]
        home_team = game["HomeTeam"]
        home_id = game["HomeTeamID"]
        home_rank = game["HomeTeamRank"]
        home_coach = game["HomeTeamCoach"]
        home_tag = game["HomeTeamDiscordID"]
        away_id = game["AwayTeamID"]
        away_team = game["AwayTeam"]
        away_tag = game["AwayTeamDiscordID"]
        away_rank = game["AwayTeamRank"]
        away_coach = game["AwayTeamCoach"]
        game_label = game["GameLabel"]
        arena = game["Arena"]
        city = game["City"]
        state = game["State"]
        country = game["Country"]
        arena = game["Arena"]
        home_ranked_str = ""
        if home_rank > 0:
            home_ranked_str=f"({home_rank}) "
        away_ranked_str = ""
        if away_rank > 0:
            away_ranked_str=f"({away_rank}) "
        contending_teams_str = ""
        hc_label = home_coach.strip() or "AI"
        ac_label = away_coach.strip() or "AI"
        if home_tag != "":
            hc_label = home_tag
        if away_tag != "":
            ac_label = away_tag
        contending_teams_str = f"Home Team: {home_ranked_str}{home_team} | Coach: {hc_label}"
        contending_teams_str += f"\nAway Team: {away_ranked_str}{away_team} | Coach: {ac_label}"
        home_team_abbr = ""
        away_team_abbr = ""
        final_score = ""
        count = 0
        results = []

        ### Logos
        home_team_id = home_id
        home_url = logos_util.GetNBALogo(home_team_id)
        away_team_id = away_id
        away_url = logos_util.GetNBALogo(away_team_id)

        ## Announcer
        announcer = util.PickBKAnnouncer()
        announcer_url = logos_util.GetAnnouncer(announcer)
        intro_text = util.BKAnnouncerIntroText(announcer, home_team_abbr, away_team_abbr, "nba", arena)

        ## Announcer Embed
        announcer_embed = discord.Embed(colour=discord.Colour.blue(),description=intro_text,title=f"Streaming SimNBA Match!")
        announcer_embed.add_field(name="Announcer", value=announcer, inline=False)
        announcer_embed.set_thumbnail(url=announcer_url)
        await message_sender.SendEmbedMessage(chan, announcer_embed)
        await asyncio.sleep(3)
        await message_sender.SendMessage(chan, contending_teams_str)
        await asyncio.sleep(5)
        ### Build Initial Embed
        init_title = f"Streaming NBA Match Live on {channel.upper()}!"
        init_embed = embed_builder.Get_Basketball_Intro_Embed(game, init_title, contending_teams_str, home_url)
        await message_sender.SendEmbedMessage(chan, embed=init_embed)
        await asyncio.sleep(5)
        home_score = 0
        away_score = 0

        for play in embed_builder.Get_Basketball_Stream_Plays(total_rows, home_id):
            home_score = play["HomeTeamScore"]
            away_score = play["AwayTeamScore"]
            play_embed = embed_builder.Get_Basketball_Play_Embed(play, home_team, away_team, home_url, away_url, home_score, away_score, injury_url, penalty_url)
            await message_sender.SendEmbedMessage(chan, embed=play_embed)
            await asyncio.sleep(embed_builder.Get_Basketball_Play_Delay(play))

            if play["Event"] == "Timeout":
                ad = util.PickAd()
                ad_title = util.AdTitleText(ad)
                ad_description = util.AdDescriptionText(ad)
                ad_embed = discord.Embed(colour=discord.Colour.light_gray(), title=ad_title, description=ad_description)
                ad_embed.set_thumbnail(url=logos_util.GetAd(ad))
                await message_sender.SendEmbedMessage(chan, embed=ad_embed)
                await asyncio.sleep(5)
        final_title = "... and that's the game, folks! Thank you for watching!"
        final_score = f"{home_score}-{away_score}"
        final_url = ""
        if home_score > away_score:
            final_url = home_url
        else:
            final_url = away_url
        final_embed = discord.Embed(colour=discord.Colour.light_gray(),description=contending_teams_str,title=final_title)
        final_embed.add_field(name="Final Score", value=final_score, inline=False)
        final_embed.add_field(name="Syncing results...", value="Check the Interface for results & a post-game discussion!", inline=False)
        final_embed.set_thumbnail(url=final_url)
        await message_sender.SendEmbedMessage(chan, embed=final_embed)
        RevealBBGameResultsOnInterface(is_pro, game["GameID"])

        await asyncio.sleep(10)
                                            

    await chan.send(f"That's all for today's games, folks!")