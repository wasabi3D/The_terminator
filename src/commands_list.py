import typing
import discord
import re
from Utils.Command import BaseCommand, TypedCommand, Permission, CMD_PREFIX


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
        rep = cmd.get_option("rep")
        num = 1
        content = cmd.raw
        try:
            if rep:
                num = int(rep.split('=')[1])
            content = " ".join(cmd.args)
        except ValueError or IndexError:
            pass

        for i in range(num):
            await cmd.channel.send(content)


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

#
# class ChangePrefix(BaseCommand):
#     def __init__(self):
#         super().__init__()
#         self.keyword = "chprefix"
#         self.description = "Change command prefix."
#         self.permission_level = Permission.ADMIN
#
#     async def run(self, cmd: TypedCommand, client: discord.Client):
#         if len(cmd.args) == 0:
#             await cmd.channel.send("Please enter the new prefix.")
#             return
#         new_prefix = cmd.args[0]
#         if cmd.get_option("option"):
#             Utils.Command.OPTION_PREFIX = new_prefix
#         else:
#             Utils.Command.CMD_PREFIX = new_prefix
#
#         if not cmd.get_option("tmp"):
#             cfg_mng.cfg.config["option_prefix"] = Utils.Command.OPTION_PREFIX
#             cfg_mng.cfg.config["command_prefix"] = Utils.Command.CMD_PREFIX
#             cfg_mng.cfg.export_config()
#         await client.change_presence(activity=discord.Game(f"Type {Utils.Command.CMD_PREFIX}help"))
#         await cmd.channel.send("Prefix successfully changed.")


class Help(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "help"
        self.description = "Display commands list and their description."

    async def run(self, cmd: TypedCommand, client: discord.Client):
        embed = discord.Embed()
        embed.title = "Help"
        embed.colour = discord.Colour.red()
        for c in CMD_LIST.values():
            ins: BaseCommand = c
            if cmd.user_hierarchy.value >= ins.permission_level.value or cmd.get_option("all"):
                embed.add_field(name=f"{CMD_PREFIX}{ins.keyword}", value=ins.description)

        await cmd.channel.send(embed=embed)


class Select(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "select"
        self.description = "Command used to select messages/members/channels."
        self.permission_level = Permission.ADMIN
        self.selected: dict[discord.User, dict[type, list[typing.Union[discord.User, discord.Message, discord.TextChannel]]]] = {}

    async def run(self, cmd: TypedCommand, client: discord.Client):
        try:
            if cmd.user not in self.selected:
                self.selected[cmd.user] = {discord.Message: [], discord.User: [], discord.TextChannel: []}
            if cmd.args[0] == "message":
                if cmd.get_option("clear"):
                    self.selected[cmd.user][discord.Message].clear()
                lim = 100
                usr_lim = cmd.get_option("lim")
                if usr_lim:
                    lim = int(usr_lim.split("=")[1])
                msgs = await cmd.channel.history(limit=lim).flatten()

                target_usr = cmd.get_option("user")
                if target_usr:
                    msgs = [m for m in msgs if m.author.mention == target_usr.split("=")[1]]

                target_exp = cmd.get_option("re")
                if target_exp:
                    msgs = [m for m in msgs if re.fullmatch(target_exp.split("=")[1], m.content)]

                self.selected[cmd.user][discord.Message] += msgs
                await cmd.channel.send(f"Successfully selected {len(self.selected[cmd.user][discord.Message])}"
                                       f"messages.")

            elif cmd.args[0] == "user":
                pass
            elif cmd.args[0] == "channel":
                pass
        except IndexError:
            await cmd.channel.send("Index error, Try again.")
        except TypeError:
            await cmd.channel.send("Type conversion failed.")


class Delete(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "delete"
        self.description = "Command used to delete messages/members/channels."
        self.permission_level = Permission.ADMIN

    async def run(self, cmd: TypedCommand, client: discord.Client):
        if cmd.user not in CMD_LIST[Select].selected:
            await cmd.channel.send("Seems you haven't selected anything")
            return
        if cmd.args[0] == "message":
            msgs: list[discord.Message] = CMD_LIST[Select].selected[cmd.user][discord.Message]
            for msg in msgs:
                await msg.delete()
            await cmd.channel.send(f"Successfully deleted {len(msgs)} messages.")
            msgs.clear()

        elif cmd.args[0] == "channel":
            pass


class Id(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "id"
        self.description = "Allows the user to obtain someone's user id by their name and discriminator."
        self.permission_level = Permission.EVERYONE

    async def run(self, cmd: TypedCommand, client: discord.Client):
        target_user = cmd.args[0]
        guild_range = [cmd.channel.guild] if not cmd.get_option("all") else client.guilds

        member: discord.Member
        for guild in guild_range:
            for member in guild.members:
                if target_user == f"{member.name}#{member.discriminator}":
                    await cmd.channel.send(member.id)
                    return
        await cmd.channel.send("User not found. Try using the --all option.")


_available = [Ping, Echo, Adder, Help, Select, Delete, Id]
CMD_LIST: dict[type, BaseCommand] = dict(zip(_available, map(lambda cls: cls(), _available)))
