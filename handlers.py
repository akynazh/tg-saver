import re
import sys
import sqlite3
import common
import logging
import telebot

LOG = logging.getLogger(__name__)


class FileHandler:
    tb_tg_chat_msg_id_name = "t_tg_chat_msg_id"
    tb_tg_chat_msg_id_sql = f"""CREATE TABLE IF NOT EXISTS {tb_tg_chat_msg_id_name} (
                                    chat_name TEXT,
                                    msg_id INTEGER,
                                    file_type INTEGER
                           );"""
    total_save_to_db_success = 0
    total_save_to_chat_success = 0
    pat_ugly_words = re.compile(r"\b(http|https|@|)\b")

    def __init__(self, file_type, from_chat, to_chat, db_file):
        self.file_type = file_type
        self.from_chat = from_chat
        self.to_chat = to_chat
        self.db_file = db_file

        self.tb_name = self.get_tb_name_by_file_type()
        self.create_tb_if_not_exists()

    def test_tb_files(self, limit=100):
        LOG.info(f"开始测试数据库文件, table={self.tb_name}, limit={limit}")
        if common.CFG.use_proxy == "1":
            telebot.apihelper.proxy = common.CFG.proxy_json
        bot = telebot.TeleBot(token=common.CFG.token)
        conn = None
        try:
            conn = self.get_db_conn()
            rows = conn.cursor().execute(f"select file_id from {self.tb_name} ORDER BY random() limit {int(limit)}") \
                .fetchall()
            LOG.info(f"待测试条数: {len(rows)}")
            fail = 0
            bot.send_message(chat_id=common.CFG.user_id, text="#测试开始")
            for row in rows:
                LOG.info(f"发送: {row[0]}")
                try:
                    self.test_send_file_to_chat(bot, row[0])
                except Exception as e:
                    LOG.error(f"发送失败: {e}")
                    fail += 1
            LOG.info(f"测试完成, 失败数: {fail}")
        except Exception as e:
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
                    f"SELECT chat_name FROM {self.tb_tg_chat_msg_id_name} WHERE chat_name = ? and file_type = ?",
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
            row = cur.execute(f"SELECT msg_id FROM {self.tb_tg_chat_msg_id_name} WHERE chat_name = ? and file_type = ?",
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
        i = 0
        try:
            conn = self.get_db_conn()
            max_id = -1
            while i < len(msg_list):
                msg = msg_list[i]
                max_id = max(msg.id, max_id)
                self.save_file_to_db(msg, conn.cursor())
                conn.commit()
                self.total_save_to_db_success += 1
                i += 1
            last_id = self.get_last_msg_id_from_db()
            if max_id > last_id:
                conn.cursor().execute(
                    f"UPDATE {self.tb_tg_chat_msg_id_name} SET msg_id = ? WHERE chat_name = ? and file_type = ?",
                    (max_id, self.from_chat, self.file_type))
                conn.commit()
                LOG.info(f"上次最新消息 id 为: {last_id}, 现更新为: {max_id}")
            LOG.info(f"成功保存记录到数据库, 已保存条数: {len(msg_list)}, 最大消息 id = {max_id}")
            return []
        except Exception as e:
            self.db_err(e)
            return msg_list[i:]
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
        if not cur.execute(f"SELECT file_id FROM {self.tb_name} where file_id = ?", (file_id,)).fetchone():
            cur.execute(f"INSERT INTO {self.tb_name}(file_id, content) VALUES(?, ?)",
                        (file_id, self.filter_ugly_content(self.get_file_content_from_msg(msg))))

    def filter_ugly_content(self, content):
        if self.pat_ugly_words.findall(content):
            return "hello world"
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
    def get_tb_name_by_file_type(self):
        return f"t_tg_v_{self.from_chat}"

    def get_file_id_from_msg(self, msg):
        return msg.video.file_id

    def get_file_content_from_msg(self, msg):
        return msg.caption

    async def save_file_to_chat(self, app, msg):
        await app.send_video(chat_id=self.to_chat, video=self.get_file_id_from_msg(msg))

    def test_send_file_to_chat(self, bot, file_id):
        bot.send_video(chat_id=common.CFG.user_id, video=file_id)


class PhotoHandler(FileHandler):
    def get_tb_name_by_file_type(self):
        return f"t_tg_p_{self.from_chat}"

    def get_file_id_from_msg(self, msg):
        return msg.photo.file_id

    def get_file_content_from_msg(self, msg):
        return msg.caption

    async def save_file_to_chat(self, app, msg):
        await app.send_photo(chat_id=self.to_chat, photo=self.get_file_id_from_msg(msg))

    def test_send_file_to_chat(self, bot, file_id):
        bot.send_photo(chat_id=common.CFG.user_id, photo=file_id)


class DocumentHandler(FileHandler):
    def get_tb_name_by_file_type(self):
        return f"t_tg_d_{self.from_chat}"

    def get_file_id_from_msg(self, msg):
        return msg.document.file_id

    def get_file_content_from_msg(self, msg):
        return msg.document.file_name

    async def save_file_to_chat(self, app, msg):
        await app.send_document(chat_id=self.to_chat, document=self.get_file_id_from_msg(msg))

    def test_send_file_to_chat(self, bot, file_id):
        bot.send_document(chat_id=common.CFG.user_id, document=file_id)


class CustomHandlerType:
    SGP_VIDEO = 1


class SgpVideoHandler(VideoHandler):
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
        c1 = cur.execute(f"SELECT file_id FROM {self.tb_name} where file_id = ?", (file_id,)).fetchone()
        c2 = cur.execute(f"SELECT av_id FROM {self.tb_name} where av_id = ?", (ids[0],)).fetchone()
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
