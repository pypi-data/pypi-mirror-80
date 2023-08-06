#  Copyright (c) 2020.
#  The copyright lies with Timo Hirsch-Hoffmann, the further use is only permitted with reference to source

import urllib.request

from RiotGames.Summoner.Account import SummonerAccount

from RiotGames.API.RiotApi import RiotApi


class Summoner(RiotApi):
    __by_account_id_url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{}?api_key={}"
    __by_name_url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"
    __by_puuid_url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}?api_key={}"
    __by_summoner_id_url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/{}?api_key={}"

    def __init__(self, apikey: str):
        """

        :param apikey:
        """
        super().__init__(apikey)
        self.__super = super()

    def by_account_id(self, summoner_account_id: str, region: str):
        """

        :param summoner_account_id:
        :param region:
        :return:
        """
        response = bytes(
            urllib.request.urlopen(
                self.__by_account_id_url.format(region, summoner_account_id, super()._get_key())).read()).decode()
        data = eval(response)

        return SummonerAccount(data["id"], data["accountId"], data["puuid"], data["name"], data["profileIconId"],
                               data["revisionDate"], data["summonerLevel"])

    def by_name(self, summoner_name: str, region: str):
        """

        :param summoner_name:
        :param region:
        :return:
        """
        summoner_name = summoner_name.replace(" ", "%20")

        response = bytes(
            urllib.request.urlopen(
                self.__by_name_url.format(region, summoner_name, super()._get_key())).read()).decode()
        data = eval(response)

        return SummonerAccount(data["id"], data["accountId"], data["puuid"], data["name"], data["profileIconId"],
                               data["revisionDate"], data["summonerLevel"])

    def by_puuid(self, puuid: str, region: str):
        """

        :param region:
        :type puuid:
        """
        response = bytes(
            urllib.request.urlopen(
                self.__by_puuid_url.format(region, puuid, super()._get_key())).read()).decode()
        data = eval(response)

        return SummonerAccount(data["id"], data["accountId"], data["puuid"], data["name"], data["profileIconId"],
                               data["revisionDate"], data["summonerLevel"])

    def by_summoner_id(self, summoner_id: str, region: str):
        """

        :param summoner_id:
        :param region:
        :return:
        """
        response = bytes(
            urllib.request.urlopen(
                self.__by_summoner_id_url.format(region, summoner_id, super()._get_key())).read()).decode()
        data = eval(response)

        return SummonerAccount(data["id"], data["accountId"], data["puuid"], data["name"], data["profileIconId"],
                               data["revisionDate"], data["summonerLevel"])
