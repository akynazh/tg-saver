import sqlite3
import sys
import time

import meilisearch
import common

CLI = meilisearch.Client(common.CFG.ms_addr, common.CFG.ms_key)


def trans_to_ms(chat_name):
    print(f"Transfer {chat_name}...")
    data = sqlite3.connect(common.CFG.db_file).cursor().execute(
        f"SELECT file_id, content FROM t_tg_{chat_name}").fetchall()
    task_info = CLI.index(chat_name).add_documents([{"id": item[0], "content": item[1]} for item in data])
    while CLI.get_task(task_info.task_uid).status != "succeeded":
        time.sleep(1)
    print(CLI.get_task(task_info.task_uid))


if __name__ == '__main__':
    trans_to_ms(sys.argv[1])
