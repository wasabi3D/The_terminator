import dataclasses

import discord
import typing


CMD_PREFIX = "!"
CANCEL_SPACE = "\\"
OPTION_PREFIX = "--"


@dataclasses.dataclass
class TypedCommand:
    def __init__(self):
        self.keyword: str = ""  # the first word of a command. often associated with a prefix
        self.args: list[str] = []  # required arguments
        self.options: list[str] = []  # starts with --
        self.user: typing.Optional[discord.User] = None  # the user who typed the command
        self.channel: typing.Optional[discord.TextChannel] = None


def parse2cmd(raw_command: str,
              usr: typing.Optional[discord.User] = None,
              channel: typing.Optional[discord.TextChannel] = None
              ) -> TypedCommand:
    spl = raw_command.split(" ")
    preprocess = []
    for arg in spl:
        if len(preprocess) > 0:
            last = preprocess[-1]
            if last[-1] == CANCEL_SPACE:
                last = last.removesuffix(CANCEL_SPACE)
                preprocess[-1] = " ".join([last, arg])
                continue
        preprocess.append(arg)

    cmd = TypedCommand()
    cmd.keyword = preprocess[0].removeprefix(CMD_PREFIX)
    for kw in preprocess[1:]:
        if kw.startswith(OPTION_PREFIX):
            cmd.options.append(kw)
        else:
            cmd.args.append(kw)

    cmd.user = usr
    cmd.channel = channel
    return cmd
