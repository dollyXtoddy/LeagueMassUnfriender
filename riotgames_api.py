#!/usr/bin/env python3

import base64
import psutil
import os
import requests
from urllib3 import disable_warnings
import configparser

disable_warnings()


def get_process_by_name(process_name):
    while True:
        for proc in psutil.process_iter():
            try:
                if process_name in proc.name():
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


# http://lcu.vivide.re/
# https://github.com/Pupix/rift-explorer
class LeagueOfLegendsClientAPI(object):
    def __init__(self):
        self.process = get_process_by_name("LeagueClientUx")

        self.lockfile = open(os.path.join(self.process.cwd(), "lockfile"), 'r').read()

        split = self.lockfile.split(":")

        self.process_name = split[0]
        self.process_id = split[1]
        self.port = split[2]
        self.password = str(base64.b64encode(("riot:" + split[3]).encode("utf-8")), "utf-8")
        self.protocol = split[4]

    def get(self, path):
        return requests.get(
            self.protocol + "://127.0.0.1:" + self.port + path,
            verify=False,
            headers={"Authorization": "Basic " + self.password}
        ).json()

    def post(self, path, json=None):
        return requests.post(
            self.protocol + "://127.0.0.1:" + self.port + path,
            verify=False,
            headers={"Authorization": "Basic " + self.password},
            json=json
        )

    def put(self, path, json=None):
        return requests.put(
            self.protocol + "://127.0.0.1:" + self.port + path,
            verify=False,
            headers={"Authorization": "Basic " + self.password},
            json=json
        )

    def delete(self, path, json=None):
        return requests.delete(
            self.protocol + "://127.0.0.1:" + self.port + path,
            verify=False,
            headers={"Authorization": "Basic " + self.password},
            json=json
        )

    def head(self, path, json=None):
        return requests.head(
            self.protocol + "://127.0.0.1:" + self.port + path,
            verify=False,
            headers={"Authorization": "Basic " + self.password},
            json=json
        )

    def patch(self, path, json=None):
        return requests.patch(
            self.protocol + "://127.0.0.1:" + self.port + path,
            verify=False,
            headers={"Authorization": "Basic " + self.password},
            json=json
        )


