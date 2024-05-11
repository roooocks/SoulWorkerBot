import aiohttp
import xml.etree.ElementTree as ET

from os import environ
from datetime import datetime

from Module.basic import Basic
from Module.embed_frame import EmbedFrame

from discord.ext import commands, tasks

class NoticeTask(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        # API call variable
        self.url: str = environ.get('NOTICE_URL')
        self.headers: dict = { 
            'User-Agent': environ.get('USER_AGENT') 
        }

        # Recent RSS data save
        self.recent_date: str = ""

        self.bot = bot

        # task start
        Basic._print_log("notice task start")
        self.upload.start()

    @commands.Cog.listener()
    async def on_ready(self):
        # 이유는 모르겠는데 가끔 봇이 스스로 재시작하는 경우가 존재
        # 이때 task는 종료만 되고 재시작을 안해서 아래와 같이 작성 
        if not self.upload.is_running():
            Basic._print_log("notice task restart")
            self.upload.start()

    # Tasks setting
    # 봇이 멈추면 종료되기 전에 작동합니다.
    def cog_unload(self) -> None:
        if self.upload.is_running():
            Basic._print_log('stop notice upload')
            self.upload.cancel()

    @tasks.loop(seconds = 120)
    async def upload(self) -> None:
        # Basic._print_log("공지 진입")

        if not Basic._guild_channel:
            # Basic._print_log("어느 서버에도 공지 채널이 존재하지 않습니다.")
            return None

        data = await self.__get()

        if self.recent_date != data['booking_date']:
            for guild_id, channel_id in Basic._guild_channel.items():
                channel = self.bot.get_channel(channel_id)
                if channel is None:
                    continue
                
                if Basic._msg_permissions(channel, channel.guild.me): # channel 부분은 TextChannel이 불가능함
                    await channel.send(embed = EmbedFrame._game_notice(data['title'], data['link'], data['src'], data['booking_date'], data['now_date']))
                    Basic._print_log(f'{channel.guild.name}에서 {data["booking_date"]}의 공지사항 출력됨')
                    self.recent_date = data['booking_date']
                else:
                    Basic._print_log(f'{channel.guild.name}에서 {channel.name} 채널에 메시지 전송 권한이 존재하지 않습니다.')

    @upload.before_loop
    async def before_loop(self) -> None:
        Basic._print_log("waiting...")
        self.recent_date = (await self.__get())['booking_date']
        
        # https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html
        await self.bot.wait_until_ready()

    async def __get(self):
        async with aiohttp.ClientSession(headers = self.headers) as session:
            async with session.get(self.url) as res:
                Basic._print_log("Steam News RSS 진입")
                
                if res.status == 200:
                    result = {}
                    xmlData = await res.text()

                    item = ET.fromstring(xmlData).find("channel/item")
                    result['title'] = item.find('title').text
                    result['link'] = item.find('link').text
                    result['src'] = item.find('enclosure').get('url')
                    
                    # pubDate type = RFC433
                    # pubDate가 예약한 날짜로 나오는거라 판단 => 날짜를 [예약한 날짜, 가져온 날짜] 2가지로 나눠 저장
                    result['booking_date'] = datetime.strptime(item.find("pubDate").text, '%a, %d %b %Y %H:%M:%S %z').strftime("%Y-%m-%d %H:%M")
                    result['now_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")

                    # 디버깅용
                    # Basic._print_log('제목: ' + item.find("title").text)
                    # Basic._print_log('링크: ' + item.find("link").text)
                    # Basic._print_log('이미지: ' + item.find("enclosure").get('url'))
                    # Basic._print_log('날짜: ' + datetime.strptime(item.find("pubDate").text, '%a, %d %b %Y %H:%M:%S %z').strftime("%Y-%m-%d %H-%M"))
                
                    return result
                else:
                    Basic._print_log(f'Steam News RSS의 {res.status} 코드')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(NoticeTask(bot))