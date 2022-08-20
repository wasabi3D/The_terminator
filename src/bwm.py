import discord
import enum
import json
import time
import os
import threading


class ScoreType(enum.Enum):
    MESSAGE = 0
    VC = 1


class OnlineHistory:
    history: dict[int, list[list[float, str, bool]]] = {}
    FILE = "../data/onlinehistory.json"

    @classmethod
    def initialize(cls, guilds: list[discord.Guild]):
        member: discord.Member
        for guild in guilds:
            for member in guild.members:
                cls.usr_init(member)
        return cls

    @classmethod
    def usr_init(cls, member: discord.Member) -> bool:
        first = False
        if member.id not in cls.history or len(cls.history[member.id]) == 0:
            cls.history[member.id] = []
            first = True
        cls.history[member.id].append([time.time(), member.status.value, False])
        cls.history[member.id].append([time.time(), discord.Status.offline, True])
        return first

    @classmethod
    def update_usr_status(cls, after: discord.Member, minimum_interval=0.5):
        if not cls.usr_init(after):
            if time.time() - cls.history[after.id][-1][0] >= minimum_interval:
                if cls.history[after.id][-1][2]:
                    cls.history[after.id].pop()
                cls.history[after.id].append([time.time(), after.status.value, False])
                cls.history[after.id].append([time.time(), discord.Status.offline, True])

    @classmethod
    def save(cls):
        with open(cls.FILE, "w") as f:
            json.dump(cls.history, f, indent=2)
        return cls

    @classmethod
    def load(cls):
        with open(cls.FILE, "r") as f:
            cls.history = json.load(f)
        return cls

    @classmethod
    def run_periodic_checker(cls):
        th = threading.Thread(target=cls._check, name="TimestampPeriodicChecker")
        th.start()

    @classmethod
    def _check(cls):
        interval = 5
        while True:
            for uid in cls.history:
                if not cls.history[uid][-1][2]:
                    cls.history[uid].append([time.time(), discord.Status.offline, True])
                else:
                    cls.history[uid][-1][0] = time.time()
            cls.save()
            time.sleep(interval)


class BwmScoreTable:
    FILE = "../data/bwm_scores.json"

    def __init__(self):
        self.enabled = False
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
        with open(self.__class__.FILE, 'w') as f:
            json.dump(self.__dict__, f)