# https://developer.riotgames.com/apis
class RiotGamesAPIS(object):
    def __init__(self, api_key, region, regional):
        self.api_key = api_key
        self.region = region
        self.regional = regional

    def get(self, path):
        return requests.get(
            "https://" + self.region + ".api.riotgames.com" + path,
            verify=False,
            headers={"X-Riot-Token": self.api_key}
        ).json()

    def post(self, path, json=None):
        return requests.post(
            "https://" + self.region + ".api.riotgames.com" + path,
            verify=False,
            headers={"X-Riot-Token": self.api_key},
            json=json
        )

    def put(self, path, json=None):
        return requests.put(
            "https://" + self.region + ".api.riotgames.com" + path,
            verify=False,
            headers={"X-Riot-Token": self.api_key},
            json=json
        )

    # account-v1
    def account_v1_accounts_by_puuid(self, puuid):
        return self.get("/riot/account/v1/accounts/by-puuid/" + puuid)

    def account_v1_accounts_by_riot_id(self, gameName, tagLine):
        return self.get("/riot/account/v1/accounts/by-riot-id/" + gameName + "/" + tagLine)

    def account_v1_active_shards_by_game(self, game, puuid):
        return self.get("/riot/account/v1/active-shards/by-game/" + game + "/by-puuid/" + puuid)

    # champion-mastery-v4
    def champion_mastery_v4_champion_masteries_by_summoner(self, encryptedSummonerId):
        return self.get("/lol/champion-mastery/v4/champion-masteries/by-summoner/" + encryptedSummonerId)

    def champion_mastery_v4_champion_masteries_by_summoner_by_champion(self, encryptedSummonerId, championId):
        return self.get(
            "/lol/champion-mastery/v4/champion-masteries/by-summoner/" + encryptedSummonerId + "/by-champion/" + championId)

    def champion_mastery_v4_scores_by_summoner(self, encryptedSummonerId):
        return self.get("/lol/champion-mastery/v4/scores/by-summoner/" + encryptedSummonerId)

    # champion-v3
    def champion_v3_champion_rotations(self):
        return self.get("/lol/platform/v3/champion-rotations")

    # clash-v1
    def clash_v1_players_by_summoner(self, summonerId):
        return self.get("/lol/clash/v1/players/by-summoner/" + summonerId)

    def clash_v1_teams(self, teamId):
        return self.get("/lol/clash/v1/teams/" + teamId)

    def clash_v1_tournaments(self):
        return self.get("/lol/clash/v1/tournaments")

    def clash_v1_tournaments_by_team(self, teamId):
        return self.get("/lol/clash/v1/tournaments/by-team/" + teamId)

    def clash_v1_tournaments_by_tournamentId(self, tournamentId):
        return self.get("/lol/clash/v1/tournaments/" + tournamentId)

    # league-exp-v4
    def cleague_exp_v4_entries(self, queue, tier, division):
        return self.get("/lol/league-exp/v4/entries/" + queue + "/" + tier + "/" + division)

    # league-v4
    def league_v4_challengerleagues_by_queue(self, queue):
        return self.get("/lol/league/v4/challengerleagues/by-queue/" + queue)

    def league_v4_entries_by_summoner(self, encryptedSummonerId):
        return self.get("/lol/league/v4/entries/by-summoner/" + encryptedSummonerId)

    def league_v4_entries(self, queue, tier, division):
        return self.get("/lol/league/v4/entries/" + queue + "/" + tier + "/" + division)

    def league_v4_grandmasterleagues_by_queue(self, queue):
        return self.get("/lol/league/v4/grandmasterleagues/by-queue/" + queue)

    def league_v4_leagues(self, leagueId):
        return self.get("/lol/league/v4/leagues/" + leagueId)

    def league_v4_masterleagues_by_queue(self, queue):
        return self.get("/lol/league/v4/masterleagues/by-queue/" + queue)

    # lol-status-v3
    def lol_status_v3_shard_data(self):
        return self.get("/lol/status/v3/shard-data")

    # lor-match-v1
    def lor_match_v1_matches_by_puuid(self, puuid):
        return self.get("/lor/match/v1/matches/by-puuid/" + puuid + "/ids")

    def lor_match_v1_matches(self, matchId):
        return self.get("/lor/match/v1/matches/" + matchId)

    # lor-ranked-v1
    def lor_ranked_v1_leaderboards(self):
        return self.get("/lor/ranked/v1/leaderboards")

    # match-v4
    def match_v4_matches(self, matchId):
        return self.get("/lol/match/v4/matches/" + matchId)

    def match_v4_matchlists_by_account(self, encryptedAccountId):
        return self.get("/lol/match/v4/matchlists/by-account/" + encryptedAccountId)

    def match_v4_timelines_by_match(self, matchId):
        return self.get("/lol/match/v4/timelines/by-match/" + matchId)

    def match_v4_matches_by_tournament_code(self, tournamentCode):
        return self.get("/lol/match/v4/matches/by-tournament-code/" + tournamentCode + "/ids")

    def match_v4_matches_by_match_by_tournament_code(self, matchId, tournamentCode):
        return self.get("/lol/match/v4/matches/" + matchId + "/by-tournament-code/" + tournamentCode)

    # spectator-v4
    def spectator_v4_active_game_by_summoner(self, encryptedSummonerId):
        return self.get("/lol/spectator/v4/active-games/by-summoner/" + encryptedSummonerId)

    def spectator_v4_featured_games(self):
        return self.get("/lol/spectator/v4/featured-games")

    # summoner-v4
    def summoner_v4_summoners_by_account(self, encryptedAccountId):
        return self.get("/lol/summoner/v4/summoners/by-account/" + encryptedAccountId)

    def summoner_v4_summoners_by_name(self, summonerName):
        return self.get("/lol/summoner/v4/summoners/by-name/" + summonerName)

    def summoner_v4_summoners_by_puuid(self, encryptedPUUID):
        return self.get("/lol/summoner/v4/summoners/by-puuid/" + encryptedPUUID)

    def summoner_v4_summoners(self, encryptedSummonerId):
        return self.get("/lol/summoner/v4/summoners/" + encryptedSummonerId)

    # tft-league-v1
    def tft_league_v1_challenger(self):
        return self.get("/tft/league/v1/challenger")

    def tft_league_v1_entries_by_summoner(self, encryptedSummonerId):
        return self.get("/tft/league/v1/entries/by-summoner/" + encryptedSummonerId)

    def tft_league_v1_entries(self, tier, division):
        return self.get("/tft/league/v1/entries/" + tier + "/" + division)

    def tft_league_v1_grandmaster(self):
        return self.get("/tft/league/v1/grandmaster")

    def tft_league_v1_leagues(self, leagueId):
        return self.get("/tft/league/v1/leagues/" + leagueId)

    def tft_league_v1_master(self):
        return self.get("/tft/league/v1/master")

    # tft-match-v1
    def tft_match_v1_matches_by_puuid(self, puuid):
        return self.get("/tft/match/v1/matches/by-puuid/" + puuid + "/ids")

    def tft_match_v1_matches(self, matchId):
        return self.get("/tft/match/v1/matches/" + matchId)

    # tft-summoner-v1
    def tft_summoner_v1_summoners_by_account(self, encryptedAccountId):
        return self.get("/tft/summoner/v1/summoners/by-account/" + encryptedAccountId)

    def tft_summoner_v1_summoners_by_name(self, summonerName):
        return self.get("/tft/summoner/v1/summoners/by-name/" + summonerName)

    def tft_summoner_v1_summoners_by_puuid(self, encryptedPUUID):
        return self.get("/tft/summoner/v1/summoners/by-puuid/" + encryptedPUUID)

    def tft_summoner_v1_summoners(self, encryptedSummonerId):
        return self.get("/tft/summoner/v1/summoners/" + encryptedSummonerId)

    # third-party-code-v4
    def third_party_code_v4_by_summoner(self, encryptedSummonerId):
        return self.get("/lol/platform/v4/third-party-code/by-summoner/" + encryptedSummonerId)

    # tournament-stub-v4
    def tournament_stub_v4_codes(self):
        return self.get("/lol/tournament-stub/v4/codes")

    def tournament_stub_v4_lobby_events_by_code(self, tournamentCode):
        return self.get("/lol/tournament-stub/v4/lobby-events/by-code/" + tournamentCode)

    def tournament_stub_v4_providers(self):
        return self.get("/lol/tournament-stub/v4/providers")

    def tournament_stub_v4_tournaments(self):
        return self.get("/lol/tournament-stub/v4/tournaments")

    # tournament-v4
    def tournament_v4_post_codes(self, json):
        return self.post("/lol/tournament/v4/codes", json)

    def tournament_v4_get_codes(self, tournamentCode):
        return self.get("/lol/tournament/v4/codes/" + tournamentCode)

    def tournament_v4_put_codes(self, tournamentCode, json):
        return self.put("/lol/tournament/v4/codes/" + tournamentCode, json)

    def tournament_v4_lobby_events_by_code(self, tournamentCode):
        return self.get("/lol/tournament/v4/lobby-events/by-code/" + tournamentCode)

    def tournament_v4_providers(self, json):
        return self.post("/lol/tournament/v4/providers", json)

    def tournament_v4_tournaments(self, json):
        return self.post("/lol/tournament/v4/tournaments", json)

    # val-content-v1
    def val_content_v1_contents(self):
        return self.get("/val/content/v1/contents")

    # val-match-v1
    def val_match_v1_matches(self, matchId):
        return self.get("/val/match/v1/matches/" + matchId)

    def val_match_v1_matchlists_by_puuid(self, puuid):
        return self.get("/val/match/v1/matchlists/by-puuid/" + puuid)

    def val_match_v1_recent_matches_by_queue(self, queue):
        return self.get("/val/match/v1/recent-matches/by-queue/" + queue)


