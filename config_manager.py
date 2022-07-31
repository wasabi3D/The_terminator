import dataclasses

import discord
import yaml
import os
import json


@dataclasses.dataclass
class Config:
    test: int = 5


class GuildConfigManager:
    config: dict[int, Config] = {}

    @classmethod
    def load(cls):
        try:
            with open("guild_configs.json", "r") as f:
                tmp = json.load(f)
                for id_, cfg_dict in tmp.items():
                    tmp_cfg = Config()
                    tmp_cfg.__dict__ = cfg_dict
                    cls.config[id_] = tmp_cfg
        except json.decoder.JSONDecodeError:
            pass
        return cls

    @classmethod
    def initialize(cls, guilds: list[discord.Guild]):
        for guild in guilds:
            if str(guild.id) not in cls.config:
                cls.config[guild.id] = Config()
        return cls

    @classmethod
    def export(cls):
        with open("guild_configs.json", "w") as f:
            tmp = {}
            for id_, cfg_obj in cls.config.items():
                tmp[id_] = cfg_obj.__dict__
            json.dump(tmp, f)
        return cls
