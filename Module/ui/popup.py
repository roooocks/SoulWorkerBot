from Module.basic import Basic
from Module.embed_frame import EmbedFrame

from discord import ui, TextStyle
from discord import Interaction

class SuggestionsPopup(ui.Modal, title="건의사항"):
    suggestions_content = ui.TextInput(label="리그 건의사항을 입력해주세요.", style=TextStyle.long, placeholder="여기서 작성해주세요~", required=True, min_length=1, max_length=500)

    async def on_submit(
        self,
        interaction: Interaction
    ) -> None:
        if interaction.user.nick:
            user_name = interaction.user.nick
        else:
            user_name = interaction.user.name

        await interaction.guild.owner.send(embed=EmbedFrame._suggestions(
            title = f'`{user_name}`님의 건의사항입니다.',
            content = self.suggestions_content,
            date = True
        ))

        Basic._print_log(f'{interaction.user.name}님이 {interaction.guild.name}에 건의사항을 보냈습니다.')
        await interaction.response.send_message("건의사항이 전송되었습니다!", ephemeral=True)