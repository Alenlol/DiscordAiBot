import discord
from discord import app_commands
from discord.ext import commands


class Join(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
                    
    @app_commands.command(name="join", description="Use it only in music-channel")
    @app_commands.guild_only()
    async def join(self, ctx : discord.Interaction):
        if ctx.channel.name == 'music-channel':
            if (ctx.user.voice):
                channel = ctx.user.voice.channel
                await ctx.response.send_message("Connecting")
                await channel.connect()
            else:
                await ctx.response.send_message("You are not in voice channel, you must be in voice channel to run this command")

    @app_commands.command(name="leave", description="Use it only in music-channel")
    @app_commands.guild_only()
    async def leave(self, ctx : discord.Interaction):
        if ctx.channel.name == 'music-channel':
            if (ctx.channel.guild.voice_client):
                await ctx.response.send_message("Disconnecting")
                await ctx.channel.guild.voice_client.disconnect()
            else:
                await ctx.response.send_message("I am not in a voice channel")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name=str(member.guild.system_channel))
        channel = self.client.get_channel(channel.id)
        embed = discord.Embed(title=f"{member.name.capitalize()}, Welcome to server nigga")
        await channel.send(embed=embed)


async def setup(client):
    await client.add_cog(Join(client))