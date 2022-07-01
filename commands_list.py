import typing
import discord
import Utils
from Utils.Command import BaseCommand, TypedCommand, Permission
import config_manager as cfg_mng


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
        self.permission_level = Permission.ADMIN

    async def run(self, cmd: TypedCommand, client: discord.Client):
        if len(cmd.args) == 0:
            await cmd.channel.send("Please enter the new prefix.")
            return
        new_prefix = cmd.args[0]
        if cmd.do_contain_option("option"):
            Utils.Command.OPTION_PREFIX = new_prefix
        else:
            Utils.Command.CMD_PREFIX = new_prefix

        if not cmd.do_contain_option("tmp"):
            cfg_mng.cfg.config["option_prefix"] = Utils.Command.OPTION_PREFIX
            cfg_mng.cfg.config["command_prefix"] = Utils.Command.CMD_PREFIX
            cfg_mng.cfg.export_config()
        await client.change_presence(activity=discord.Game(f"Type {Utils.Command.CMD_PREFIX}help"))
        await cmd.channel.send("Prefix successfully changed.")


class Help(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "help"
        self.description = "Display commands list and their description."

    async def run(self, cmd: TypedCommand, client: discord.Client):
        embed = discord.Embed()
        embed.title = "Help"
        embed.colour = discord.Colour.red()
        for c in CMD_LIST:
            ins: BaseCommand = c()
            if cmd.user_hierarchy.value >= ins.permission_level.value or\
                    f"{Utils.Command.OPTION_PREFIX}all" in cmd.options:
                embed.add_field(name=f"{Utils.Command.CMD_PREFIX}{ins.keyword}", value=ins.description)

        await cmd.channel.send(embed=embed)


CMD_LIST: list[typing.Callable] = [Ping,
                                   Echo,
                                   Adder,
                                   ChangePrefix,
                                   Help
                                   ]
