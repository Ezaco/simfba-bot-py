import asyncio
import time
from discord import app_commands
import api_requests

TEAM_CACHE_SECONDS = 600
team_cache = {"fetched_at": 0.0, "teams": []}

async def get_lax_teams():
    if not team_cache["teams"] or time.monotonic() - team_cache["fetched_at"] > TEAM_CACHE_SECONDS:
        teams = await asyncio.to_thread(api_requests.GetLaxTeams)
        if teams:
            team_cache["teams"] = teams
            team_cache["fetched_at"] = time.monotonic()
    return team_cache["teams"]

def lax_team_label(team):
    return f"{team['name']} {team['nickname']}".strip()

def find_lax_team(teams, query):
    query = query.strip().lower()
    for team in teams:
        names = [str(team["id"]), (team["abbreviation"] or ""), team["name"], lax_team_label(team)]
        if query in [name.lower() for name in names if name]:
            return team
    return None

async def lax_team_choices(current):
    current = current.strip().lower()
    matches = []
    for team in await get_lax_teams():
        haystack = f"{lax_team_label(team)} {team['abbreviation'] or ''}".lower()
        if current in haystack:
            matches.append(app_commands.Choice(name=lax_team_label(team)[:100], value=str(team["id"])))
        if len(matches) == 25:
            break
    return matches
