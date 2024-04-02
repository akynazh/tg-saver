# python3 -m utils.clean xxx
import sqlite3
import common
import sys

content = "-"
if len(sys.argv) > 1:
    content = sys.argv[1]

LOG = common.Logger(path_log_file=f"{common.PATH_ROOT}/log.txt").logger
CONN = sqlite3.connect(common.CFG.db_file)


CONN.cursor().execute(
    f"""
delete from t_tg_zh_coav_channel_1 where content = '{content}';
"""
)
res = (
    CONN.cursor()
    .execute(
        """
select changes();
"""
    )
    .fetchone()
)
CONN.commit()

LOG.info(f"clean t_tg_zh_coav_channel_1: {res[0]}")
