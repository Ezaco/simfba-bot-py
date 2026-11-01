import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import api_requests
from helper import embed_builder
from helper.lax_teams import get_lax_teams, find_lax_team, lax_team_choices

async def find_player_by_id(interaction, player_id):
    data = await asyncio.to_thread(api_requests.GetLaxPlayer, player_id)
    if not data:
        await interaction.followup.send(f"Could not find player based on the provided id: {player_id}")
        return None, None
    return data, None

async def find_player_by_name(interaction, first_name, last_name, team):
    teams = await get_lax_teams()
    if not teams:
        await interaction.followup.send("I couldn't load the CLAX team list right now. Please try again later.")
        return None, None
    team_data = find_lax_team(teams, team)
    if team_data is None:
        await interaction.followup.send(f"Could not find team: {team}")
        return None, None
    matches = await asyncio.to_thread(api_requests.GetLaxPlayers, first_name, last_name, team_data["id"])
    if not matches:
        await interaction.followup.send("Could not find player")
        return None, None
    note = None
    if len(matches) > 1:
        note = f"{len(matches)} players on this team share that name; showing the first. Use /clax_player_id for the others."
    return matches[0], note

def logo_for(data):
    return api_requests.GetLaxLogoUrl((data["team"] or {}).get("logoFileName"))

async def send_attributes(interaction, data, note):
    await interaction.followup.send(content=note, embed=embed_builder.Get_LAX_Player_Embed(data, logo_for(data)))

async def send_stats(interaction, data, note):
    stats = await asyncio.to_thread(api_requests.GetLaxPlayerStats, data["player"]["id"])
    if not stats:
        await interaction.followup.send("Could not load that player's stats right now. Please try again later.")
        return
    await interaction.followup.send(content=note, embed=embed_builder.Get_LAX_Player_Stats_Embed(data, stats, logo_for(data)))

async def send_career_stats(interaction, data, note):
    stats = await asyncio.to_thread(api_requests.GetLaxPlayerStats, data["player"]["id"])
    if not stats:
        await interaction.followup.send("Could not load that player's stats right now. Please try again later.")
        return
    await interaction.followup.send(content=note, embed=embed_builder.Get_LAX_Player_Career_Embed(data, stats, logo_for(data)))

class LAX_Player(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    clax_player_id_group = app_commands.Group(name="clax_player_id", description="CLAX Player by ID")
    clax_player_name_group = app_commands.Group(name="clax_player_name", description="CLAX Player by Name")

    @clax_player_id_group.command(name="attributes", description="Look up a college lacrosse player using a player {id}")
    async def id_attributes(self, interaction: discord.Interaction, id: int):
        try:
            await interaction.response.defer()
            data, note = await find_player_by_id(interaction, id)
            if data:
                await send_attributes(interaction, data, note)
        except Exception as e:
            print(f"Error occured: {e}")

    @clax_player_id_group.command(name="stats", description="Look up a college lacrosse player's season stats using a player {id}")
    async def id_stats(self, interaction: discord.Interaction, id: int):
        try:
            await interaction.response.defer()
            data, note = await find_player_by_id(interaction, id)
            if data:
                await send_stats(interaction, data, note)
        except Exception as e:
            print(f"Error occured: {e}")

    @clax_player_id_group.command(name="career_stats", description="Look up a college lacrosse player's career stats using a player {id}")
    async def id_career_stats(self, interaction: discord.Interaction, id: int):
        try:
            await interaction.response.defer()
            data, note = await find_player_by_id(interaction, id)
            if data:
                await send_career_stats(interaction, data, note)
        except Exception as e:
            print(f"Error occured: {e}")

    @clax_player_name_group.command(name="attributes", description="Look up a college lacrosse player using a {first name}, {last name}, and {team}")
    @app_commands.describe(team="The player's team")
    async def name_attributes(self, interaction: discord.Interaction, first_name: str, last_name: str, team: str):
        try:
            await interaction.response.defer()
            data, note = await find_player_by_name(interaction, first_name, last_name, team)
            if data:
                await send_attributes(interaction, data, note)
        except Exception as e:
            print(f"Error occured: {e}")

    @clax_player_name_group.command(name="stats", description="Look up a college lacrosse player's season stats using a {first name}, {last name}, and {team}")
    @app_commands.describe(team="The player's team")
    async def name_stats(self, interaction: discord.Interaction, first_name: str, last_name: str, team: str):
        try:
            await interaction.response.defer()
            data, note = await find_player_by_name(interaction, first_name, last_name, team)
            if data:
                await send_stats(interaction, data, note)
        except Exception as e:
            print(f"Error occured: {e}")

    @name_attributes.autocomplete("team")
    async def name_attributes_team_autocomplete(self, interaction: discord.Interaction, current: str):
        return await lax_team_choices(current)

    @name_stats.autocomplete("team")
    async def name_stats_team_autocomplete(self, interaction: discord.Interaction, current: str):
        return await lax_team_choices(current)

async def setup(client: commands.Bot):
    await client.add_cog(LAX_Player(client))
