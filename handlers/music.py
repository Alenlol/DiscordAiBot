import discord, asyncio, pafy, sys
from discord.ext import commands
from discord import FFmpegPCMAudio, app_commands
from youtubesearchpython import VideosSearch


sys.path.append("..")
import handlers.voiceChannelCommands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        # all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.title = None
        self.duration = None
        self.thumbnail = None

        self.vc = None

    @commands.Cog.listener()
    async def on_ready(self):
        synced = await self.bot.tree.sync()

    @staticmethod
    def time_checker(duration: str):
        result = duration.split(":")
        if 1 < len(result) < 3:
            result = [int(time) for time in result]
            if result[0] < 5:
                return True
        return False

    def search_yt(self, item):
        if item.startswith("https://"):
            return
        result = None
        try:
            search = VideosSearch(item.lower(), limit=1)
            print(search.result())
            self.duration = search.result()["result"][0]["duration"]
            self.title = search.result()["result"][0]["title"]
            self.thumbnail = search.result()["result"][0]["thumbnails"]
            if self.time_checker(self.duration):
                result = {'source': search.result()["result"][0]["link"], 'title': self.title}
        except Exception as e:
            print("Error", e)

        return result

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)
            song = pafy.new(m_url)

            audio = song.getbestaudio()

            self.vc.play(FFmpegPCMAudio(audio.url, **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx : discord.Interaction):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            # data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            # song = data['url']
            # self.vc.play(discord.FFmpegPCMAudio(song, executable= "ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
            song = pafy.new(m_url['source'])  # creates a new pafy object

            await ctx.followup.send("Playing")

            audio = song.getbestaudio()  # gets an audio source

            # converts the youtube audio source into a source discord can use

            self.vc.play(FFmpegPCMAudio(audio.url, **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False


    async def embed(self, ctx):
        name_of_music = self.title.split(" ")
        thubmnail_of_music = self.thumbnail[0]['url']
        if self.is_playing:
            name_of_music[0] = f"#{(len(self.music_queue)+1)} " + name_of_music[0]
        embed = discord.Embed(title=name_of_music[0], description = " ".join(name_of_music), colour=0x2471A3)
        embed.set_thumbnail(url=thubmnail_of_music)
        embed.add_field(name=f"Requested by {ctx.user.name}", value=f"Length : {self.duration}")
        await ctx.response.send_message(embed=embed, ephemeral=False)

    @app_commands.command(name="play", description="Use it only in music-channel")
    @app_commands.describe(url="Give me a link")
    @app_commands.guild_only()
    async def play(self, ctx, url: str):
        if self.vc is None:
            self.vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

            # in case we fail to connect
            if not ctx.channel.guild.voice_client:
                await ctx.response.send_message("```Could not connect to the voice channel```")
                return

        if self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(url)
            if song is None:
                await ctx.response.send_message("```You have to write link of the music after /play```")
            else:
                self.music_queue.append([song, self.vc])
                await self.embed(ctx)
                if self.is_playing == False:
                    await self.play_music(ctx)

    @app_commands.command(name="pause", description="Use it only in music-channel")
    @app_commands.guild_only()
    async def pause(self, ctx):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            await ctx.response.send_message("```Pausing```")
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            await ctx.response.send_message("```Resuming```")
            self.vc.resume()

    @app_commands.command(name="resume", description="Use it only in music-channel")
    @app_commands.guild_only()
    async def resume(self, ctx):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            await ctx.response.send_message("```Resuming```")
            self.vc.resume()

    @app_commands.command(name="skip", description="Use it only in music-channel")
    @app_commands.guild_only()
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            # try to play next in the queue if it exists
            await ctx.response.send_message("```Skipping```")
            await self.play_music(ctx)

    @app_commands.command(name="queue", description="Use it only in music-channel")
    @app_commands.guild_only()
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"#{i+1} -" + self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.response.send_message(f"```queue:\n{retval}```")
        else:
            await ctx.response.send_message("```No music in queue```")

    @app_commands.command(name="clear", description="Use it only in music-channel")
    @app_commands.guild_only()
    async def clear(self, ctx):
        if self.vc is not None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.response.send_message("```Music queue cleared```")

    @app_commands.command(name="remove", description="Use it only in music-channel")
    @app_commands.guild_only()
    async def re(self, ctx):
        self.music_queue.pop()
        await ctx.response.send_message("```last song removed```")


async def setup(client):
    await client.add_cog(Music(client))

if __name__ == '__main__':
    print("Ok")