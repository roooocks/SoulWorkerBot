from Module.ui.popup import SuggestionsPopup

from discord import ui as ui, ButtonStyle
from discord import Interaction

class SuggestionsButton(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="건의사항 작성", style=ButtonStyle.blurple, custom_id='suggestions')
    async def suggestions_input(
        self,
        interaction: Interaction,
        button: ui.Button
    ):
        await interaction.response.send_modal(SuggestionsPopup())
