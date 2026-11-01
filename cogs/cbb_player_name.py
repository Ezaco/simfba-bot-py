import discord
from discord.ext import commands
from discord import app_commands
import logos_util
import id_util
import api_requests
import settings

class cbb_player_name(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    cbb_player_name_group = app_commands.Group(name="cbb_player_name", description="CBB Player by Name")


    @cbb_player_name_group.command(name="attributes", description="Look up a college basketball player using a {first name}, {last name}, and {team}")
    async def attributes(self, interaction: discord.Interaction, first_name: str, last_name: str, team: str):
            team_abbreviation = team.upper()
            team_id = id_util.GetCollegeBasketballTeamID(team_abbreviation)
            logo_url = logos_util.GetCBBLogo(team_id)
            data = api_requests.GetCollegeBasketballPlayer(first_name, last_name, team_id)
            if data == False:
                await interaction.response.send_message(f"Could not find player: {first_name} {last_name} on {team_abbreviation}")
            else:
                location = ""
                if data['Country'] == 'USA':
                    location = data['State']
                else:
                    location = data['Country']
                stats = data["SeasonStats"]
                title = f"{data['FirstName']} {data['LastName']} {data['Position']}"
                desc = f"{data['Stars']} Star {data['Archetype']} {data['Position']} from {location}"
                

                embed = discord.Embed(colour=discord.Colour.orange(),
                                    description=desc,
                                    title=title)

                # Player Attribute Embeds
                embed.add_field(name="Inside Shooting", value=data['FinishingGrade'], inline=True)
                embed.add_field(name="MidRange Shooting", value=data['Shooting2Grade'], inline=True)
                embed.add_field(name="3pt Shooting", value=data['Shooting3Grade'], inline=True)
                embed.add_field(name="Free Throw", value=data['FreeThrowGrade'], inline=True)
                embed.add_field(name="Agility", value=data['AgilityGrade'], inline=True)
                embed.add_field(name="Ballwork", value=data['BallworkGrade'], inline=True)
                embed.add_field(name="Stealing", value=data['StealingGrade'], inline=True)
                embed.add_field(name="Blocking", value=data['BlockingGrade'], inline=True)
                embed.add_field(name="Rebounding", value=data['ReboundingGrade'], inline=True)
                embed.add_field(name="Interior Defense", value=data['InteriorDefenseGrade'], inline=True)
                embed.add_field(name="Perimeter Defense", value=data['PerimeterDefenseGrade'], inline=True)
                embed.add_field(name="Overall", value=data['OverallGrade'], inline=True)
                embed.add_field(name="Stamina", value=f"{data['Stamina']}", inline=True)
                embed.add_field(name="Potential", value=data['PotentialGrade'], inline=True)
                embed.set_thumbnail(url=logo_url)
                embed.set_footer(text="Simulation Sports Network")
                await interaction.response.send_message(embed=embed)

    @cbb_player_name_group.command(name="stats", description="Look up a college basketball player using a {first name}, {last name}, and {team}")
    async def stats(self, interaction: discord.Interaction, first_name: str, last_name: str, team: str):
            team_abbreviation = team.upper()
            team_id = id_util.GetCollegeBasketballTeamID(team_abbreviation)
            logo_url = logos_util.GetCBBLogo(team_id)
            data = api_requests.GetCollegeBasketballPlayer(first_name, last_name, team_id)
            if data == False:
                await interaction.response.send_message(f"Could not find player")
            else:
                location = ""
                if data['Country'] == 'USA':
                    location = data['State']
                else:
                    location = data['Country']
                stats = data["SeasonStats"]
                title = f"{data['FirstName']} {data['LastName']} {data['Position']}"
                desc = f"{data['Stars']} Star {data['Archetype']} {data['Position']} from {location}"

                embed = discord.Embed(colour=discord.Colour.orange(),
                                    description=desc,
                                    title=title)

                # Player Stats Embeds
                embed.add_field(name="Games Played", value=stats['GamesPlayed'], inline=True)
                embed.add_field(name="Minutes Per Game", value=stats['MinutesPerGame'], inline=True)
                embed.add_field(name="Possessions Per Game", value=stats['PossessionsPerGame'], inline=True)
                embed.add_field(name="FGs Attempted", value=stats['FGA'], inline=True)
                embed.add_field(name="FGs Made", value=stats['FGM'], inline=True)
                try:
                    embed.add_field(name="FG %", value=str(round((stats['FGM']/stats['FGA'])*100,2))+"%", inline=True)
                except Exception as e:
                    embed.add_field(name="FG %", value="N/A", inline=True)
                embed.add_field(name="3 Pointers Attempted", value=stats['ThreePointAttempts'], inline=True)
                embed.add_field(name="3 Pointers Made", value=stats['ThreePointsMade'], inline=True)
                try:
                    embed.add_field(name="3 Point %", value=str(round((stats['ThreePointsMade']/stats['ThreePointAttempts'])*100,2))+"%", inline=True)
                except Exception as e:
                    embed.add_field(name="3 Point %", value="N/A", inline=True)
                embed.add_field(name="FTs Attempted", value=stats['FTA'], inline=True)
                embed.add_field(name="FTs Made", value=stats['FTM'], inline=True)
                try:
                    embed.add_field(name="FT %", value=str(round((stats['FTM']/stats['FTA'])*100,2))+"%", inline=True)
                except Exception as e:
                    embed.add_field(name="FT %", value="N/A", inline=True)
                embed.add_field(name="Offensive Rebounds", value=stats['OffRebounds'], inline=True)
                embed.add_field(name="Defensiv Rebounds", value=stats['DefRebounds'], inline=True)
                embed.add_field(name="Total Rebounds", value=stats['TotalRebounds'], inline=True)
                embed.add_field(name="Assists", value=stats['Assists'], inline=True)
                embed.add_field(name="Steals", value=stats['Steals'], inline=True)
                embed.add_field(name="Blocks", value=stats['Blocks'], inline=True)
                embed.add_field(name="Turnovers", value=stats['Turnovers'], inline=True)
                embed.add_field(name="Fouls", value=stats['Fouls'], inline=True)
                embed.set_thumbnail(url=logo_url)
                embed.set_footer(text="Simulation Sports Network")
                await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(cbb_player_name(client))
