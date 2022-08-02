import commands_list
from commands_list import *
import config_manager as cfg_mng
import bwm
import Utils
import os


def main():
    os.chdir(os.path.dirname(__file__))
    token = input("Please enter bot token: ")
    intents = discord.Intents.default()
    intents.members = True
    intents.presences = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('Bot successfully connected to Discord.')
        guilds = client.guilds
        cfg_mng.GuildConfigManager.load().initialize(guilds).export()
        bwm.OnlineHistory.initialize(guilds).save().run_periodic_checker()

    execute_on_msg = [
        Utils.CommandInterpreter(
            *commands_list.CMD_LIST.values()
        )
    ]

    @client.event
    async def on_message(message: discord.Message):
        for cal in execute_on_msg:
            await cal.on_message(message, client)

    @client.event
    async def on_member_update(before: discord.Member, after: discord.Member):
        bwm.OnlineHistory.update_usr_status(after)

    client.run(token)


if __name__ == "__main__":
    main()
