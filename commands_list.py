import discord

import Utils
from Utils.Command import BaseCommand, TypedCommand


class Ping(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "ping"

    async def run(self, cmd: TypedCommand, client: discord.Client):
        await cmd.channel.send("Pong!")


class Echo(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "echo"

    async def run(self, cmd: TypedCommand, client: discord.Client):
        await cmd.channel.send(cmd.raw)


class Adder(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "add"
        self.total = 0

    async def run(self, cmd: TypedCommand, client: discord.Client):
        self.total += 1
        await cmd.channel.send(f"{self.total}")
        await client.get_channel(992081849838993439).send(f"{cmd.user.mention} has added 1, total = {self.total}")


class ChangePrefix(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "chprefix"

    async def run(self, cmd: TypedCommand, client: discord.Client):
        if len(cmd.args) == 0:
            await cmd.channel.send("Please enter the new prefix.")
            return
        new_prefix = cmd.args[0]
        Utils.Command.CMD_PREFIX = new_prefix
        await client.change_presence(activity=discord.Game(f"Type {Utils.Command.CMD_PREFIX}help"))
        await cmd.channel.send("Prefix successfully changed.")

