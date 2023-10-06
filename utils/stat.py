import sqlite3
import common
from pyrogram import Client, enums

LOG = common.Logger(path_log_file=f"{common.PATH_ROOT}/log.txt").logger
CONN = sqlite3.connect(common.CFG.db_file)
result = ""


def get_count(chat_name):
    global result

    c = CONN.cursor().execute(f"""
select count(*) from t_tg_{chat_name};
""").fetchone()
    info = f"{chat_name}: {c[0]}"
    result += info + "\n"
    LOG.info(f"{chat_name}: {c[0]}")


def send_res():
    with Client(common.SESSION_FILE, common.CFG.api_id, common.CFG.api_hash,
                proxy=common.CFG.proxy_pyrogram_json,
                parse_mode=enums.ParseMode.DISABLED) as app:
        app.send_message("jackbryant286", result)


get_count("zh_coav_channel_1")
get_count("zh_sgp_av_channel_1")
get_count("zh_jav_channel_1_i")
send_res()
