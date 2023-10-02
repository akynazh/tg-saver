import sqlite3
import time

import meilisearch
import common
from pyrogram.types import Message


class FileHandler:
    APP = None
    C_TYPE = 0

    def __init__(self, file_type, from_chat, to_chat, enable_ms):
        self.file_type = file_type
        self.from_chat = from_chat
        self.to_chat = to_chat
        self.enable_ms = enable_ms

        self.tb_name = f"t_tg_{self.to_chat}"
        self.conn = sqlite3.connect(common.CFG.db_file)
        self.ms = meilisearch.Client(common.CFG.ms_addr, common.CFG.ms_key)
        self.init_last_msg_id()

    def init_last_msg_id(self):
        if not self.conn.cursor().execute(
                f"SELECT chat_name FROM t_tg_last_msg_id WHERE chat_name = ? AND ori_chat_name = ? AND file_type = ?",
                (self.to_chat, self.from_chat, self.file_type)).fetchone():
            self.conn.cursor().execute(
                f"INSERT INTO t_tg_last_msg_id(chat_name, ori_chat_name, file_type, ori_min_msg_id, ori_max_msg_id) \
                VALUES(?, ?, ?, ?, ?)",
                (self.to_chat, self.from_chat, self.file_type, -1, -1))
            self.conn.commit()

    def get_last_msg_id(self, get_max=False) -> int:
        col_name = "ori_max_msg_id" if get_max else "ori_min_msg_id"
        msg_id = self.conn.cursor().execute(
            f"SELECT {col_name} FROM t_tg_last_msg_id WHERE chat_name = ? AND ori_chat_name = ? AND file_type = ?",
            (self.to_chat, self.from_chat, self.file_type)).fetchone()[0]
        return msg_id if msg_id != -1 else 0

    def update_last_msg_id(self, msg_id, update_max=False):
        col_name = "ori_max_msg_id" if update_max else "ori_min_msg_id"
        self.conn.cursor().execute(
            f"UPDATE t_tg_last_msg_id SET {col_name} = ? WHERE chat_name = ? AND ori_chat_name = ? AND file_type = ?",
            (msg_id, self.to_chat, self.from_chat, self.file_type))
        self.conn.commit()

    def get_file_content_from_msg(self, msg) -> str:
        return msg.caption if msg.caption else "-"

    def get_file_id_from_msg(self, msg) -> str:
        pass

    async def save_file(self, msg):
        content = self.get_file_content_from_msg(msg)
        new_msg = await self.save_file_to_chat(self.get_file_id_from_msg(msg), content)
        self.save_file_to_db(new_msg, msg.id)
        if self.enable_ms:
            self.save_file_to_ms(self.get_file_id_from_msg(new_msg), content)

    def save_file_to_db(self, msg, ori_msg_id):
        file_id = self.get_file_id_from_msg(msg)
        content = self.get_file_content_from_msg(msg)
        self.conn.cursor().execute(f"""INSERT INTO {self.tb_name}(msg_id, file_id, file_type, content, ori_chat_name, ori_msg_id)
                        VALUES(?, ?, ?, ?, ?, ?)""",
                                   (msg.id, file_id, self.file_type, content, self.from_chat, ori_msg_id))
        self.conn.commit()

    def save_file_to_ms(self, file_id, content):
        doc = {"id": file_id, "content": content}
        self.ms.index(self.to_chat).add_documents([doc])

    async def save_file_to_chat(self, file_id, content) -> Message:
        pass


class VideoHandler(FileHandler):
    def get_file_id_from_msg(self, msg) -> str:
        return msg.video.file_id

    async def save_file_to_chat(self, file_id, content) -> Message:
        return await self.APP.send_video(chat_id=self.to_chat, video=file_id, caption=content)


class PhotoHandler(FileHandler):
    def get_file_id_from_msg(self, msg) -> str:
        return msg.photo.file_id

    async def save_file_to_chat(self, file_id, content) -> Message:
        return await self.APP.send_photo(chat_id=self.to_chat, photo=file_id, caption=content)


class DocumentHandler(FileHandler):
    def get_file_id_from_msg(self, msg) -> str:
        return msg.document.file_id

    async def save_file_to_chat(self, file_id, content) -> Message:
        return await self.APP.send_document(chat_id=self.to_chat, document=file_id, caption=content)
