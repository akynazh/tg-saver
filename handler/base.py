import sqlite3
import time
from typing import Type

import meilisearch
import common
from pyrogram.types import Message


class FileHandler:
    APP = None
    C_TYPE = 0
    UGLY_WORDS = ["@", "http", "https", "群", "赌", "搜", "网址"]

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
        new_msg = await self.save_file_to_chat(msg)
        self.save_file_to_db(new_msg, msg)
        if self.enable_ms:
            self.save_file_to_ms(new_msg)

    def save_file_to_db(self, new_msg, old_msg):
        self.conn.cursor().execute(f"""INSERT INTO {self.tb_name}(msg_id, file_id, file_type, content, ori_chat_name, ori_msg_id)
                        VALUES(?, ?, ?, ?, ?, ?)""",
                                   (new_msg.id, self.get_file_id_from_msg(new_msg), self.file_type,
                                    self.get_file_content_from_msg(new_msg), self.from_chat, old_msg.id))
        self.conn.commit()

    def save_file_to_ms(self, msg):
        doc = {"id": self.get_file_id_from_msg(msg), "content": self.get_file_content_from_msg(msg)}
        self.ms.index(self.to_chat).add_documents([doc])

    async def save_file_to_chat(self, msg) -> Message:
        pass

    def check_if_file_is_ok(self, msg) -> bool:
        return self.check_if_has_no_markup(msg) \
            and self.check_if_content_is_ok(msg)

    def check_if_has_no_markup(self, msg):
        return True if not msg.reply_markup else False

    def check_if_content_is_ok(self, msg) -> bool:
        l_content = self.get_file_content_from_msg(msg).lower()
        return True if not any(word in l_content for word in self.UGLY_WORDS) else False


class VideoHandler(FileHandler):
    def get_file_id_from_msg(self, msg) -> str:
        return msg.video.file_id

    async def save_file_to_chat(self, msg) -> Message:
        return await self.APP.send_video(chat_id=self.to_chat, video=self.get_file_id_from_msg(msg),
                                         caption=self.get_file_content_from_msg(msg))


class PhotoHandler(FileHandler):
    def get_file_id_from_msg(self, msg) -> str:
        return msg.photo.file_id

    async def save_file_to_chat(self, msg) -> Message:
        return await self.APP.send_photo(chat_id=self.to_chat, photo=self.get_file_id_from_msg(msg),
                                         caption=self.get_file_content_from_msg(msg))


class DocumentHandler(FileHandler):
    def get_file_id_from_msg(self, msg) -> str:
        return msg.document.file_id

    async def save_file_to_chat(self, msg) -> Message:
        return await self.APP.send_document(chat_id=self.to_chat, document=self.get_file_id_from_msg(msg),
                                            caption=self.get_file_content_from_msg(msg))


class AudioHandler(FileHandler):
    def get_file_id_from_msg(self, msg) -> str:
        return msg.audio.file_id

    async def save_file_to_chat(self, msg) -> Message:
        return await self.APP.send_audio(chat_id=self.to_chat, audio=self.get_file_id_from_msg(msg),
                                         caption=self.get_file_content_from_msg(msg))


class MediaGroupHandler(FileHandler):
    sub_handler = None

    def get_file_type(self, msg):
        if msg.video:
            return common.FileTypes.VIDEO
        elif msg.photo:
            return common.FileTypes.PHOTO
        elif msg.document:
            return common.FileTypes.DOCUMENT
        elif msg.audio:
            return common.FileTypes.AUDIO

    async def save_file_to_chat(self, msg) -> Message:
        if msg.video:
            return await self.APP.send_video(chat_id=self.to_chat, video=self.get_file_id_from_msg(msg))
        elif msg.photo:
            return await self.APP.send_photo(chat_id=self.to_chat, photo=self.get_file_id_from_msg(msg))
        elif msg.document:
            return await self.APP.send_document(chat_id=self.to_chat, document=self.get_file_id_from_msg(msg))
        elif msg.audio:
            return await self.APP.send_audio(chat_id=self.to_chat, audio=self.get_file_id_from_msg(msg))

    def get_file_id_from_msg(self, msg) -> str:
        if msg.video:
            return msg.video.file_id
        elif msg.photo:
            return msg.photo.file_id
        elif msg.document:
            return msg.document.file_id
        elif msg.audio:
            return msg.audio.file_id

    def save_file_to_db(self, new_msg, old_msg):
        self.conn.cursor().execute(f"""INSERT INTO {self.tb_name}(media_group_id, msg_id, file_id, file_type, 
                                        ori_chat_name, ori_msg_id) VALUES(?, ?, ?, ?, ?, ?)""",
                                   (old_msg.media_group_id, new_msg.id, self.get_file_id_from_msg(new_msg),
                                    self.get_file_type(old_msg), self.from_chat, old_msg.id))
        content = old_msg.caption
        if content:
            i_id = self.gen_id_from_content(content)
            if not self.conn.cursor().execute(f"""SELECT id FROM {self.tb_name}_i WHERE id = ?""", (i_id,)).fetchone():
                self.conn.cursor().execute(
                    f"""INSERT INTO {self.tb_name}_i(id, media_group_id, ori_chat_name, content) VALUES (?, ?, ?, ?)""",
                    (i_id, old_msg.media_group_id, self.from_chat, content))
        self.conn.commit()

    def gen_id_from_content(self, content) -> str:
        return str(time.time())
