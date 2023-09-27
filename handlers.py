import logging
import re
import sqlite3
import sys
import telebot
import common

LOG = logging.getLogger(__name__)


class FileHandler:
    name = "File"
    tb_tg_chat_msg_id_name = "t_tg_chat_msg_id"
    tb_tg_chat_msg_id_sql = f"""CREATE TABLE IF NOT EXISTS {tb_tg_chat_msg_id_name} (
                                    chat_name TEXT,
                                    msg_id INTEGER,
                                    file_type INTEGER
                           );"""
    success_count = 0
    pat_ugly_words = re.compile(r"\b(http|https|@)\b")

    def __init__(self, file_type, from_chat, to_chat, db_file):
        self.file_type = file_type
        self.from_chat = from_chat
        self.to_chat = to_chat
        self.db_file = db_file

        self.tb_name = self.get_tb_name_by_file_type()
        self.create_tb_if_not_exists()

    def clear_tb_files(self):
        conn = None
        try:
            LOG.info(f"开始清除数据库文件, table={self.tb_name}")
            conn = self.get_db_conn()
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {self.tb_name}")
            cur.execute(f"DELETE FROM {self.tb_tg_chat_msg_id_name} WHERE chat_name = ? AND file_type = ?",
                        (self.from_chat, self.file_type))
            conn.commit()
            LOG.info(f"{self.tb_name} 和 {self.tb_tg_chat_msg_id_name} 表中相关数据已清除")
        except Exception as e:
            self.db_err(e)
            return
        finally:
            if conn:
                conn.close()

    def test_tb_files(self, limit=100):
        if common.CFG.use_proxy == "1":
            telebot.apihelper.proxy = common.CFG.proxy_json
        bot = telebot.TeleBot(token=common.CFG.token)
        conn = None
        try:
            conn = self.get_db_conn()
            rows = conn.cursor().execute(f"SELECT file_id FROM {self.tb_name} ORDER BY random() LIMIT {int(limit)}") \
                .fetchall()
            fail = 0
            start_msg = f"#测试# 开始测试, 测试目标={self.tb_name}, 测试数={limit}"
            LOG.info(start_msg)
            bot.send_message(chat_id=common.CFG.test_id, text=start_msg)
            for row in rows:
                LOG.info(f"发送: {row[0]}")
                try:
                    self.test_send_file_to_chat(bot, row[0])
                except Exception as e:
                    LOG.error(f"发送失败: {e}")
                    fail += 1
            end_msg = f"#测试# 测试完成, 测试数={limit}, 失败数={fail}"
            LOG.info(end_msg)
            if fail != 0:
                bot.send_message(chat_id=common.CFG.admin_id, text=end_msg)
            bot.send_message(chat_id=common.CFG.test_id, text=end_msg)
        except Exception as e:
            bot.send_message(chat_id=common.CFG.admin_id, text=f"#测试# 测试失败, 数据库异常, 请检查!")
            self.db_err(e)
            return
        finally:
            if conn:
                conn.close()

    def db_err(self, e):
        LOG.error(f"数据库出错: {e}")

    def get_db_conn(self):
        return sqlite3.connect(self.db_file)

    def create_tb_if_not_exists(self):
        conn = None
        try:
            conn = self.get_db_conn()
            cur = conn.cursor()
            cur.execute(self.tb_tg_chat_msg_id_sql)
            cur.execute(self.get_create_sql())
            conn.commit()
            if not cur.execute(
                    f"SELECT chat_name FROM {self.tb_tg_chat_msg_id_name} WHERE chat_name = ? AND file_type = ?",
                    (self.from_chat, self.file_type)).fetchone():
                cur.execute(f"INSERT INTO {self.tb_tg_chat_msg_id_name}(chat_name, msg_id, file_type) VALUES(?, ?, ?)",
                            (self.from_chat, -1, self.file_type))
            LOG.info(f"{self.tb_name} 和 {self.tb_tg_chat_msg_id_name} 表已就绪")
            conn.commit()
        except Exception as e:
            self.db_err(e)
            sys.exit(1)
        finally:
            if conn:
                conn.close()

    def get_last_msg_id_from_db(self):
        conn = None
        try:
            conn = self.get_db_conn()
            cur = conn.cursor()
            row = cur.execute(f"SELECT msg_id FROM {self.tb_tg_chat_msg_id_name} WHERE chat_name = ? AND file_type = ?",
                              (self.from_chat, self.file_type)).fetchone()
            return row[0] if row else -1
        except Exception as e:
            self.db_err(e)
            return -1
        finally:
            if conn:
                conn.close()

    async def batch_save_file_to_db(self, msg_list: list):
        LOG.info(f"开始保存记录到数据库, 即将保存条数: {len(msg_list)}")
        conn = None
        try:
            conn = self.get_db_conn()
            max_id = -1
            for msg in msg_list:
                max_id = max(msg.id, max_id)
                self.save_file_to_db(msg, conn.cursor())
                conn.commit()
                self.success_count += 1
            last_id = self.get_last_msg_id_from_db()
            if max_id > last_id:
                conn.cursor().execute(
                    f"UPDATE {self.tb_tg_chat_msg_id_name} SET msg_id = ? WHERE chat_name = ? AND file_type = ?",
                    (max_id, self.from_chat, self.file_type))
                conn.commit()
        except Exception as e:
            self.db_err(e)
        finally:
            if conn:
                conn.close()

    def get_create_sql(self):
        return f"""CREATE TABLE IF NOT EXISTS {self.tb_name} (
                                                file_id TEXT PRIMARY KEY,
                                                content TEXT
              );"""

    def save_file_to_db(self, msg, cur):
        file_id = self.get_file_id_from_msg(msg)
        if not cur.execute(f"SELECT file_id FROM {self.tb_name} WHERE file_id = ?", (file_id,)).fetchone():
            cur.execute(f"INSERT INTO {self.tb_name}(file_id, content) VALUES(?, ?)",
                        (file_id, self.filter_ugly_content(str(self.get_file_content_from_msg(msg)))))

    def filter_ugly_content(self, content):
        if self.pat_ugly_words.findall(content):
            return "-"
        return content

    def get_tb_name_by_file_type(self):
        pass

    def get_file_id_from_msg(self, msg):
        pass

    def get_file_content_from_msg(self, msg):
        pass

    async def save_file_to_chat(self, app, msg):
        pass

    def test_send_file_to_chat(self, bot, file_id):
        pass