# https://developer.riotgames.com/docs/lol
class LeagueOfLegendsExternalAPI(object):
    def __init__(self, language="en_US", version=None):
        self.language = language
        self.url1 = "http://static.developer.riotgames.com"
        self.url2 = "http://ddragon.leagueoflegends.com"
        if version:
            self.version = version
        else:
            self.version = requests.get(self.url2 + "/api/versions.json").json()[0]

    def get_seasons(self):
        return requests.get(self.url1 + "/docs/lol/seasons.json").json()

    def get_queues(self):
        return requests.get(self.url1 + "/docs/lol/queues.json").json()

    def get_maps(self):
        return requests.get(self.url1 + "/docs/lol/maps.json").json()

    def get_gameModes(self):
        return requests.get(self.url1 + "/docs/lol/gameModes.json").json()

    def get_gameTypes(self):
        return requests.get(self.url1 + "/docs/lol/gameTypes.json").json()

    def get_ranked_emblems(self):
        return requests.get(self.url1 + "/docs/lol/ranked-emblems.zip").raw

    def get_ranked_positions(self):
        return requests.get(self.url1 + "/docs/lol/ranked-positions.zip").raw

    # OLD
    def get_old_tier_icons(self):
        return requests.get("http://s3-us-west-1.amazonaws.com/riot-developer-portal/assets/tier-icons.zip").raw

    # ###

    def get_Data_Dragon(self):
        return requests.get(self.url2 + "/cdn/dragontail-" + self.version + ".tgz").raw

    def get_versions(self):
        return requests.get(self.url2 + "/api/versions.json").json()

    def get_realms(self, region="na"):
        return requests.get(self.url2 + "/realms/" + region + ".json").json()

    def get_languages(self):
        return requests.get(self.url2 + "/cdn/languages.json").json()

    def get_champions(self):
        return requests.get(self.url2 + "/cdn/" + self.version + "/data/" + self.language + "/champion.json").json()

    def get_champion(self, champion):
        return requests.get(
            self.url2 + "/cdn/" + self.version + "/data/" + self.language + "/champion/" + champion + ".json").json()

    def get_Champion_Splash_Assets(self, champion, skin_id=0):
        return requests.get(
            self.url2 + "/cdn/" + self.version + "/img/champion/splash/" + champion + '_' + str(
                skin_id) + ".png").content

    def get_Champion_Loading_Screen_Assets(self, champion, skin_id=0):
        return requests.get(
            self.url2 + "/cdn/" + self.version + "/img/champion/loading/" + champion + '_' + str(
                skin_id) + ".png").content

    def get_Champion_Square_Assets(self, champion):
        return requests.get(self.url2 + "/cdn/" + self.version + "/img/champion/" + champion + ".png").content

    def get_Champion_Passive_Assets(self, champion):
        return requests.get(self.url2 + "/cdn/" + self.version + "/img/passive/" + champion + "_P.png").content

    def get_Champion_Ability_Assets(self, spell_key):
        return requests.get(self.url2 + "/cdn/" + self.version + "/img/spell/" + spell_key + ".png").content

    def get_items(self):
        return requests.get(self.url2 + "/cdn/" + self.version + "/data/" + self.language + "/item.json").json()

    def get_Item_Assets(self, item_id):
        return requests.get(self.url2 + "/cdn/" + self.version + "/img/item/" + str(item_id) + ".png").content

    def get_summoner_spells(self):
        return requests.get(self.url2 + "/cdn/" + self.version + "/data/" + self.language + "/summoner.json").json()

    def get_spell_img(self, spell):
        return requests.get(self.url2 + "/cdn/" + self.version + "/img/spell/" + spell + ".png").content

    def get_profile_icons(self):
        return requests.get(self.url2 + "/cdn/" + self.version + "/data/" + self.language + "/profileicon.json").json()

    def get_profile_icon_img(self, profileicon):
        return requests.get(self.url2 + "/cdn/" + self.version + "/img/profileicon/" + profileicon + ".png").content

    def get_Minimaps(self, map):
        return requests.get(self.url2 + "/cdn/" + self.version + "/img/map/" + map + ".png").content

    def get_Sprites(self, sprit):
        return requests.get(self.url2 + "/cdn/" + self.version + "/img/sprite/" + sprit + ".png").content

    # OLD
    def get_old_scoreboard_icons(self, type):  # (version 5.5.1)
        return requests.get(self.url2 + "/cdn/" + self.version + "/img/ui/" + type + ".png").content

    # ###

    # Custom
    def get_champion_names(self):
        champions = []
        for champ in \
                requests.get(self.url2 + "/cdn/" + self.version + "/data/" + self.language + "/champion.json").json()[
                    "data"]:
            champions.append(champ)
        return champions


