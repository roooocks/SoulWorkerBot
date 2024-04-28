from os import environ

from Module.embed_frame import EmbedFrame
from Module.ui.button import SuggestionsButton

from discord import app_commands, Interaction
from discord.ext import commands

class GuildFeatures(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        pass

    @app_commands.command(name="suggestions", description="건의사항 기능을 가진 UI를 출력합니다.")
    @app_commands.describe(warning="건의사항 작성 시 주의사항과 경고사항 적기")
    @commands.guild_only()
    async def suggestions(
        self,
        interaction: Interaction,
        warning: str
    ) -> None:
        if not interaction.user.guild_permissions.administrator and not interaction.user.id == int(environ.get('MY_ID')):
            return await interaction.response.send_message(f'`suggestions` 명령어는 관리자 외 사용이 불가능합니다.', ephemeral=True)

        await interaction.response.send_message(
            embed=EmbedFrame._suggestions("디스코드 건의사항", warning),
            view=SuggestionsButton()
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GuildFeatures(bot))
