import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

fba_url = "https://simfba.azurewebsites.net/api/"
test_url = "http://localhost:5001/api/"
bba_test_url = "http://localhost:8081/api/"
bba_url = "https://simnba.azurewebsites.net/api/"
hck_test_url = "http://localhost:8080/api/"
hck_url = "https://simhck-hqd2bme9gse5d7g9.westus-01.azurewebsites.net/api/"
bas_url = "https://simbaseball.afwh.app/api/v1/"
lax_url = os.getenv("SIMLAX_API_URL", "https://3.17.19.90/api/v1").rstrip("/")
lax_origin = lax_url.removesuffix("/api/v1")
# bba_url = bba_test_url

def _without_hidden_ratings(data):
    """College ratings are hidden from users, so only letter grades may reach a Discord message.

    Drops every raw "ratings" block and every numeric "overall" the moment a SimLAX response arrives,
    so no embed can display them, even by mistake. Letter grades (strings) are kept.
    """
    if isinstance(data, dict):
        return {key: _without_hidden_ratings(value) for key, value in data.items()
                if key != "ratings" and not (key == "overall" and isinstance(value, (int, float)) and not isinstance(value, bool))}
    if isinstance(data, list):
        return [_without_hidden_ratings(item) for item in data]
    return data

def GetLaxLogoUrl(file_name):
    if not file_name:
        return ""
    return f"{lax_origin}/static/team-logos/{requests.utils.quote(file_name)}"

def GetLaxWeekGames(season=None, week=None):
    params = {}
    if season is not None:
        params["season"] = season
    if week is not None:
        params["week"] = week
    res = requests.get(f"{lax_url}/stream/week", params=params, headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=30)
    if res.status_code == 200:
        return res.json()
    return False

def GetLaxTeams():
    res = requests.get(f"{lax_url}/stream/teams", headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=30)
    if res.status_code == 200:
        return res.json()
    return False

def GetLaxPlayer(player_id):
    res = requests.get(f"{lax_url}/stream/players/{player_id}", headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=30)
    if res.status_code == 200:
        return _without_hidden_ratings(res.json())
    return False

def GetLaxClassRankings(limit=25):
    res = requests.get(f"{lax_url}/stream/recruiting/rankings", params={"limit": limit}, headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=60)
    if res.status_code == 200:
        return res.json()
    return False

def GetLaxVersus(team_id, other_team_id):
    res = requests.get(f"{lax_url}/stream/teams/{team_id}/versus/{other_team_id}", headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=30)
    if res.status_code == 200:
        return res.json()
    return False

def GetLaxCroot(recruit_id):
    res = requests.get(f"{lax_url}/stream/recruits/{recruit_id}", headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=30)
    if res.status_code == 200:
        return _without_hidden_ratings(res.json())
    return False

def GetLaxClass(team_id):
    res = requests.get(f"{lax_url}/stream/teams/{team_id}/class", headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=30)
    if res.status_code == 200:
        return _without_hidden_ratings(res.json())
    return False

def GetLaxPlayerStats(player_id):
    res = requests.get(f"{lax_url}/stream/players/{player_id}/stats", headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=30)
    if res.status_code == 200:
        return res.json()
    return False

def GetLaxPlayerYears(player_ids):
    """Class year (1 = Fr ... 5 = 5th) for each player id, looked up in parallel. Players that fail to load are left out."""
    from concurrent.futures import ThreadPoolExecutor
    ids = list(player_ids)
    if not ids:
        return {}

    def lookup(player_id):
        # A year is a nicety: a timeout or error on one player must never break the team card.
        try:
            return GetLaxPlayer(player_id)
        except Exception as e:
            print(f"Could not look up the class year for SimLAX player {player_id}: {e}")
            return False

    with ThreadPoolExecutor(max_workers=min(len(ids), 8)) as pool:
        results = list(pool.map(lookup, ids))
    return {player_id: data["player"]["year"] for player_id, data in zip(ids, results) if data}

def GetLaxPlayers(first_name, last_name, team_id):
    res = requests.get(f"{lax_url}/stream/players", params={"first_name": first_name, "last_name": last_name, "team_id": team_id}, headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=30)
    if res.status_code == 200:
        return _without_hidden_ratings(res.json())
    return False

def GetLaxTeamProfile(team_id):
    res = requests.get(f"{lax_url}/stream/teams/{team_id}", headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=30)
    if res.status_code == 200:
        return _without_hidden_ratings(res.json())
    return False

def RegisterLaxTeam(team_id, discord_mention):
    res = requests.put(f"{lax_url}/stream/teams/{team_id}/discord", json={"discordMention": discord_mention}, headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=30)
    return res.status_code == 200

def GetLaxGame(game_id):
    res = requests.get(f"{lax_url}/stream/games/{game_id}", headers={"X-Bot-Key": os.getenv("SIMLAX_BOT_KEY", "")}, timeout=60)
    if res.status_code == 200:
        return res.json()
    return False

def GetBaseballTeam(team):
    res = requests.get(f"{bas_url}teams/{team}")
    if res.status_code == 200:
        return res.json()
    return False

