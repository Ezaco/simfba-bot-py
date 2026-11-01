import os
import pathlib
import logging
import discord
from dotenv import load_dotenv

load_dotenv()

def GetEnvironmentVariable(var):
    env_var = os.getenv(var)
    return int(env_var)

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / 'cmds'
COGS_DIR = BASE_DIR / 'cogs'


GUILDS_ID = discord.Object(id=GetEnvironmentVariable("GUILD_ID"))
GUILD_ID_INT = GetEnvironmentVariable("GUILD_ID")
STREAM_CHANNEL = GetEnvironmentVariable("FBS_STREAM")
B1G_NOON = GetEnvironmentVariable("BIG_NOON_STREAM")
PRIME_TIME = GetEnvironmentVariable("PRIME_TIME_STREAM")
AFTER_DARK = GetEnvironmentVariable("AFTER_DARK_STREAM")
CBB_STREAM_CHANNEL = GetEnvironmentVariable("CBB_STREAM")
TBS_STREAM_CHANNEL = GetEnvironmentVariable("TBS_STREAM")
ESPN_STREAM_CHANNEL = GetEnvironmentVariable("ESPN_STREAM")
ESPN2_STREAM_CHANNEL = GetEnvironmentVariable("ESPN_2_STREAM")
TNT_STREAM_CHANNEL = GetEnvironmentVariable("TNT_STREAM")
NBA_LIVE_STREAM_CHANNEL = GetEnvironmentVariable("NBA_LIVE_STREAM")
NBA_PRIME_STREAM_CHANNEL = GetEnvironmentVariable("NBA_PRIME_STREAM")
NBA_HBO_STREAM_CHANNEL = GetEnvironmentVariable("NBA_HBO_STREAM")
INT_STREAM_CHANNEL = GetEnvironmentVariable("INT_STREAM")
FCS_STREAM_CHANNEL = GetEnvironmentVariable("FCS_STREAM")
NFL_STREAM_CHANNEL = GetEnvironmentVariable("NFL_STREAM")
ADMIN_ROLE = GetEnvironmentVariable("ADMIN_ROLE")
MOD_ROLE = GetEnvironmentVariable("MOD_ROLE")
STAFF_ROLE = GetEnvironmentVariable("STAFF_ROLE")
BROADCASTER_ROLE = GetEnvironmentVariable("BROADCASTER_ROLE")
RINK_STREAM_CHANNEL = GetEnvironmentVariable("THE_RINK")
CBC_STREAM_CHANNEL = GetEnvironmentVariable("CBC_STREAM")
TSN_STREAM_CHANNEL = GetEnvironmentVariable("TSN_STREAM")
COLLEGE_U_STREAM_CHANNEL = GetEnvironmentVariable("COLLEGE_U_STREAM")
POLAR_STREAM_CHANNEL = GetEnvironmentVariable("POLAR_SPORTS_NET_STREAM")
FROZEN_STREAM_CHANNEL = GetEnvironmentVariable("FROZEN_FRENZY_STREAM")
LAX_STREAM_CHANNEL = int(os.getenv("LAX_STREAM", 0))
# One channel per SimCLAX network. Any that is unset falls back to LAX_STREAM (the test channel).
LAX_NETWORK_CHANNELS = {
    "flo": int(os.getenv("LAX_FLO_STREAM", 0)),
    "laxtv": int(os.getenv("LAX_LAXTV_STREAM", 0)),
    "abc": int(os.getenv("LAX_ABC_STREAM", 0)),
    "espnu": int(os.getenv("LAX_ESPNU_STREAM", 0)),
}