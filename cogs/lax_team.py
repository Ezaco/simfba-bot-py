import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import api_requests
from helper import embed_builder
from helper.lax_teams import get_lax_teams, find_lax_team, lax_team_choices

class LAX_Team(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="clax_team", description="Look up a college lacrosse team")
    @app_commands.describe(team="The team to look up")
    async def clax_team(self, interaction: discord.Interaction, team: str):
        try:
            await interaction.response.defer()
            teams = await get_lax_teams()
            if not teams:
                await interaction.followup.send("I couldn't load the CLAX team list right now. Please try again later.")
                return
            team_data = find_lax_team(teams, team)
            if team_data is None:
                await interaction.followup.send(f"Could not find team: {team}")
                return
            profile = await asyncio.to_thread(api_requests.GetLaxTeamProfile, team_data["id"])
            if not profile:
                await interaction.followup.send(f"Could not load {team_data['name']} right now. Please try again later.")
                return
            logo_url = api_requests.GetLaxLogoUrl(team_data["logoFileName"])
            # The server sends each top player's class year with the team (JSON keys arrive as strings).
            # An older server does not, so only then look the players up one by one.
            player_years = profile.get("topPlayerYears")
            if player_years is None:
                top_player_ids = [player["id"] for player in profile["preview"]["topPlayers"]]
                player_years = await asyncio.to_thread(api_requests.GetLaxPlayerYears, top_player_ids)
            else:
                player_years = {int(player_id): year for player_id, year in player_years.items()}
            await interaction.followup.send(embed=embed_builder.Get_LAX_Team_Embed(profile, logo_url, player_years))
        except Exception as e:
            print(f"Error occured: {e}")

    @clax_team.autocomplete("team")
    async def clax_team_autocomplete(self, interaction: discord.Interaction, current: str):
        return await lax_team_choices(current)

async def setup(client: commands.Bot):
    await client.add_cog(LAX_Team(client))
