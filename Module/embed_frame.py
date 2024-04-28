from datetime import datetime

from discord import Embed

class EmbedFrame:
    def __init__(self):
        pass

    def _game_notice(
        title: str,
        link: str,
        src: str,
        date: str
    ) -> Embed:
        embed = Embed(title = title, url = link)
        if src is not None:
            embed.set_image(url = src)

        embed.set_footer(text = '공지 업로드 일자 ' + date)
        return embed

    def _bot_notice(
        title: str,
        content: str
    ) -> Embed:
        embed = Embed(
            title = title,
            description = content
        )
        embed.set_footer(text = f'공지 전송 일자 {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        return embed
    
    def _suggestions(
        title: str,
        content: str,
        date: bool = False
    ) -> Embed:
        embed = Embed(
            title = title,
            description = content
        )

        if date:
            embed.set_footer(text = f'건의사항 전송 일자 {datetime.now().strftime("%Y-%m-%d %H:%M")}')

        return embed
