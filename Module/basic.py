import os.path, pickle

from datetime import datetime

from discord import TextChannel, Member

class Basic:
    _guild_channel: dict = {}

    def __init__(self) -> None:
        pass

    def _print_log(msg: str = '') -> None:
        print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg}')

    def _file_info() -> dict:
        if os.path.isfile("FileSys/NoticeChannel.bin"):
            with open('FileSys/NoticeChannel.bin', 'rb') as f:
                try:
                    return pickle.load(f)
                except EOFError:
                    return {}
        else:
            Basic._print_log("존재하지 않는 파일입니다.")
            return {}

    def _file_write(channel_id: dict) -> None:
        with open("FileSys/NoticeChannel.bin", "wb") as fw:
            pickle.dump(channel_id, fw)

    def _msg_permissions(channel: TextChannel, user: Member) -> bool:
        if channel.permissions_for(user).send_messages:
            return True
        else:
            return False
