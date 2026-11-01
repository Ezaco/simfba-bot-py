import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import logos_util
import id_util
import api_requests
import settings
from helper import embed_builder
from helper.lax_teams import get_lax_teams, find_lax_team, lax_team_choices

class flex(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    flex_group = app_commands.Group(name="flex", description="Compare wins between different programs")

    @flex_group.command(name="cfb", description="Compare the wins between two CFB programs. Input two {teams}")
    async def cfb(self, interaction: discord.Integration, t1: str, t2: str):
        t1_upper = t1.upper()
        t2_upper = t2.upper()
        team_one_id = id_util.GetCollegeFootballTeamID(t1_upper)
        team_two_id = id_util.GetCollegeFootballTeamID(t2_upper)
        data = api_requests.CompareTwoCFBTeams(team_one_id, team_two_id)
        if data == False:
            await interaction.response.send_message(f"Could not find team based on the provided teams: {t1} {t2}")
        elif data["LatestWin"] == "":
            team_one_url = logos_util.GetCFBLogo(team_one_id)
            title = f"{t1} and {t2} have never played against each other"
            desc = ""
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.set_thumbnail(url=team_one_url)
            await interaction.response.send_message(embed=embed)
        else:
            latest_win = data["LatestWin"]
            team_id = id_util.GetCollegeFootballTeamID(data["LatestWin"].upper())
            latest_win_url = logos_util.GetCFBLogo(team_id)
            current_streak = data["CurrentStreak"]
            team_one_wins = data["TeamOneWins"]
            team_one_losses = data["TeamOneLosses"]
            team_one_streak = data["TeamOneStreak"]
            team_one_season = data["TeamOneMSeason"]
            team_one_margin_score = data["TeamOneMScore"]
            team_two_wins = data["TeamTwoWins"]
            team_two_losses = data["TeamTwoLosses"]
            team_two_streak = data["TeamTwoStreak"]
            team_two_season = data["TeamTwoMSeason"]
            team_two_margin_score = data["TeamTwoMScore"]
            title = f"Comparison Between {t1} and {t2}"
            desc = f"Current Streak: {latest_win} with {current_streak} wins"
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.add_field(name=f"{t1} Wins", value=team_one_wins, inline=True)
            embed.add_field(name=f"{t1} Losses", value=team_one_losses, inline=True)
            embed.add_field(name=f"{t1} Best Streak", value=team_one_streak, inline=True)
            if team_one_season > 0:
                embed.add_field(name=f"{t1} Largest Margin of Victory", value=f"{team_one_margin_score}, {team_one_season}", inline=False)
            embed.add_field(name=f"{t2} Wins", value=team_two_wins, inline=True)
            embed.add_field(name=f"{t2} Losses", value=team_two_losses, inline=True)
            embed.add_field(name=f"{t2} Best Streak", value=team_two_streak, inline=True)
            if team_two_season > 0:
                embed.add_field(name=f"{t2} Largest Margin of Victory", value=f"{team_two_margin_score}, {team_two_season}", inline=True)
            embed.set_thumbnail(url=latest_win_url)
            await interaction.response.send_message(embed=embed)

    @flex_group.command(name="nfl", description="Compare the wins between two NFL teams. Input two {teams}")
    async def nfl(self, interaction: discord.Integration, t1: str, t2: str):
        t1_upper = t1.upper()
        t2_upper = t2.upper()
        team_one_id = id_util.GetNFLTeamID(t1_upper)
        team_two_id = id_util.GetNFLTeamID(t2_upper)
        data = api_requests.CompareTwoNFLTeams(team_one_id, team_two_id)
        if data == False:
            await interaction.response.send_message(f"These teams have never played against each other")
        elif data["LatestWin"] == "":
            team_one_url = logos_util.GetNFLLogo(team_one_id)
            title = f"{t1} and {t2} have never played against each other"
            desc = ""
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.set_thumbnail(url=team_one_url)
            await interaction.response.send_message(embed=embed)
        else:
            latest_win = data["LatestWin"]
            team_id = id_util.GetNFLTeamID(data["LatestWin"].upper())
            latest_win_url = logos_util.GetNFLLogo(team_id)
            current_streak = data["CurrentStreak"]
            team_one_wins = data["TeamOneWins"]
            team_one_losses = data["TeamOneLosses"]
            team_one_streak = data["TeamOneStreak"]
            team_one_season = data["TeamOneMSeason"]
            team_one_margin_score = data["TeamOneMScore"]
            team_two_wins = data["TeamTwoWins"]
            team_two_losses = data["TeamTwoLosses"]
            team_two_streak = data["TeamTwoStreak"]
            team_two_season = data["TeamTwoMSeason"]
            team_two_margin_score = data["TeamTwoMScore"]
            title = f"Comparison Between {t1} and {t2}"
            desc = f"Current Streak: {latest_win} with {current_streak} wins"
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.add_field(name=f"{t1} Wins", value=team_one_wins, inline=True)
            embed.add_field(name=f"{t1} Losses", value=team_one_losses, inline=True)
            embed.add_field(name=f"{t1} Best Streak", value=team_one_streak, inline=True)
            if team_one_season > 0:
                embed.add_field(name=f"{t1} Largest Margin of Victory", value=f"{team_one_margin_score}, {team_one_season}", inline=False)
            embed.add_field(name=f"{t2} Wins", value=team_two_wins, inline=True)
            embed.add_field(name=f"{t2} Losses", value=team_two_losses, inline=True)
            embed.add_field(name=f"{t2} Best Streak", value=team_two_streak, inline=True)
            if team_two_season > 0:
                embed.add_field(name=f"{t2} Largest Margin of Victory", value=f"{team_two_margin_score}, {team_two_season}", inline=True)
            embed.set_thumbnail(url=latest_win_url)
            await interaction.response.send_message(embed=embed)

    @flex_group.command(name="cbb", description="Compare the wins between two CBB programs. Input two {teams}")
    async def cbb(self, interaction: discord.Integration, t1: str, t2: str):
        t1_upper = t1.upper()
        t2_upper = t2.upper()
        team_one_id = id_util.GetCollegeBasketballTeamID(t1_upper)
        team_two_id = id_util.GetCollegeBasketballTeamID(t2_upper)
        data = api_requests.CompareTwoCBBTeams(team_one_id, team_two_id)
        if data == False:
            await interaction.response.send_message(f"Could not find team based on the provided teams: {t1} {t2}")
        elif data["LatestWin"] == "":
            team_one_url = logos_util.GetCBBLogo(team_one_id)
            title = f"{t1} and {t2} have never played against each other"
            desc = ""
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.set_thumbnail(url=team_one_url)
            await interaction.response.send_message(embed=embed)
        else:
            latest_win = data["LatestWin"]
            team_id = id_util.GetCollegeBasketballTeamID(data["LatestWin"].upper())
            latest_win_url = logos_util.GetCBBLogo(team_id)
            current_streak = data["CurrentStreak"]
            team_one_wins = data["TeamOneWins"]
            team_one_losses = data["TeamOneLosses"]
            team_one_streak = data["TeamOneStreak"]
            team_one_season = data["TeamOneMSeason"]
            team_one_margin_score = data["TeamOneMScore"]
            team_two_wins = data["TeamTwoWins"]
            team_two_losses = data["TeamTwoLosses"]
            team_two_streak = data["TeamTwoStreak"]
            team_two_season = data["TeamTwoMSeason"]
            team_two_margin_score = data["TeamTwoMScore"]
            title = f"Comparison Between {t1} and {t2}"
            desc = f"Current Streak: {latest_win} with {current_streak} wins"
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.add_field(name=f"{t1} Wins", value=team_one_wins, inline=True)
            embed.add_field(name=f"{t1} Losses", value=team_one_losses, inline=True)
            embed.add_field(name=f"{t1} Best Streak", value=team_one_streak, inline=True)
            if team_one_season > 0:
                embed.add_field(name=f"{t1} Largest Margin of Victory", value=f"{team_one_margin_score}, {team_one_season}", inline=False)
            embed.add_field(name=f"{t2} Wins", value=team_two_wins, inline=True)
            embed.add_field(name=f"{t2} Losses", value=team_two_losses, inline=True)
            embed.add_field(name=f"{t2} Best Streak", value=team_two_streak, inline=True)
            if team_two_season > 0:
                embed.add_field(name=f"{t2} Largest Margin of Victory", value=f"{team_two_margin_score}, {team_two_season}", inline=True)
            embed.set_thumbnail(url=latest_win_url)
            await interaction.response.send_message(embed=embed)

    @flex_group.command(name="nba", description="Compare the wins between two NBA teams. Input two {teams}")
    async def nba(self, interaction: discord.Integration, t1: str, t2: str):
        t1_upper = t1.upper()
        t2_upper = t2.upper()
        team_one_id = id_util.GetNBATeamID(t1_upper)
        team_two_id = id_util.GetNBATeamID(t2_upper)
        data = api_requests.CompareTwoNBATeams(team_one_id, team_two_id)
        if data == False:
            await interaction.response.send_message(f"These teams have never played against each other")
        elif data["LatestWin"] == "":
            team_one_url = logos_util.GetNBALogo(team_one_id)
            title = f"{t1} and {t2} have never played against each other"
            desc = ""
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.set_thumbnail(url=team_one_url)
            await interaction.response.send_message(embed=embed)
        else:
            latest_win = data["LatestWin"]
            team_id = id_util.GetNBATeamID(data["LatestWin"].upper())
            latest_win_url = logos_util.GetNBALogo(team_id)
            current_streak = data["CurrentStreak"]
            team_one_wins = data["TeamOneWins"]
            team_one_losses = data["TeamOneLosses"]
            team_one_streak = data["TeamOneStreak"]
            team_one_season = data["TeamOneMSeason"]
            team_one_margin_score = data["TeamOneMScore"]
            team_two_wins = data["TeamTwoWins"]
            team_two_losses = data["TeamTwoLosses"]
            team_two_streak = data["TeamTwoStreak"]
            team_two_season = data["TeamTwoMSeason"]
            team_two_margin_score = data["TeamTwoMScore"]
            title = f"Comparison Between {t1} and {t2}"
            desc = f"Current Streak: {latest_win} with {current_streak} wins"
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.add_field(name=f"{t1} Wins", value=team_one_wins, inline=True)
            embed.add_field(name=f"{t1} Losses", value=team_one_losses, inline=True)
            embed.add_field(name=f"{t1} Best Streak", value=team_one_streak, inline=True)
            if team_one_season > 0:
                embed.add_field(name=f"{t1} Largest Margin of Victory", value=f"{team_one_margin_score}, {team_one_season}", inline=False)
            embed.add_field(name=f"{t2} Wins", value=team_two_wins, inline=True)
            embed.add_field(name=f"{t2} Losses", value=team_two_losses, inline=True)
            embed.add_field(name=f"{t2} Best Streak", value=team_two_streak, inline=True)
            if team_two_season > 0:
                embed.add_field(name=f"{t2} Largest Margin of Victory", value=f"{team_two_margin_score}, {team_two_season}", inline=True)
            embed.set_thumbnail(url=latest_win_url)
            await interaction.response.send_message(embed=embed)

    @flex_group.command(name="chl", description="Compare the wins between two CHL programs. Input two {teams}")
    async def chl(self, interaction: discord.Integration, t1: str, t2: str):
        t1_upper = t1.upper()
        t2_upper = t2.upper()
        team_one_id = id_util.GetCollegeHockeyTeamID(t1_upper)
        team_two_id = id_util.GetCollegeHockeyTeamID(t2_upper)
        data = api_requests.CompareTwoCHLTeams(team_one_id, team_two_id)
        if data == False:
            await interaction.response.send_message(f"Could not find team based on the provided teams: {t1} {t2}")
        elif data["LatestWin"] == "":
            team_one_url = logos_util.GetCHLLogo(team_one_id)
            title = f"{t1} and {t2} have never played against each other"
            desc = ""
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.set_thumbnail(url=team_one_url)
            await interaction.response.send_message(embed=embed)
        else:
            latest_win = data["LatestWin"]
            team_id = id_util.GetCollegeHockeyTeamID(data["LatestWin"].upper())
            latest_win_url = logos_util.GetCHLLogo(team_id)
            current_streak = data["CurrentStreak"]
            team_one_wins = data["TeamOneWins"]
            team_one_losses = data["TeamOneLosses"]
            team_one_streak = data["TeamOneStreak"]
            team_one_season = data["TeamOneMSeason"]
            team_one_margin_score = data["TeamOneMScore"]
            team_two_wins = data["TeamTwoWins"]
            team_two_losses = data["TeamTwoLosses"]
            team_two_streak = data["TeamTwoStreak"]
            team_two_season = data["TeamTwoMSeason"]
            team_two_margin_score = data["TeamTwoMScore"]
            title = f"Comparison Between {t1} and {t2}"
            desc = f"Current Streak: {latest_win} with {current_streak} wins"
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.add_field(name=f"{t1} Wins", value=team_one_wins, inline=True)
            embed.add_field(name=f"{t1} Losses", value=team_one_losses, inline=True)
            embed.add_field(name=f"{t1} Best Streak", value=team_one_streak, inline=True)
            if team_one_season > 0:
                embed.add_field(name=f"{t1} Largest Margin of Victory", value=f"{team_one_margin_score}, {team_one_season}", inline=False)
            embed.add_field(name=f"{t2} Wins", value=team_two_wins, inline=True)
            embed.add_field(name=f"{t2} Losses", value=team_two_losses, inline=True)
            embed.add_field(name=f"{t2} Best Streak", value=team_two_streak, inline=True)
            if team_two_season > 0:
                embed.add_field(name=f"{t2} Largest Margin of Victory", value=f"{team_two_margin_score}, {team_two_season}", inline=True)
            embed.set_thumbnail(url=latest_win_url)
            await interaction.response.send_message(embed=embed)

    @flex_group.command(name="phl", description="Compare the wins between two PHL teams. Input two {teams}")
    async def phl(self, interaction: discord.Integration, t1: str, t2: str):
        t1_upper = t1.upper()
        t2_upper = t2.upper()
        team_one_id = id_util.GetPHLTeamID(t1_upper)
        team_two_id = id_util.GetPHLTeamID(t2_upper)
        data = api_requests.CompareTwoPHLTeams(team_one_id, team_two_id)
        if data == False:
            await interaction.response.send_message(f"These teams have never played against each other")
        elif data["LatestWin"] == "":
            team_one_url = logos_util.GetPHLLogo(team_one_id)
            title = f"{t1} and {t2} have never played against each other"
            desc = ""
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.set_thumbnail(url=team_one_url)
            await interaction.response.send_message(embed=embed)
        else:
            latest_win = data["LatestWin"]
            team_id = id_util.GetPHLTeamID(data["LatestWin"].upper())
            latest_win_url = logos_util.GetphlLogo(team_id)
            current_streak = data["CurrentStreak"]
            team_one_wins = data["TeamOneWins"]
            team_one_losses = data["TeamOneLosses"]
            team_one_streak = data["TeamOneStreak"]
            team_one_season = data["TeamOneMSeason"]
            team_one_margin_score = data["TeamOneMScore"]
            team_two_wins = data["TeamTwoWins"]
            team_two_losses = data["TeamTwoLosses"]
            team_two_streak = data["TeamTwoStreak"]
            team_two_season = data["TeamTwoMSeason"]
            team_two_margin_score = data["TeamTwoMScore"]
            title = f"Comparison Between {t1} and {t2}"
            desc = f"Current Streak: {latest_win} with {current_streak} wins"
            embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                description=desc,
                                title=title)
            embed.add_field(name=f"{t1} Wins", value=team_one_wins, inline=True)
            embed.add_field(name=f"{t1} Losses", value=team_one_losses, inline=True)
            embed.add_field(name=f"{t1} Best Streak", value=team_one_streak, inline=True)
            if team_one_season > 0:
                embed.add_field(name=f"{t1} Largest Margin of Victory", value=f"{team_one_margin_score}, {team_one_season}", inline=False)
            embed.add_field(name=f"{t2} Wins", value=team_two_wins, inline=True)
            embed.add_field(name=f"{t2} Losses", value=team_two_losses, inline=True)
            embed.add_field(name=f"{t2} Best Streak", value=team_two_streak, inline=True)
            if team_two_season > 0:
                embed.add_field(name=f"{t2} Largest Margin of Victory", value=f"{team_two_margin_score}, {team_two_season}", inline=True)
            embed.set_thumbnail(url=latest_win_url)
            await interaction.response.send_message(embed=embed)


    @flex_group.command(name="clax", description="Compare the wins between two CLAX programs. Input two {teams}")
    @app_commands.describe(t1="The first team", t2="The second team")
    async def clax(self, interaction: discord.Interaction, t1: str, t2: str):
        try:
            await interaction.response.defer()
            teams = await get_lax_teams()
            if not teams:
                await interaction.followup.send("I couldn't load the CLAX team list right now. Please try again later.")
                return
            team_one = find_lax_team(teams, t1)
            team_two = find_lax_team(teams, t2)
            if team_one is None or team_two is None:
                await interaction.followup.send(f"Could not find team based on the provided teams: {t1} {t2}")
                return
            if team_one["id"] == team_two["id"]:
                await interaction.followup.send("Pick two different teams to compare.")
                return
            data = await asyncio.to_thread(api_requests.GetLaxVersus, team_one["id"], team_two["id"])
            if not data:
                await interaction.followup.send("Could not load that comparison right now. Please try again later.")
                return
            # CFB shows the logo of whoever won last; with no games played, use the first team
            winner = data["latestWinner"] or team_one
            logo_url = api_requests.GetLaxLogoUrl(winner["logoFileName"])
            await interaction.followup.send(embed=embed_builder.Get_LAX_Flex_Embed(data, logo_url))
        except Exception as e:
            print(f"Error occured: {e}")

    @clax.autocomplete("t1")
    async def clax_t1_autocomplete(self, interaction: discord.Interaction, current: str):
        return await lax_team_choices(current)

    @clax.autocomplete("t2")
    async def clax_t2_autocomplete(self, interaction: discord.Interaction, current: str):
        return await lax_team_choices(current)


async def setup(client: commands.Bot):
    await client.add_cog(flex(client))
