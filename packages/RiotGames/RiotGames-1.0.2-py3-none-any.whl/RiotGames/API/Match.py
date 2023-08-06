#  Copyright (c) 2020.
#  The copyright lies with Timo Hirsch-Hoffmann, the further use is only permitted with reference to source


import urllib.request

from RiotGames.API.RiotApi import RiotApi


class Match(RiotApi):
    __timeline_by_match_id_url = "https://{}.api.riotgames.com/lol/match/v4/timelines/by-match/{}?api_key={}"

    def __init__(self, apikey: str):
        super().__init__(apikey)
        self.__super = super()

    def by_id(self, match_id: int, region: str):
        pass

    def matchlist_by_account_id(self, account_id: str, begin_time: int = None, end_time: int = None, begin_index: int = None, end_index: int = None, champions: list = None, queue: list = None, season: list = None):
        """
        Special Function still in dev
        https://developer.riotgames.com/apis#match-v4/GET_getMatchlist

        TODO
        format url

        :param account_id:
        encrypted account id
        :param begin_time:
        :param end_time:
        :param begin_index:
        :param end_index:
        :param champions:
        :param queue:
        :param season:
        :return:
        """
        pass

    def timeline_by_match_id(self, match_id: int, region: str):
        response = bytes(
            urllib.request.urlopen(
                self.__timeline_by_match_id_url.format(region, match_id, super()._get_key())).read()).decode()
        data = eval(response)

        return data


Match.matchlist_by_account_id(Match("ok"), "1", )