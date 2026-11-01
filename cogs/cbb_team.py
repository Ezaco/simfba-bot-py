import discord
from discord.ext import commands
from discord import app_commands
import logos_util
import id_util
import api_requests

class cbb_team(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @app_commands.command(name="cbb_team", description="Look up a college basketball team")
    async def cbb_team(self, interaction: discord.Integration, team: str):
        upper_input = team.upper()
        team_id = id_util.GetCollegeBasketballTeamID(upper_input)
        logo_url = logos_util.GetCBBLogo(team_id)
        data = api_requests.GetCollegeBasketballTeam(team_id)
        if data == False:
            await interaction.response.send_message(f"Could not find team: {upper_input}")
        else:
            team_data = data["TeamData"]
            team_standings = data["TeamStandings"]
            matches = data["UpcomingMatches"]
            if len(team_data['State']) == 0:
                title = f"{team_data['Team']} {team_data['Nickname']}"
                desc = f"Team based in {team_data['City']}, {team_data['Country']}. Members of the {team_data['Conference']}."
                embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                    description=desc,
                                    title=title)
                coach = ""
                if len(team_data['Coach']) > 0:
                    coach = team_data['Coach']
                else:
                    coach = "AI"

                embed.add_field(name="Coach", value=coach, inline=True)
                if team_standings['PostSeasonStatus'] != "None":
                    embed.add_field(name="Post-Season Status", value=team_standings['PostSeasonStatus'], inline=False)
                current_record_label = f"{team_standings['TotalWins']}-{team_standings['TotalLosses']} ({team_standings['ConferenceWins']}-{team_standings['ConferenceLosses']})"
                embed.add_field(name="Current Record", value=f"{current_record_label}", inline=True)
                embed.add_field(name="Arena", value=team_data['Arena'], inline=False)
                a_rank_label = ''
                h_rank_label = ''
                embed.add_field(name="Schedule", value="", inline=False)

                x = 0

                if len(matches) > 0:
                    for m in matches:
                        if x >= len(matches)-4:
                            is_complete = m['GameComplete']
                            match_description = ""
                            neutral_label = ""
                            conf_label = ""
                            conf_tourney_label = ""
                            bowl_label =""
                            playoff_label = ""
                            natty_label = ""
                            match_arena = f"{m['Arena']}"
                            ovr_desc = ""
                            match = f"{m['AwayTeam']} at {m['HomeTeam']} | At {match_arena}"
                            if is_complete == True:
                                match_description = f"{m['AwayTeamScore']}-{m['HomeTeamScore']}"
                            else:
                                match_description = ""
                            embed.add_field(name="", value=match, inline=False)
                            embed.add_field(name=match_description, value="", inline=False)
                        x += 1
    
                embed.set_thumbnail(url=logo_url)
                await interaction.response.send_message(embed=embed)

            else:
                title = f"{team_data['Team']} {team_data['Nickname']}"
                desc = f"Team based in {team_data['City']}, {team_data['State']}. Members of the {team_data['Conference']} conference."
                embed = discord.Embed(colour=discord.Colour.dark_gold(),
                                    description=desc,
                                    title=title)
               
                coach = ""
                if len(team_data['Coach']) > 0:
                    coach = team_data['Coach']
                else:
                    coach = "AI"

                embed.add_field(name="Coach", value=coach, inline=True)
                if team_standings['PostSeasonStatus'] != "None":
                    embed.add_field(name="Post-Season Status", value=team_standings['PostSeasonStatus'], inline=False)
                current_record_label = f"{team_standings['TotalWins']}-{team_standings['TotalLosses']} ({team_standings['ConferenceWins']}-{team_standings['ConferenceLosses']})"
                embed.add_field(name="Current Record", value=f"{current_record_label}", inline=True)
                embed.add_field(name="Arena", value=team_data['Arena'], inline=False)
                a_rank_label = ''
                h_rank_label = ''
                embed.add_field(name="Schedule", value="", inline=False)

                x = 0

                if len(matches) > 0:
                    for m in matches:
                        if x >= len(matches)-4:
                            is_complete = m['GameComplete']
                            match_description = ""
                            neutral_label = ""
                            conf_label = ""
                            conf_tourney_label = ""
                            bowl_label =""
                            playoff_label = ""
                            natty_label = ""
                            match_arena = f"{m['Arena']}"
                            ovr_desc = ""
                            match = f"{m['AwayTeam']} at {m['HomeTeam']} | At {match_arena}"
                            if is_complete == True:
                                match_description = f"{m['AwayTeamScore']}-{m['HomeTeamScore']}"
                            else:
                                match_description = ""
                            embed.add_field(name="", value=match, inline=False)
                            embed.add_field(name=match_description, value="", inline=False)
                        x += 1
    
                embed.set_thumbnail(url=logo_url)
                await interaction.response.send_message(embed=embed)
                
async def setup(client: commands.Bot):
    await client.add_cog(cbb_team(client))
