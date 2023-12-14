import discord
from discord.ext import commands
from ApiKeys import apikeys


class MyClient(commands.Bot):
    async def setup_hook(self) -> None:
        await self.load_extension("handlers.messages")
        await self.load_extension("handlers.voiceChannelCommands")
        await self.load_extension("handlers.coolCommands")
        await self.load_extension("handlers.music")  

# defaul client = discord.Client(intents = intents)
client = MyClient(command_prefix='/', intents=discord.Intents.all())

@client.event
async def on_ready():
    #await client.change_presence(activity=discord.Streaming(name="Tommy Shelby", url="https://www.youtube.com/watch?v=LZytul2HsqI"))
    print("Bot started")


if __name__ == '__main__':
    client.run(apikeys.TOKEN)