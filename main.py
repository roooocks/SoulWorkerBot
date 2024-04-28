import logging

from os import environ

from dotenv import load_dotenv

from Module.basic import Basic
from Module.ui.button import SuggestionsButton

from discord import Intents, Guild
from discord import Game, Status
from discord.ext import commands

class MyBot(commands.Bot):
    def __init__(self) -> None:
        # Shard ID None has successfully RESUMED session "DISABLE!!!!!!!!!!!!!!!!"
        logging.getLogger("discord").setLevel(logging.WARN)  

        # Setting Intents (Whitelist Gateway Intent)
        intents = Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix = environ.get('COMMAND_PREFIX'),
            help_command = None,
            intents = intents,
            sync_command = True
        )

        self.initial_extension = [
            "Cogs.notice_task",
            "Cogs.notice_features",
            "Cogs.guild_features",
            "Cogs.developer_features"
        ]

        load_dotenv()

    async def setup_hook(self) -> None:
        for ext in self.initial_extension:
            await self.load_extension(ext)
        await self.tree.sync()

        self.add_view(SuggestionsButton())

    async def on_ready(self) -> None:
        Basic._print_log('아린! 활동을 시작합니다!')

        Basic._guild_channel = Basic._file_info()

        # version => 기능_종류.기능_수정(종합).오류_수정(종합)
        # 기능 종류에 개발자 관련은 제외
        # 1v => 1.3.1v
        # 2v => 2.6.4v
        await self.change_presence(status=Status.online, activity=Game("아린, 대기 중! - 2.6.4v"))

    async def on_guild_remove(self, guild: Guild):
        Basic._guild_channel.pop(guild.id)
        Basic._print_log(f'{guild.name}에서 추방되었습니다.')


# Running the bot
bot = MyBot()
bot.run(environ.get('DISCORD_TOKEN'))