import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import api_requests
from helper import embed_builder
from helper.lax_teams import get_lax_teams, find_lax_team, lax_team_choices

class LAX_Recruiting(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="clax_croot", description="Look up a college lacrosse croot using a croot {id}")
    async def clax_croot(self, interaction: discord.Interaction, id: int):
        try:
            await interaction.response.defer()
            recruit = await asyncio.to_thread(api_requests.GetLaxCroot, id)
            if not recruit:
                await interaction.followup.send(f"Could not find player based on the provided id: {id}")
                return
            team = recruit["committedTeam"]
            logo_url = api_requests.GetLaxLogoUrl(team["logoFileName"] if team else None)
            await interaction.followup.send(embed=embed_builder.Get_LAX_Croot_Embed(recruit, logo_url))
        except Exception as e:
            print(f"Error occured: {e}")

    @app_commands.command(name="clax_class", description="Look up a college lacrosse team's recruiting class")
    @app_commands.describe(team="The team to look up")
    async def clax_class(self, interaction: discord.Interaction, team: str):
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
            data = await asyncio.to_thread(api_requests.GetLaxClass, team_data["id"])
            if not data:
                await interaction.followup.send(f"Could not load {team_data['name']}'s recruiting class right now. Please try again later.")
                return
            logo_url = api_requests.GetLaxLogoUrl(team_data["logoFileName"])
            await interaction.followup.send(embed=embed_builder.Get_LAX_Class_Embed(data, logo_url))
        except Exception as e:
            print(f"Error occured: {e}")

    @app_commands.command(name="clax_rankings", description="See the top college lacrosse recruiting classes")
    async def clax_rankings(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            data = await asyncio.to_thread(api_requests.GetLaxClassRankings, 25)
            if not data:
                await interaction.followup.send("Could not load the recruiting class rankings right now. Please try again later.")
                return
            leader = data["rankings"][0]["team"] if data["rankings"] else None
            logo_url = api_requests.GetLaxLogoUrl(leader["logoFileName"] if leader else None)
            await interaction.followup.send(embed=embed_builder.Get_LAX_Rankings_Embed(data, logo_url))
        except Exception as e:
            print(f"Error occured: {e}")

    @clax_class.autocomplete("team")
    async def clax_class_autocomplete(self, interaction: discord.Interaction, current: str):
        return await lax_team_choices(current)

async def setup(client: commands.Bot):
    await client.add_cog(LAX_Recruiting(client))
