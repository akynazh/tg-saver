import time
import sys
from saver import Saver
from database import BotDb
import asyncio
import common
import telebot

LOG = common.LOG
CFG = common.CFG


# python3 main.py save_video @DoO_o @zh_testt_bot 5
# python3 main.py save_video @DoO_o @zh_jav_plus_bot 5
def save_video(from_chat, to_chat, limit=100):
    LOG.info(f"开始保存视频: from_chat={from_chat}, to_chat={to_chat}, limit={limit}")
    saver = Saver(from_chat=from_chat, to_chat=to_chat,
                  need_send=True,
                  media_type=BotDb.CHAT_TYPE_MAP[from_chat],
                  session_file=common.SESSION_FILE,
                  api_id=CFG.api_id,
                  api_hash=CFG.api_hash,
                  db_file=CFG.db_file,
                  proxies=CFG.proxy_pyrogram_json,
                  limit=int(limit)
                  )
    asyncio.run(saver.save_video())


# python3 main.py test_tb_files t_tg_sgp 5
# python3 main.py test_tb_files t_tg_cav 5
def test_tb_files(tb, limit=100):
    LOG.info(f"开始测试数据库文件, table={tb}, limit={limit}")
    if CFG.use_proxy == "1":
        telebot.apihelper.proxy = CFG.proxy_json
    bot = telebot.TeleBot(token=CFG.token)
    db = BotDb(CFG.db_file)
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute(f"select file_id from {tb} limit {int(limit)}")
    rows = cur.fetchall()
    conn.close()
    LOG.info(f"条数: {len(rows)}")
    fail = 0
    for row in rows:
        LOG.info(f"发送: {row[0]}")
        try:
            bot.send_video(chat_id=CFG.user_id, video=row[0])
            time.sleep(1)
        except Exception:
            fail += 1
    LOG.info(f"测试完成, 失败数: {fail}")


# python3 main.py clear_tb_files t_tg_sgp
def clear_tb_files(tb):
    LOG.info(f"开始清空表文件, table={tb}")
    db = BotDb(CFG.db_file)
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute(f"select * from {tb}")
    rows = cur.fetchall()
    LOG.info(f"现有条数: {len(rows)}")
    cur.execute(f"delete from {tb} where 1=1")
    conn.commit()
    cur.execute(f"select * from {tb}")
    rows = cur.fetchall()
    conn.close()
    if len(rows) == 0:
        LOG.info(f"表文件已清空")
    else:
        LOG.info(f"表文件未清空, 未清空条数: {len(rows)}")


if __name__ == "__main__":
    LOG.info(f"测试函数: {sys.argv[1]}")
    if len(sys.argv) > 2:
        LOG.info(f"参数列表: {sys.argv[2:]}")
        globals()[sys.argv[1]](*sys.argv[2:])
    else:
        globals()[sys.argv[1]]()
