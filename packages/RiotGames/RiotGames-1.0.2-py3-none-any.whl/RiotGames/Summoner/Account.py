#  Copyright (c) 2020.
#  The copyright lies with Timo Hirsch-Hoffmann, the further use is only permitted with reference to source

class SummonerAccount:
    def __init__(self, summonerId: str, accountId: str, puuid: str, name: str, profileIconId: str, revisionDate: int,
                 summonerLevel: int):
        self.summonerId = summonerId
        self.accountId = accountId
        self.puuid = puuid
        self.name = name
        self.profileIconId = profileIconId
        self.revisionDate = revisionDate
        self.summonerLevel = summonerLevel
