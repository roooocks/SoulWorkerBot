from datetime import datetime

from discord import Embed

class EmbedFrame:
    def __init__(self):
        pass

    def   _game_notice(
        title: str,
        link: str,
        src: str,
        booking_date: str,
        now_date: str
    ) -> Embed:
        embed = Embed(title = title, url = link)
        if src is not None:
            embed.set_image(url = src)

        # 스팀 소울워커의 공지 RSS는 거의 대부분이 당일날의 날짜와 시간이 아님 (예약이라 생각)
        # 다른 게임에 사용할 경우 해당부분 수정
        embed.set_footer(text = f'공지 업로드 예약 일자 : {booking_date}\n실제 공지 업로드 일자 : {now_date}')
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