def GetBaseballPlayer_id(id):
    res = requests.get(f"{bas_url}stats/player/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetBaseballPlayer_id2(id):
    res = requests.get(f"{bas_url}scouting/player/{id}?org_id=6&league_year_id=1")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeBaseballClass(year, id):
    res = requests.get(f"{bas_url}recruiting/commitments?league_year_id={year}&org_id={id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetBaseballCroot(id, year):
    res = requests.get(f"{bas_url}recruiting/player/{id}?league_year_id={year}&viewing_org_id=142")
    if res.status_code == 200:
        return res.json()
    return False

def GetBaseballCrootCommitted(id, year, org=142):
    res = requests.get(f"{bas_url}scouting/player/{id}?league_year_id={year}&org_id={org}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeBasketballTeam(id):
    res = requests.get(f"{bba_url}ds/cbb/team/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeBasketballPlayer(first_name, last_name, id):
    res = requests.get(f"{bba_url}ds/cbb/player/name/{first_name}/{last_name}/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeBasketballPlayer_id(id):
    res = requests.get(f"{bba_url}ds/cbb/player/id/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetNBABasketballPlayer_id(id):
    res = requests.get(f"{bba_url}ds/nba/player/id/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetNBABasketballTeam(id):
    res = requests.get(f"{bba_url}ds/nba/team/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetNBABasketballPlayer(first_name, last_name, id):
    res = requests.get(f"{bba_url}ds/nba/player/name/{first_name}/{last_name}/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def CompareTwoNBATeams(t1, t2):
    res = requests.get(f"{bba_url}ds/nba/flex/{t1}/{t2}")
    if res.status_code == 200:
        return res.json()
    return False

def GetAllCBBMatches():
    res = requests.get(f"{bba_url}match/season/3")
    if res.status_code == 200:
        return res.json()
    return False

def CompareTwoCBBTeams(t1, t2):
    res = requests.get(f"{bba_url}ds/cbb/flex/{t1}/{t2}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeFootballPlayer(first_name, last_name, id):
    res = requests.get(f"{fba_url}ds/cfb/player/name/{first_name}/{last_name}/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeFootballPlayer_id(id):
    res = requests.get(f"{fba_url}ds/cfb/player/id/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeFootballPlayerCareer_id(id):
    res = requests.get(f"{fba_url}ds/college/player/careerstats/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetNFLFootballPlayer(first_name, last_name, id):
    res = requests.get(f"{fba_url}ds/nfl/player/name/{first_name}/{last_name}/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetNFLFootballPlayer_id(id):
    res = requests.get(f"{fba_url}ds/nfl/player/id/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetNFLFootballPlayerCareer_id(id):
    res = requests.get(f"{fba_url}ds/nfl/player/careerstats/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeFootballPlayerIndStats(first_name, last_name, id, week):
    res = requests.get(f"{fba_url}ds/cfb/player/indstats/{first_name}/{last_name}/{id}/{week}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeFootballPlayerSeasonStats(first_name, last_name, id):
    res = requests.get(f"{fba_url}ds/cfb/player/seasonsstats/{first_name}/{last_name}/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeFootballCroot(id):
    res = requests.get(f"{fba_url}ds/cfb/croot/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeFootballCrootName(first_name, last_name):
    res = requests.get(f"{fba_url}ds/cfb/croot/name/{first_name}/{last_name}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeFootballCrootingClass(id):
    res = requests.get(f"{fba_url}ds/cfb/croots/class/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeBasketballCroot(id):
    res = requests.get(f"{bba_url}ds/cbb/croot/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeBasketballCrootName(first_name, last_name):
    res = requests.get(f"{bba_url}ds/cbb/croot/name/{first_name}/{last_name}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeBasketballCrootingClass(id):
    res = requests.get(f"{bba_url}ds/cbb/croots/class/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeFootballConfStandings(id):
    res = requests.get(f"{fba_url}ds/cfb/conference/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeBasketballConfStandings(id):
    res = requests.get(f"{bba_url}ds/cbb/conf/standings/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetNBABasketballConfStandings(id):
    res = requests.get(f"{bba_url}ds/nba/conf/standings/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeFootballTeam(id):
    res = requests.get(f"{fba_url}ds/cfb/team/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def CompareTwoCFBTeams(t1, t2):
    res = requests.get(f"{fba_url}ds/cfb/flex/{t1}/{t2}")
    if res.status_code == 200:
        return res.json()
    return False

def GetNFLFootballConfStandings(id):
    res = requests.get(f"{fba_url}ds/nfl/conference/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetNFLFootballDiviStandings(id):
    res = requests.get(f"{fba_url}ds/nfl/division/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetNFLFootballTeam(id):
    res = requests.get(f"{fba_url}teams/nfl/roster/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def CompareTwoNFLTeams(t1, t2):
    res = requests.get(f"{fba_url}ds/nfl/flex/{t1}/{t2}")
    if res.status_code == 200:
        return res.json()
    return False

def StreamFootballGames(league, timeslot, isNFL):
    req_url = ""
    if isNFL == False:
        req_url = f"{fba_url}ds/cfb/{league}/stream/{timeslot}/"
    else:
        req_url = f"{fba_url}ds/nfl/league/stream/{timeslot}/"
    res = requests.get(f"{req_url}")
    if res.status_code == 200:
        return res.json()
    return False

def StreamBasketballGames(isPro, streamType):
    req_url = ""
    if isPro == False:
        req_url = f"{bba_url}ds/cbb/stream/{streamType}/"
    else:
        req_url = f"{bba_url}ds/nba/stream/{streamType}/"
    res = requests.get(f"{req_url}")
    if res.status_code == 200:
        return res.json()
    return False

def StreamHockeyGames(isPro, streamType):
    req_url = ""
    if isPro == False:
        req_url = f"{hck_url}ds/chl/stream/{streamType}/"
    else:
        req_url = f"{hck_url}ds/phl/stream/{streamType}/"
    res = requests.get(f"{req_url}")
    if res.status_code == 200:
        return res.json()
    return False

def RevealBBAGameResultsOnInterface(isPro, gameID):
    req_url = ""
    if isPro == False:
        req_url = f"{bba_url}ds/cbb/reveal/results/{gameID}/"
    else:
        req_url = f"{bba_url}ds/nba/reveal/results/{gameID}/"
    res = requests.get(f"{req_url}")
    if res.status_code == 200:
        return res.json()
    return False

def RevealHCKGameResultsOnInterface(isPro, gameID):
    req_url = ""
    if isPro == False:
        req_url = f"{hck_url}ds/chl/reveal/results/{gameID}/"
    else:
        req_url = f"{hck_url}ds/phl/reveal/results/{gameID}/"
    res = requests.get(f"{req_url}")
    if res.status_code == 200:
        return res.json()
    return False

def RevealBBGameResultsOnInterface(isPro, gameID):
    req_url = ""
    if isPro == False:
        req_url = f"{bba_url}ds/cbb/reveal/results/{gameID}/"
    else:
        req_url = f"{bba_url}ds/nba/reveal/results/{gameID}/"
    res = requests.get(f"{req_url}")
    if res.status_code == 200:
        if res.content:
            return res.json()
        return True
    return False

def RevealFBGameResultsOnInterface(isPro, gameID):
    req_url = ""
    if isPro == False:
        req_url = f"{fba_url}ds/cfb/reveal/results/{gameID}/"
    else:
        req_url = f"{fba_url}ds/nfl/reveal/results/{gameID}/"
    res = requests.get(f"{req_url}")
    if res.status_code == 200:
        if res.content:
            return res.json()
        return True
    return False

def RegisterFBTeam(isNFL, team_id, user):
    req_url = ""
    if isNFL == False:
        req_url = f"{fba_url}ds/cfb/assign/discord/{team_id}/{user}"
    else:
        req_url = f"{fba_url}ds/nfl/assign/discord/{team_id}/{user}"
    res = requests.get(f"{req_url}")
    if res.status_code == 200:
        return True
    return False

def RegisterBBTeam(isNBA, team_id, user, username):
    req_url = ""
    if isNBA == False:
        req_url = f"{bba_url}ds/cbb/assign/discord/{team_id}/{user}"
    else:
        req_url = f"{bba_url}ds/nba/assign/discord/{team_id}/{user}/{username}"
    res = requests.get(f"{req_url}")
    if res.status_code == 200:
        return True
    return False

def RegisterHCTeam(isPHL, team_id, user):
    req_url = ""
    if isPHL == False:
        req_url = f"{hck_url}ds/chl/assign/discord/{team_id}/{user}"
    else:
        req_url = f"{hck_url}ds/phl/assign/discord/{team_id}/{user}"
    res = requests.get(f"{req_url}")
    if res.status_code == 200:
        return True
    return False

def CompareTwoCHLTeams(t1, t2):
    res = requests.get(f"{hck_url}ds/chl/flex/{t1}/{t2}")
    if res.status_code == 200:
        return res.json()
    return False

def CompareTwoPHLTeams(t1, t2):
    res = requests.get(f"{hck_url}ds/phl/flex/{t1}/{t2}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeHockeyTeam(id):
    res = requests.get(f"{hck_url}ds/chl/team/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetPHLHockeyTeam(id):
    res = requests.get(f"{hck_url}ds/phl/team/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeHockeyPlayer(first_name, last_name, id):
    res = requests.get(f"{hck_url}ds/chl/player/name/{first_name}/{last_name}/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeHockeyPlayer_id(id):
    res = requests.get(f"{hck_url}ds/chl/player/id/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetPHLHockeyPlayer(first_name, last_name, id):
    res = requests.get(f"{hck_url}ds/phl/player/name/{first_name}/{last_name}/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetPHLHockeyPlayer_id(id):
    res = requests.get(f"{hck_url}ds/phl/player/id/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeHockeyCroot(id):
    res = requests.get(f"{hck_url}ds/chl/croot/{id}")
    if res.status_code == 200:
        return res.json()
    return False

def GetCollegeHockeyCrootingClass(id):
    res = requests.get(f"{hck_url}ds/chl/croots/class/{id}")
    if res.status_code == 200:
        return res.json()
    return False
