import discord
import yaml
import typing
import Utils
import os
from commands_list import *


def main(config: dict[str, typing.Any]):
    print(f"Bot token is: {config['token']}")

    client = discord.Client()

    @client.event
    async def on_ready():
        print('Bot successfully connected to Discord.')
        await client.change_presence(activity=discord.Game(f"Type {Utils.Command.CMD_PREFIX}help"))

    execute_on_msg = [
        Utils.CommandInterpreter(
            Ping,
            Echo,
            Adder,
            ChangePrefix
        )
    ]

    @client.event
    async def on_message(message: discord.Message):
        for cal in execute_on_msg:
            await cal.on_message(message, client)

    client.run(config['token'])


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    print(os.listdir())
    main(yaml.load(open("botconfigs.yml", "r"), yaml.CLoader))
