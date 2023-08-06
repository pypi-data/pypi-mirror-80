#  Copyright (c) 2020.
#  The copyright lies with Timo Hirsch-Hoffmann, the further use is only permitted with reference to source


import urllib.request


from RiotGames.API.RiotApi import RiotApi


class LOLStatus(RiotApi):
    __lol_status_url = "https://{}.api.riotgames.com/lol/status/v3/shard-data?api_key={}"

    def __init__(self, apikey: str):
        super().__init__(apikey)
        self.__super = super()

    def get_status(self, region: str):
        response = bytes(
            urllib.request.urlopen(
                self.__lol_status_url.format(region, super()._get_key())).read()).decode()

        data = eval(response.replace("true", "True").replace("false", "False"))

        return data