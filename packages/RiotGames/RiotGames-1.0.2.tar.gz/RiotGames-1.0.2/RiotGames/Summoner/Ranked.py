#  Copyright (c) 2020.
#  The copyright lies with Timo Hirsch-Hoffmann, the further use is only permitted with reference to source


class Ranked:
    def __init__(self, queue: str, summonerName: str, hotStreak: bool, wins: int, veteran: bool, losses: int, freshBlood: bool,
                 tier: str, inactive: bool, rank: str, summonerId: str, leaguePoints: int):
        self.queue = queue
        self.summonerName = summonerName
        self.hotStreak = hotStreak
        self.wins = wins
        self.veteran = veteran
        self.losses = losses
        self.freshBlood = freshBlood
        self.tier = tier
        self.inactive = inactive
        self.rank = rank
        self.summonerId = summonerId
        self.leaguePoints = leaguePoints
