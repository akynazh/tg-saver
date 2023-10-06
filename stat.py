import sqlite3
import common

CONN = sqlite3.connect(common.CFG.db_file)


def get_count(chat_name) -> int:
    c = CONN.cursor().execute(f"""
select count(*) from t_tg_{chat_name};
""").fetchone()
    print(f"{chat_name}: {c[0]}")


get_count("zh_coav_channel_1")
get_count("zh_sgp_av_channel_1")
get_count("zh_jav_channel_1")