class VideoHandler(FileHandler):
    name = "Video"

    def get_tb_name_by_file_type(self):
        return f"t_tg_v_{self.from_chat}"

    def get_file_id_from_msg(self, msg):
        return msg.video.file_id

    def get_file_content_from_msg(self, msg):
        return msg.caption if msg.caption else "-"

    async def save_file_to_chat(self, app, msg):
        await app.send_video(chat_id=self.to_chat, video=self.get_file_id_from_msg(msg))

    def test_send_file_to_chat(self, bot, file_id):
        bot.send_video(chat_id=common.CFG.test_id, video=file_id)


class PhotoHandler(FileHandler):
    name = "Photo"

    def get_tb_name_by_file_type(self):
        return f"t_tg_p_{self.from_chat}"

    def get_file_id_from_msg(self, msg):
        return msg.photo.file_id

    def get_file_content_from_msg(self, msg):
        return msg.caption if msg.caption else "-"

    async def save_file_to_chat(self, app, msg):
        await app.send_photo(chat_id=self.to_chat, photo=self.get_file_id_from_msg(msg))

    def test_send_file_to_chat(self, bot, file_id):
        bot.send_photo(chat_id=common.CFG.test_id, photo=file_id)


class DocumentHandler(FileHandler):
    name = "Document"

    def get_tb_name_by_file_type(self):
        return f"t_tg_d_{self.from_chat}"

    def get_file_id_from_msg(self, msg):
        return msg.document.file_id

    def get_file_content_from_msg(self, msg):
        return msg.document.file_name if msg.document.file_name else "-"

    async def save_file_to_chat(self, app, msg):
        await app.send_document(chat_id=self.to_chat, document=self.get_file_id_from_msg(msg))

    def test_send_file_to_chat(self, bot, file_id):
        bot.send_document(chat_id=common.CFG.test_id, document=file_id)


class CustomHandlerType:
    SGP_VIDEO = 1


class SgpVideoHandler(VideoHandler):
    name = "SgpVideo"
    AV_PAT = re.compile(r"[a-z0-9]+[-_](?:ppv-)?[a-z0-9]+")

    def get_create_sql(self):
        return f"""CREATE TABLE IF NOT EXISTS {self.tb_name} (
                                        av_id TEXT PRIMARY KEY,
                                        title TEXT,
                                        file_id TEXT UNIQUE
              );"""

    def save_file_to_db(self, msg, cur):
        file_id = self.get_file_id_from_msg(msg)
        title = self.get_file_content_from_msg(msg)
        ids = SgpVideoHandler.AV_PAT.findall(title.lower())
        if not ids or len(ids) == 0:
            return
        c1 = cur.execute(f"SELECT file_id FROM {self.tb_name} WHERE file_id = ?", (file_id,)).fetchone()
        c2 = cur.execute(f"SELECT av_id FROM {self.tb_name} WHERE av_id = ?", (ids[0],)).fetchone()
        if not c1 and not c2:
            cur.execute(f"INSERT INTO {self.tb_name}(av_id, title, file_id) VALUES(?, ?, ?)",
                        (ids[0], title, file_id))


class FileHandlerFactory:
    handler_map = {
        common.FileType.VIDEO: VideoHandler,
        common.FileType.PHOTO: PhotoHandler,
        common.FileType.DOCUMENT: DocumentHandler
    }
    c_handler_map = {
        CustomHandlerType.SGP_VIDEO: SgpVideoHandler
    }

    def __init__(self, file_type, from_chat, to_chat, db_file, c_type=0):
        self.file_type = file_type
        self.from_chat = from_chat
        self.to_chat = to_chat
        self.db_file = db_file
        self.c_type = c_type

    def get_handler(self):
        if self.c_type == 0:
            return self.handler_map[self.file_type](self.file_type, self.from_chat, self.to_chat,
                                                    self.db_file)
        else:
            return self.c_handler_map[self.c_type](self.file_type, self.from_chat, self.to_chat, self.db_file)
