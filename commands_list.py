import typing

import discord

import Utils

from Utils.Command import BaseCommand, TypedCommand


class Ping(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "ping"
        self.description = "Just return 'Pong!'"

    async def run(self, cmd: TypedCommand, client: discord.Client):
        await cmd.channel.send("Pong!")


class Echo(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "echo"
        self.description = "Repeat what the user said"

    async def run(self, cmd: TypedCommand, client: discord.Client):
        await cmd.channel.send(cmd.raw)


class Adder(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "add"
        self.total = 0
        self.description = "Louis's command to add numbers?"

    async def run(self, cmd: TypedCommand, client: discord.Client):
        self.total += 1
        await cmd.channel.send(f"{self.total}")
        await client.get_channel(992081849838993439).send(f"{cmd.user.mention} has added 1, total = {self.total}")


class ChangePrefix(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "chprefix"
        self.description = "Change command prefix."

    async def run(self, cmd: TypedCommand, client: discord.Client):
        if len(cmd.args) == 0:
            await cmd.channel.send("Please enter the new prefix.")
            return
        new_prefix = cmd.args[0]
        Utils.Command.CMD_PREFIX = new_prefix
        await client.change_presence(activity=discord.Game(f"Type {Utils.Command.CMD_PREFIX}help"))
        await cmd.channel.send("Prefix successfully changed.")


class Help(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "help"
        self.description = "Display commands list and their description."

    async def run(self, cmd: TypedCommand, client):
        embed = discord.Embed()
        embed.title = "Help"
        embed.colour = discord.Colour.red()
        for c in CMD_LIST:
            ins: BaseCommand = c()
            embed.add_field(name=f"{Utils.Command.CMD_PREFIX}{ins.keyword}", value=ins.description)

        await cmd.channel.send(embed=embed)


CMD_LIST: list[typing.Callable] = [Ping,
                                   Echo,
                                   Adder,
                                   ChangePrefix,
                                   Help
                                   ]
