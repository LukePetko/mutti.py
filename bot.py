import discord
from discord.ext import commands
import youtube_dl

mutti = commands.Bot(command_prefix = '!')

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

@mutti.command()
async def pod(ctx):
    server = ctx.message.guild

    voice_mutti = await ctx.message.author.voice.channel.connect()

    player = await voice_mutti.create_ytdl_player('https://www.youtube.com/watch?v=MbhXIddT2YY')
    player.start()

mutti.run('NTc4NTI2OTgzOTE1NDM4MDgx.XN05Zw.UznGNE2Wnoh9Gz4vJY5PEk9qcT0')
