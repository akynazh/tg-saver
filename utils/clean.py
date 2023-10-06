import sqlite3
import common

conn = sqlite3.connect(common.CFG.db_file)
conn.cursor().execute("""
delete from t_tg_zh_coav_channel_1 where content = '-';
""")
res = conn.cursor().execute("""
select changes();
""").fetchone()
print(f"clean t_tg_zh_coav_channel_1: {res[0]}")
conn.commit()
