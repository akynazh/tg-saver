import re
from handlers import VideoHandler
from pyrogram.types import Message


class JavHandler(VideoHandler):
    C_TYPE = 101
    AV_PAT = re.compile(r"[a-z0-9]+[-_](?:ppv-)?[a-z0-9]+")

    def save_file_to_db(self, msg, ori_msg_id):
        file_id = self.get_file_id_from_msg(msg)
        ids = self.AV_PAT.findall(self.get_file_content_from_msg(msg).lower())
        self.conn.cursor().execute(f"""INSERT INTO {self.tb_name}(
        av_id, msg_id, file_id, file_type, content, ori_chat_name, ori_msg_id)
                        VALUES(?, ?, ?, ?, ?, ?, ?)""",
                                   (ids[0], msg.id, file_id, self.file_type, ids[0], self.from_chat, ori_msg_id))
        self.conn.commit()

    def check_if_content_is_ok(self, msg) -> bool:
        return self.AV_PAT.findall(self.get_file_content_from_msg(msg).lower()) != []

    async def save_file_to_chat(self, file_id, content) -> Message:
        return await self.APP.send_video(chat_id=self.to_chat, video=file_id,
                                         caption=self.AV_PAT.findall(content.lower())[0])
