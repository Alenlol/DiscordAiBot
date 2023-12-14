import discord, sys, asyncio
from discord import app_commands
from discord.ext import commands

sys.path.append(".")
from Ai import coolAiThings
from handlers import messages


class CoolCommands(commands.Cog):

    def __init__(self, client) -> None:
        self.client = client
        self.channel_name = "testbot"

    @commands.Cog.listener()
    async def on_ready(self):
        # This will synchronize @app_commands to work in discord
        synced = await self.client.tree.sync()

    @app_commands.command(name="start", description="Use it only in testbot")
    @app_commands.guild_only()
    async def start(self, ctx):
        if ctx.channel.name == self.channel_name:
            await ctx.response.send_message("Started", ephemeral=False)

    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     channel = reaction.message.channel
    #     print(reaction.emoji)
    #     await channel.send(f"{user.name} added: {reaction.emoji}")
    #     pass

    @app_commands.command(name="embed", description="Use it only in testbot")
    @app_commands.guild_only()
    async def embed(self, ctx):
        if ctx.channel.name == self.channel_name:
            await ctx.response.defer()
            await asyncio.sleep(0)
            response = coolAiThings.aiGenerateText(text="give to me a cringe quote", cntWords=10, candidatesCount=1)

            embed = discord.Embed(title="Tamyr", url="https://www.youtube.com/watch?v=LZytul2HsqI",
                                  description="I'm Tamyr Shelby", color=0x000000)
            embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
            embed.set_thumbnail(url=ctx.client.user.avatar.url)
            embed.add_field(name="Thomas Shelby", value=response)
            await ctx.followup.send(embed=embed, ephemeral=False)

    @app_commands.command(name="getnword", description="Use it only in testbot")
    @app_commands.guild_only()
    async def get_n_word(self, ctx):
        if ctx.channel.name == self.channel_name:
            await ctx.response.send_message(f"The count that N-word were used - {messages.Messages.get_n()}", ephemeral=False)


async def setup(client):
    await client.add_cog(CoolCommands(client))


if __name__ == '__main__':
    print("Ok")
