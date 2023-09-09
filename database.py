import sqlite3
import logging

LOG = logging.getLogger(__name__)


class BotDb:
    TYPE_SGP = 1
    TYPE_CAV = 2

    def __init__(self, path_db_file: str):
        self.path_db_file = path_db_file

    def get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path_db_file)

    def select_cur_msg_id(self, type: int) -> int:
        conn = None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            if type == BotDb.TYPE_SGP:
                cur.execute("SELECT max(msg_id) FROM t_tg_sgp")
            elif type == BotDb.TYPE_CAV:
                cur.execute("SELECT max(msg_id) FROM t_tg_cav")
            cur_id = cur.fetchone()[0]
            return cur_id if cur_id else -1
        except Exception as e:
            LOG.error(e)
        finally:
            if conn:
                conn.close()

    def insert_sgp_av(self, sgp_av, cur):
        cur.execute("INSERT INTO t_tg_sgp(av_id, title, file_id, msg_id) VALUES(?, ?, ?, ?)",
                    (sgp_av["av_id"], sgp_av["title"], sgp_av["file_id"], sgp_av["msg_id"]))

    def insert_cav(self, cav, cur):
        cur.execute("INSERT INTO t_tg_cav(title, file_id, msg_id) VALUES(?, ?, ?)",
                    (cav["title"], cav["file_id"], cav["msg_id"]))

    def batch_insert_medias(self, media_list: list, media_type: int):
        conn = None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            for v in media_list:
                if media_type == BotDb.TYPE_SGP:
                    self.insert_sgp_av(v, cur)
                elif media_type == BotDb.TYPE_CAV:
                    self.insert_cav(v, cur)
            conn.commit()
            return True
        except Exception as e:
            LOG.error(e)
        finally:
            if conn:
                conn.close()
