# python3 -m utils.clean xxx
import sqlite3
import common
import sys

LOG = common.Logger(path_log_file=f"{common.PATH_ROOT}/log.txt").logger
CONN = sqlite3.connect(common.CFG.db_file)

if len(sys.argv) > 1:
    CONN.cursor().execute(
        f"""
    delete from t_tg_zh_coav_channel_1 where instr(content, '{sys.argv[1]}');
    """
    )
else:
    CONN.cursor().execute(
        f"""
    delete from t_tg_zh_coav_channel_1 where content = '-';
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
