#  Copyright (c) 2020.
#  The copyright lies with Timo Hirsch-Hoffmann, the further use is only permitted with reference to source

import urllib.request

from RiotGames.Summoner.Account import SummonerAccount

from RiotGames.API.RiotApi import RiotApi


class ChampionMasteries:
    def __init__(self, championLevel: int, chestGranted: bool, championPoints, championPointsSinceLastLevel,
                 championPointsUntilNextLevel: int, summonerId: str, tokensEarned: int, championId: int,
                 lastPlayTime: int):
        self.championLevel = championLevel
        self.chestGranted = chestGranted
        self.championPoints = championPoints
        self.championPointsSinceLastLevel = championPointsSinceLastLevel
        self.championPointsUntilNextLevel = championPointsUntilNextLevel
        self.summonerId = summonerId
        self.tokensEarned = tokensEarned
        self.championId = championId
        self.lastPlayTime = lastPlayTime


class ChampionMastery(RiotApi):
    __summoner_masteries_url = "https://{}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}?api_key={}"
    __champion_masteries_url = "https://{}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}/{}?api_key={}"
    __score_url = "https://{}.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/{}?api_key={}"

    def __init__(self, apikey: str):
        super().__init__(apikey)
        self.__super = super()

    def summoner_masteries(self, summoner: SummonerAccount, region: str):
        """

        :param summoner:
        :param region:
        :return:
        """
        summoner_masteries = []
        response = bytes(
            urllib.request.urlopen(
                self.__summoner_masteries_url.format(region, summoner.summonerId,
                                                     super()._get_key())).read()).decode()

        data = eval(response.replace("true", "True").replace("false", "False"))
        for champion_data in data:
            summoner_masteries.append(ChampionMasteries(champion_data["championLevel"],
                                                        champion_data["chestGranted"],
                                                        champion_data["championPoints"],
                                                        champion_data["championPointsSinceLastLevel"],
                                                        champion_data["championPointsUntilNextLevel"],
                                                        champion_data["summonerId"],
                                                        champion_data["tokensEarned"],
                                                        champion_data["championId"],
                                                        champion_data["lastPlayTime"]))
        return summoner_masteries

    def champion_masteries(self, summoner: SummonerAccount, champion_id: int, region: str):
        """

        :param summoner:
        :param champion_id:
        :param region:
        :return:
        """
        response = bytes(
            urllib.request.urlopen(
                self.__summoner_masteries_url.format(region, summoner.summonerId, champion_id,
                                                     super()._get_key())).read()).decode()

        data = eval(response.replace("true", "True").replace("false", "False"))
        return ChampionMasteries(data["championLevel"],
                                 data["chestGranted"],
                                 data["championPoints"],
                                 data["championPointsSinceLastLevel"],
                                 data["championPointsUntilNextLevel"],
                                 data["summonerId"],
                                 data["tokensEarned"],
                                 data["championId"],
                                 data["lastPlayTime"])

    def scores(self, summoner: SummonerAccount, region: str):
        """

        :param summoner:
        :param region:
        :return:
        """
        response = bytes(
            urllib.request.urlopen(
                self.__score_url.format(region, summoner.summonerId, super()._get_key())).read()).decode()

        return eval(response)
