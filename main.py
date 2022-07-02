import commands_list
from commands_list import *
import config_manager as cfg_mng
import threading


def main(config: dict[str, typing.Any]):
    print(f"Bot token is: {config['token']}")
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('Bot successfully connected to Discord.')
        await client.change_presence(activity=discord.Game(f"Type {Utils.Command.CMD_PREFIX}help"))

    execute_on_msg = [
        Utils.CommandInterpreter(
            *commands_list.CMD_LIST.values()
        )
    ]

    @client.event
    async def on_message(message: discord.Message):
        for cal in execute_on_msg:
            await cal.on_message(message, client)

    Utils.Command.CMD_PREFIX = config['command_prefix']
    Utils.Command.OPTION_PREFIX = config['option_prefix']
    client.run(config['token'])


if __name__ == "__main__":
    main(cfg_mng.cfg.get_config())
