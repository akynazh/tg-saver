# python3 -m utils.check xxx
import sqlite3
import common
import sys

content = "-"
if len(sys.argv) > 1:
    content = sys.argv[1]

LOG = common.Logger(path_log_file=f"{common.PATH_ROOT}/log.txt").logger
CONN = sqlite3.connect(common.CFG.db_file)
res = (
    CONN.cursor()
    .execute(
        f"""
select count(*) from t_tg_zh_coav_channel_1 where content = '{content}';
"""
    )
    .fetchone()
)
LOG.info(f"clean t_tg_zh_coav_channel_1: {res}")
