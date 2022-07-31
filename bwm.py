import discord
import enum
import json


class ScoreType(enum.Enum):
    MESSAGE = 0
    VC = 1


class OnlineTimestamp:
    def __init__(self, guild: discord.Guild):
        self.guild = guild

    def tick(self):
        pass


class BwmScoreManager:
    def __init__(self):
        self.started = False
        self.guild_id: int = -1
        self.scores: dict[int, dict[ScoreType, int]] = {}  # first key -> member id

    def on_message(self, message: discord.Message, client: discord.Client):
        if not self.started:
            return
        if message.author.id not in self.scores:
            tmp = ScoreType.__members__.values()
            self.scores[message.author.id] = dict(zip(tmp, [0] * len(tmp)))

        self.scores[message.author.id][ScoreType.MESSAGE] += 1
        self.export()

    def export(self):
        with open("bwm_scores.json", 'w') as f:
            json.dump(self.__dict__, f)


