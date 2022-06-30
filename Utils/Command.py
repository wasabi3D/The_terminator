import dataclasses

import discord
import typing


CMD_PREFIX = "!"
CANCEL_SPACE = "\\"
OPTION_PREFIX = "--"


@dataclasses.dataclass
class TypedCommand:
    keyword: str = ""  # the first word of a command. often associated with a prefix
    args: list[str] = dataclasses.field(default_factory=list)  # required arguments
    options: list[str] = dataclasses.field(default_factory=list)  # starts with --
    user: typing.Optional[discord.User] = None  # the user who typed the command
    channel: typing.Optional[discord.TextChannel] = None
    raw: str = ""  # raw arguments and options


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

    cmd = TypedCommand(keyword=preprocess[0].removeprefix(CMD_PREFIX), raw=" ".join(preprocess[1:]))
    for kw in preprocess[1:]:
        if kw.startswith(OPTION_PREFIX):
            cmd.options.append(kw)
        else:
            cmd.args.append(kw)

    cmd.user = usr
    cmd.channel = channel
    return cmd


class BaseCommand:
    def __init__(self):
        self.keyword = ""

    async def run(self, cmd: TypedCommand):
        pass


class CommandInterpreter:
    def __init__(self, *available_commands: typing.Callable):
        self.commands: list[BaseCommand] = list(map(lambda c: c(), available_commands))

    async def on_message(self, msg: discord.Message):
        if not msg.content.startswith(CMD_PREFIX):
            return
        typed_cmd = parse2cmd(msg.content, msg.author, msg.channel)
        called_cmd: BaseCommand = BaseCommand()
        for cmd in self.commands:
            if typed_cmd.keyword.lower() == cmd.keyword.lower():
                called_cmd = cmd
                break

        await called_cmd.run(typed_cmd)