# https://developer.riotgames.com/docs/lol
class LeagueOfLegendsGameClientAPI(object):
    def __init__(self):
        self.port = 2999
        self.clientPath = get_process_by_name("LeagueClientUx").cwd()

    def get(self, path):
        return requests.get(
            "https://127.0.0.1:" + str(self.port) + path,
            verify=False
        ).json()

    def post(self, path, json=None):
        return requests.post(
            "https://127.0.0.1:" + str(self.port) + path,
            verify=False,
            json=json
        )

    # Swagger
    def get_swagger_v2(self):
        return self.get("/swagger/v2/swagger.json")

    def get_openapi_v3(self):
        return self.get("/swagger/v3/openapi.json")

    # Live Client json API
    def get_liveclientdata_allgamedata(self):
        return self.get("/liveclientdata/allgamedata")

    def get_liveclientdata_activeplayer(self):
        return self.get("/liveclientdata/activeplayer")

    def get_liveclientdata_activeplayername(self):
        return self.get("/liveclientdata/activeplayername")

    def get_liveclientdata_activeplayerabilities(self):
        return self.get("/liveclientdata/activeplayerabilities")

    def get_liveclientdata_activeplayerrunes(self):
        return self.get("/liveclientdata/activeplayerrunes")

    def get_liveclientdata_playerlist(self):
        return self.get("/liveclientdata/playerlist")

    def get_liveclientdata_playerscores(self, summoner_name):
        return self.get("/liveclientdata/playerscores?summonerName=" + summoner_name)

    def get_liveclientdata_playermainrunes(self, summoner_name):
        return self.get("/liveclientdata/playermainrunes?summonerName=" + summoner_name)

    def get_liveclientdata_playeritems(self, summoner_name):
        return self.get("/liveclientdata/playeritems?summonerName=" + summoner_name)

    def get_liveclientdata_eventdata(self):
        return self.get("/liveclientdata/eventdata")

    def get_liveclientdata_gamestats(self):
        return self.get("/liveclientdata/gamestats")

    # Replay API
    def get_replay_api_game(self):
        return self.get("/replay/game")

    def get_replay_api_playback(self):
        return self.get("/replay/playback")

    def set_replay_api_playback(self, json):
        self.post("/replay/playback", json)

    def get_replay_api_render(self):
        return self.get("/replay/render")

    def set_replay_api_render(self, json):
        self.post("/replay/render", json)

    def get_replay_api_recording(self):
        return self.get("/replay/recording")

    def set_replay_api_recording(self, json):
        self.post("/replay/recording", json)

    def get_replay_api_sequence(self):
        return self.get("/replay/sequence")

    def set_replay_api_sequence(self, json):
        self.post("/replay/sequence", json)

    # Custom
    def get_game_cfg(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(self.clientPath, "Config", "game.cfg"))
        return config

    def save_game_cfg(self, config):
        config.write(open(os.path.join(self.clientPath, "Config", "game.cfg"), 'w'))

    def enable_replay_api(self):
        config = self.get_game_cfg()
        config["General"]['EnableReplayApi'] = '1'
        self.save_game_cfg(config)

    def disable_replay_api(self):
        config = self.get_game_cfg()
        config["General"]['EnableReplayApi'] = '0'
        self.save_game_cfg(config)
