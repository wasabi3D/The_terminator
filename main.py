import commands_list
from commands_list import *
import config_manager as cfg_mng
import vars


def main():
    token = input("Please enter bot token: ")
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('Bot successfully connected to Discord.')
        vars.GUILDS = client.guilds
        cfg_mng.GuildConfigManager.load().initialize(vars.GUILDS).export()

    execute_on_msg = [
        Utils.CommandInterpreter(
            *commands_list.CMD_LIST.values()
        )
    ]

    @client.event
    async def on_message(message: discord.Message):
        for cal in execute_on_msg:
            await cal.on_message(message, client)

    client.run(token)


if __name__ == "__main__":
    main()
