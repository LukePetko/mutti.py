import discord
from discord.ext import commands
from discord.utils import get

import youtube_dl
from apiclient.discovery import build
import asyncio


# Hudba

youtube = build('youtube', 'v3', developerKey='AIzaSyBRZJGbujFn3dv5kSOQyBFafRxHvGCT0eQ')

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, mutti):
        self.mutti = mutti

    @commands.command(aliases=['hraj'])
    async def play(self, ctx, *, url):
        if url[:31] != "https://www.youtube.com/watch?v=":
            video = youtube.search().list(q=url, part='snippet', type='video')
            url = f'https://www.youtube.com/watch?v={video.execute()["items"][0]["id"]["videoId"]}'

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.mutti.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send(f'Pustil som ti: {player.title}')

    @commands.command(aliases=['hlasitosť', 'hlasitost'])
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Zmenil som si hlasitosť na {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the mutti from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


mutti = commands.Bot(command_prefix = 'mutti ')

@mutti.event
async def on_ready():
    print('Som tu mojko!')

@mutti.event
async def on_member_join(member):
    print(f'{member} došel')

@mutti.event
async def on_member_remove(member):
    print(f'{member} tu už neni')

@mutti.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(mutti.latency * 1000)}ms')



mutti.add_cog(Music(mutti))
mutti.run('NTc4NTI2OTgzOTE1NDM4MDgx.XN05Zw.UznGNE2Wnoh9Gz4vJY5PEk9qcT0')
