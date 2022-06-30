from Utils.Command import BaseCommand, TypedCommand


class Ping(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "ping"

    async def run(self, cmd: TypedCommand):
        await cmd.channel.send("Pong!")


class Echo(BaseCommand):
    def __init__(self):
        super().__init__()
        self.keyword = "echo"

    async def run(self, cmd: TypedCommand):
        await cmd.channel.send(cmd.raw)
