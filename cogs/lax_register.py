import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import api_requests
from helper.lax_teams import get_lax_teams, find_lax_team, lax_team_label, lax_team_choices

class LAX_Register(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="clax_register", description="Register to your CLAX team so you will be tagged when games stream!")
    @app_commands.describe(team="Your team")
    async def clax_register(self, interaction: discord.Interaction, team: str):
        try:
            await interaction.response.defer()
            teams = await get_lax_teams()
            if not teams:
                await interaction.followup.send("I couldn't load the CLAX team list right now. Please try again later.")
                return
            team_data = find_lax_team(teams, team)
            if team_data is None:
                await interaction.followup.send(f"I couldn't find a CLAX team called \"{team}\". Pick one from the list that appears as you type.")
                return
            label = lax_team_label(team_data)
            logo_url = api_requests.GetLaxLogoUrl(team_data["logoFileName"])
            registered = await asyncio.to_thread(api_requests.RegisterLaxTeam, team_data["id"], interaction.user.mention)
            if registered:
                embed = discord.Embed(colour=discord.Colour.dark_gold(),
                    description=f"Congratulations! You will now be pinged whenever {label}'s games are streamed.",
                    title=f"Successfully Registered to {label}!")
            else:
                embed = discord.Embed(colour=discord.Colour.dark_gold(),
                    description="Don't worry, you did nothing wrong. Something technical occurred and will be resolved. Please post in forums for details.",
                    title=f"Error! Could not register to {label}!")
            embed.set_thumbnail(url=logo_url)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(f"Error occured: {e}")

    @clax_register.autocomplete("team")
    async def clax_register_autocomplete(self, interaction: discord.Interaction, current: str):
        return await lax_team_choices(current)

async def setup(client: commands.Bot):
    await client.add_cog(LAX_Register(client))
