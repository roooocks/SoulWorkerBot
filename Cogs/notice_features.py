from os import environ
from typing import List, Union

from Module.basic import Basic

from discord import app_commands, Interaction, Guild
from discord.ext import commands

class NoticeFeatures(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        pass

    # autocomplete 검색용 채널 목록
    # 반환 자체는 어느타입이던 괜찮으나, 받는 함수의 파라미터가 무조건 str, floot, int 셋 중 하나여야 한다.
    async def channel_list(self,
        interaction: Interaction,
        current: str,
    ) -> List[Union[str, app_commands.Choice[str]]]:
        list = {}

        text_channels = interaction.guild.text_channels
        if len(current) == 0 and len(text_channels) >= 20:
            list['채널이 너무 많습니다. 채널명을 검색해서 찾아주세요!'] = '999'
        else:
            for channel in text_channels:
                if Basic._msg_permissions(channel, interaction.guild.me) and Basic._msg_permissions(channel, interaction.user):
                    list[channel.name] = str(channel.id)

        return [
            app_commands.Choice(name=key, value=key + '/' + value)
            for key, value in list.items() if current.lower() in key.lower()
        ]

    @app_commands.command(name="setting", description="공지를 받을 채널을 설정합니다.")
    @app_commands.describe(channel="채널을 검색해서 선택해주세요.")
    @app_commands.autocomplete(channel=channel_list)
    @app_commands.checks.cooldown(1, 6)
    @commands.guild_only()
    async def setting_channel(
        self,
        interaction: Interaction,
        channel: str
    ):
        if not interaction.user.guild_permissions.administrator and not interaction.user.id == int(environ.get('MY_ID')):
            return await interaction.response.send_message(f'`setting` 명령어는 관리자 외 사용이 불가능합니다.', ephemeral=True)

        if (channel.find('/') == -1):
            return await interaction.response.send_message('존재하지 않는 채널입니다!', ephemeral=True)

        channel_info = channel.split('/') # 0: 채널 이름 / 1: 채널 번호
        channel_id = int(channel_info[1])
        for text_channel in interaction.guild.text_channels:
            if channel_id == text_channel.id:
                if Basic._msg_permissions(text_channel, interaction.guild.me):
                    Basic._guild_channel[interaction.guild.id] = channel_id

                    Basic._file_write(Basic._guild_channel)
                    await interaction.response.send_message(f'`{channel_info[0]}`채널에 공지출력을 설정했습니다.', ephemeral=True)
                    Basic._print_log(f'{interaction.guild.name}에서 {channel_info[0]}채널에 공지출력을 설정했습니다.')
                    return
                else:
                    return await interaction.response.send_message(f'`{channel_info[0]}`채널에 `메시지 보내기` 권한이 없습니다.', ephemeral=True)

        await interaction.response.send_message(f'`{channel_info[0]}`채널이 존재하지 않습니다.', ephemeral=True)
    
    @setting_channel.error
    async def check_exception(
        self,
        interaction: Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f'{round(error.retry_after, 2)}초 뒤에 다시 시도해주세요.', ephemeral=True)
        
    @app_commands.command(name="delete", description="설정한 공지 채널을 제외합니다.")
    @commands.guild_only()
    async def delete_channel(
        self,
        interaction: Interaction
    ):
        if not interaction.user.guild_permissions.administrator and not interaction.user.id == int(environ.get('MY_ID')):
            return await interaction.response.send_message(f'`delete` 명령어는 관리자 외 사용이 불가능합니다.', ephemeral=True)
        
        if not Basic._guild_channel or not (interaction.guild.id in Basic._guild_channel):
            return await interaction.response.send_message("설정된 공지 채널이 없습니다.", ephemeral=True)

        Basic._print_log(f'{interaction.guild.name}에서 {interaction.guild.get_channel(Basic._guild_channel[interaction.guild.id]).name} 공지 채널을 삭제했습니다.')
        Basic._guild_channel.pop(interaction.guild.id)
        Basic._file_write(Basic._guild_channel)

        await interaction.response.send_message("설정한 공지 채널을 삭제했습니다.", ephemeral=True)

    @app_commands.command(name="now", description="현재 설정된 공지 채널을 확인합니다.")
    @app_commands.checks.cooldown(1, 6)
    @commands.guild_only()
    async def now_channel(
        self,
        interaction: Interaction
    ):
        if not Basic._guild_channel or not (interaction.guild.id in Basic._guild_channel):
            await interaction.response.send_message("설정된 공지 채널이 없습니다.", ephemeral=True)
        else:
            await interaction.response.send_message(f'현재 공지 채널은 `{interaction.guild.get_channel(Basic._guild_channel[interaction.guild.id]).name}`입니다.', ephemeral=True)

    @now_channel.error
    async def cooldown_exception(
        self,
        interaction: Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f'{round(error.retry_after, 2)}초 뒤에 다시 시도해주세요.', ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(NoticeFeatures(bot))
