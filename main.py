import discord
import yaml
import typing
import Utils
from commands_list import *


def main(config: dict[str, typing.Any]):
    print(f"Bot token is: {config['token']}")

    client = discord.Client()

    @client.event
    async def on_ready():
        print('Bot successfully connected to Discord.')

    execute_on_msg = [
        Utils.CommandInterpreter(
            Ping,
            Echo
        )
    ]

    @client.event
    async def on_message(message: discord.Message):
        for cal in execute_on_msg:
            await cal.on_message(message)

    client.run(config['token'])


if __name__ == "__main__":
    main(yaml.load(open("botconfigs.yml", "r"), yaml.CLoader))
