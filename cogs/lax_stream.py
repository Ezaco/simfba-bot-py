import discord
from discord.ext import commands
from discord import app_commands
from helper import lax_stream_builder
import settings

WEEK_HELP = "Week to stream"
RESTART_HELP = "Start the stream over instead of picking up where the channel left off"

class LAX_Stream(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    def channel_id(self, network_key):
        # A network without its own channel uses the LAX_STREAM test channel.
        return settings.LAX_NETWORK_CHANNELS.get(network_key) or settings.LAX_STREAM_CHANNEL

    def bot_id(self):
        # The bot's own id, so it can recognise its earlier messages in a channel. None (no resume) before it has logged in.
        return getattr(getattr(self.client, "user", None), "id", None)

    async def run_network(self, interaction: discord.Interaction, network_key: str, week: int, restart: bool):
        name = lax_stream_builder.NETWORK_NAMES[network_key]
        chan = self.client.get_channel(self.channel_id(network_key))
        if chan is None:
            await interaction.response.send_message(f"The {name} stream channel isn't configured (LAX_{network_key.upper()}_STREAM).", ephemeral=True)
            return
        await interaction.response.send_message(f"Loading {name} games for the week...")
        await lax_stream_builder.stream_lax_network(network_key, chan, None, week, report=interaction.followup.send, resume=not restart, bot_id=self.bot_id())

    @app_commands.command(name="clax_stream_flo", description="Stream FloSports' share of this week's SimCLAX games")
    @app_commands.describe(week=WEEK_HELP, restart=RESTART_HELP)
    async def clax_stream_flo(self, interaction: discord.Interaction, week: int, restart: bool = False):
        await self.run_network(interaction, "flo", week, restart)

    @app_commands.command(name="clax_stream_laxtv", description="Stream Lacrosse TV's share of this week's SimCLAX games")
    @app_commands.describe(week=WEEK_HELP, restart=RESTART_HELP)
    async def clax_stream_laxtv(self, interaction: discord.Interaction, week: int, restart: bool = False):
        await self.run_network(interaction, "laxtv", week, restart)

    @app_commands.command(name="clax_stream_abc", description="Stream ABC's share of this week's SimCLAX games")
    @app_commands.describe(week=WEEK_HELP, restart=RESTART_HELP)
    async def clax_stream_abc(self, interaction: discord.Interaction, week: int, restart: bool = False):
        await self.run_network(interaction, "abc", week, restart)

    @app_commands.command(name="clax_stream_espnu", description="Stream ESPNU's share of this week's SimCLAX games")
    @app_commands.describe(week=WEEK_HELP, restart=RESTART_HELP)
    async def clax_stream_espnu(self, interaction: discord.Interaction, week: int, restart: bool = False):
        await self.run_network(interaction, "espnu", week, restart)

    @app_commands.command(name="clax_streams", description="Start all four SimCLAX networks at once for the week")
    @app_commands.describe(week=WEEK_HELP, restart=RESTART_HELP)
    async def clax_streams(self, interaction: discord.Interaction, week: int, restart: bool = False):
        ids = {key: self.channel_id(key) for key, _ in lax_stream_builder.NETWORKS}
        if not all(ids.values()):
            await interaction.response.send_message("The SimCLAX stream channels aren't configured (LAX_FLO_STREAM, LAX_LAXTV_STREAM, LAX_ABC_STREAM, LAX_ESPNU_STREAM).", ephemeral=True)
            return
        if len(set(ids.values())) != len(ids):
            await interaction.response.send_message("Each network needs its own channel to run them all at once; two of them share one. Set all four LAX_*_STREAM channels, or start one network at a time.", ephemeral=True)
            return
        channels = {key: self.client.get_channel(channel_id) for key, channel_id in ids.items()}
        missing = [lax_stream_builder.NETWORK_NAMES[key] for key, chan in channels.items() if chan is None]
        if missing:
            await interaction.response.send_message(f"I can't see the channel for: {', '.join(missing)}. Check the channel IDs and the bot's permissions.", ephemeral=True)
            return
        await interaction.response.send_message("Loading SimCLAX games for the week...")
        await lax_stream_builder.stream_lax_week_all(channels, None, week, report=interaction.followup.send, resume=not restart, bot_id=self.bot_id())

async def setup(client: commands.Bot):
    await client.add_cog(LAX_Stream(client))
