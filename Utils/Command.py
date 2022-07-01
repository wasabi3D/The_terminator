from __future__ import annotations
import dataclasses
from enum import Enum

import discord
import typing


CMD_PREFIX = "!"
CANCEL_SPACE = "\\"
OPTION_PREFIX = "--"


class Permission(Enum):
    EVERYONE = 0
    MOD = 1
    ADMIN = 2


@dataclasses.dataclass
class TypedCommand:
    """
    Interpreted command by the user
    """
    keyword: str = ""  # the first word of a command. often associated with a prefix
    args: list[str] = dataclasses.field(default_factory=list)  # required arguments
    options: list[str] = dataclasses.field(default_factory=list)  # starts with --
    user: typing.Optional[discord.User] = None  # the user who typed the command
    channel: typing.Optional[discord.TextChannel] = None
    raw: str = ""  # raw arguments and options
    user_hierarchy: Permission = Permission.EVERYONE

    def do_contain_option(self, option) -> bool:
        """
        :param option: Option without its prefix
        :return: True or False
        """
        for op in self.options:
            if op.startswith(f"{OPTION_PREFIX}{option}"):
                return True
        return False


def removeprefix(self: str, prefix: str, /) -> str:
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]


def removesuffix(self: str, suffix: str, /) -> str:
    # suffix='' should not call self[:-0].
    if suffix and self.endswith(suffix):
        return self[:-len(suffix)]
    else:
        return self[:]


def parse2cmd(raw_command: str,
              usr: typing.Optional[discord.User] = None,
              channel: typing.Optional[discord.TextChannel] = None
              ) -> TypedCommand:
    """
    Converts raw string command to TypedCommand

    :param raw_command: raw string
    :param usr: the user who typed this
    :param channel: the channel which the command was typed
    """
    spl = raw_command.split(" ")
    preprocess = []
    for arg in spl:
        if len(preprocess) > 0:
            last = preprocess[-1]
            if last[-1] == CANCEL_SPACE:
                last = removesuffix(last, CANCEL_SPACE)
                preprocess[-1] = " ".join([last, arg])
                continue
        preprocess.append(arg)

    cmd = TypedCommand(keyword=removeprefix(preprocess[0], CMD_PREFIX), raw=" ".join(preprocess[1:]))
    for kw in preprocess[1:]:
        if kw.startswith(OPTION_PREFIX):
            cmd.options.append(kw)
        else:
            if kw.startswith('"') and kw.endswith('"'):
                kw = removesuffix(removeprefix(kw, '"'), '"')
            cmd.args.append(kw)

    cmd.user = usr
    cmd.channel = channel
    guild: discord.Guild = channel.guild
    member: discord.Member = guild.get_member(usr.id)
    if member.guild_permissions.administrator:
        cmd.user_hierarchy = Permission.ADMIN

    return cmd


class BaseCommand:
    """
    Base class to define all other commands. See commands_list.py for examples
    """
    def __init__(self):
        self.keyword = ""
        self.description = ""
        self.permission_level: Permission = Permission.EVERYONE

    async def run(self, cmd: TypedCommand, client):
        pass


class CommandInterpreter:
    """
    Class which executes a given command
    """
    def __init__(self, *available_commands: typing.Callable):
        self.commands: list[BaseCommand] = list(map(lambda c: c(), available_commands))

    async def on_message(self, msg: discord.Message, client: discord.Client):
        if not msg.content.startswith(CMD_PREFIX):
            return
        typed_cmd = parse2cmd(msg.content, msg.author, msg.channel)
        called_cmd: BaseCommand = BaseCommand()
        for cmd in self.commands:
            if typed_cmd.keyword.lower() == cmd.keyword.lower():
                called_cmd = cmd
                break

        if typed_cmd.user_hierarchy.value >= called_cmd.permission_level.value:
            await called_cmd.run(typed_cmd, client)
        else:
            await msg.channel.send("You don't have enough permissions to run that command.")
