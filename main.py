import discord
from discord.ext import commands
import asyncio
from gtts import gTTS
import time
import random

tts_name = "a.wav"
alarm_sound = "alarm.mp3"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_voice_state_update(member, before, after):
    bot_channel_id = None
    if bot.voice_clients:
        bot_channel_id = bot.voice_clients[0].channel.id
        bot_voice_channel = member.guild.get_channel(bot_channel_id)
        if len(bot_voice_channel.members) == 1:
            await bot_voice_channel.guild.voice_client.disconnect()

@bot.command()
async def 도움(ctx):
    await ctx.send("!도움 !입장 !나가 !알람 시간 할일 !스톱워치 시간 할일 !주사위 최소 최대")

# 음성 채널에 봇 호출
@bot.command()
async def 입장(ctx):
    # 호출한 유저가 속한 음성 채널에 봇을 입장시킵니다.
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("입장 오류 : 음성 채널에 먼저 들어가 주세요!")

# 음성 채널에서 봇 퇴장
@bot.command()
async def 나가(ctx):
    # 호출한 유저가 속한 음성 채널에서 봇을 퇴장시킵니다.
    if (ctx.voice_client and ctx.author.voice and ctx.voice_client.channel == ctx.author.voice.channel):
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("퇴장 오류 : 동일한 음성 채널에 먼저 들어가 주세요!")

@bot.command()
async def 알람(ctx,t,s="빈 알람"):
    # 입력된 시간 문자열에서 시간과 분을 추출
    try:
        hour = int(t[:2])
        minute = int(t[2:])
    except ValueError:
        await ctx.send("올바른 시간 형식이 아닙니다. 예: !알람 1730 알람내용")
        return

    current_time = time.localtime()
    current_hours = current_time.tm_hour
    current_minutes = current_time.tm_min
    current_seconds = current_time.tm_sec

    time_to_wait = (hour - current_hours) * 3600 + (minute - current_minutes) * 60 - current_seconds
    
    if time_to_wait <= 0:
        time_to_wait + 24 * 3600

    await ctx.send(f"{hour}시 {minute}분에 알람이 생성되었습니다. ")
    print(current_time,"|",time_to_wait,"|")

    # 타이머 설정 및 작업 예약
    await asyncio.sleep(time_to_wait)
    
    # 알람 실행
    await ctx.send(s)
    if bot.voice_clients:
        voice_client = bot.voice_clients[0]
        if voice_client.is_connected():
                voice_client.play(discord.FFmpegPCMAudio(alarm_sound))

@bot.command()
async def 스톱워치(ctx,t,s="빈 스톱워치"):
    await ctx.send(f"{t}분 후에 알람이 생성되었습니다.")
    
    await asyncio.sleep(int(float(t)*60))
    
    await ctx.send(s)
    if bot.voice_clients:
        voice_client = bot.voice_clients[0]
        if voice_client.is_connected():
                voice_client.play(discord.FFmpegPCMAudio(alarm_sound))

@bot.command()
async def 주사위(ctx, minn=1, maxn=99):
    random.seed(time.time())
    await ctx.send(f"{ctx.author.mention}님께서 주사위를 굴려 {random.randint(int(minn),int(maxn))}이 나왔습니다!")

# on_message 이벤트가 발생할 때 마다 호출 - 채팅채널에 채팅이 올라올 때 마다 호출
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # TTS로 메시지 음성 변환
    tts = gTTS(text=message.content, lang='ko')
    tts.save(tts_name)
    
    # 봇이 현재 연결된 음성 채널에서 메시지 음성을 재생
    if bot.voice_clients:
        voice_client = bot.voice_clients[0]
        if voice_client.is_connected():
            voice_client.play(discord.FFmpegPCMAudio(tts_name))
    
    await bot.process_commands(message)

# Discord Bot Token
token = ""
with open('token', 'r') as file:
    token = file.read()
bot.run(token)

