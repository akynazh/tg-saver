import sys
import time
import random
import common
import asyncio
import argparse
from pyrogram import Client, enums
from handlers import FileHandlerFactory

LOG = common.Logger(path_log_file=f"{common.PATH_ROOT}/log.txt").logger


class Saver:
    app = None
    tasks = []
    success_msg_list = []
    fail_msg_list = []

    def __init__(self, from_chat: str, to_chat: str, need_save_to_chat: bool, need_save_to_db: bool, file_type: int,
                 session_file: str, api_id: int, api_hash: str, db_file: str, need_test=False, test_only=False,
                 max_test_count=100, renew=False, proxies=None, limit=0, retry_times=10, c_type=0,
                 task_count_per_time=100):
        """TgChat 文件保存器

        :param from_chat: 抓取文件的目标 chat
        :param to_chat: 文件 id 保存的目标 chat
        :param need_save_to_chat: 是否需要保存文件 id 到 chat
        :param need_save_to_db: 是否需要保存文件到数据库
        :param file_type: 文件类型 [FileType]
        :param session_file: session 文件地址
        :param api_id: tg api id
        :param api_hash: tg api hash
        :param db_file: sqlite3 数据库文件
        :param need_test: 完成后是否需要测试
        :param test_only: 是否只测试
        :param max_test_count: 最大测试条数
        :param renew: 是否重新获取(忽略上次获取到的最新消息 id)
        :param proxies: 代理 dict
        :param limit: 消息限制数, 默认 0 即不限制
        :param retry_times: 重试抓取文件的次数, 默认 10
        :param c_type: 自定义 handler 的类型 [CustomHandlerType], 默认为 0, 不进行自定义
        :param task_count_per_time: 每次保存文件 id 到 chat 的任务数, 默认 100
        """
        self.from_chat = from_chat
        self.to_chat = to_chat
        self.need_save_to_chat = need_save_to_chat
        self.need_save_to_db = need_save_to_db
        self.file_type = file_type
        self.session_file = session_file
        self.api_id = api_id
        self.api_hash = api_hash
        self.db_file = db_file
        self.need_test = need_test
        self.test_only = test_only
        self.max_test_count = max_test_count
        self.renew = renew
        self.proxies = proxies
        self.limit = limit
        self.retry_times = retry_times
        self.c_type = c_type
        self.task_count_per_time = task_count_per_time

        self.file_type_tag = common.FileType.FILE_TAG_MAP[self.file_type]
        self.handler = FileHandlerFactory(self.file_type, self.from_chat, self.to_chat, self.db_file,
                                          self.c_type).get_handler()

    async def run_save_file_to_chat_tasks(self):
        LOG.info(f"开始保存文件 id 到 chat, 任务数: {len(self.tasks)}, 发送中......")
        start = time.time()
        res_list = await asyncio.gather(*self.tasks)
        end = time.time()
        count_fail = len(list(filter(lambda x: not x, res_list)))
        LOG.info(f"完成任务, 失败数: {count_fail}, 耗时: {end - start}s")
        self.tasks = []

    async def retry_save_file_to_chat_tasks(self):
        cur_retry_times = 0
        while len(self.fail_msg_list) > 0:
            if cur_retry_times == self.retry_times:
                LOG.error(
                    f"重试次数已经达到 {self.retry_times} 次, 停止重试, 剩余保存失败的文件数: {len(self.fail_msg_list)}")
                break
            if cur_retry_times >= 3:
                sleep_time = cur_retry_times * 60
                LOG.warning(f"重试次数过多, 进入休眠, 休眠时间: {sleep_time}s")
                await asyncio.sleep(sleep_time)
            LOG.warning(
                f"重试保存文件 id 到 chat, 剩余保存失败的文件数: {len(self.fail_msg_list)}, 已重试次数: {cur_retry_times}, 开始重试...")
            self.tasks = [asyncio.create_task(self.save_file_to_chat(msg)) for msg in self.fail_msg_list]
            self.fail_msg_list = []
            await self.run_save_file_to_chat_tasks()
            cur_retry_times += 1

    async def save_file_to_chat(self, msg):
        await asyncio.sleep(random.randint(1, 50))
        try:
            await self.handler.save_file_to_chat(self.app, msg)
            self.handler.total_save_to_chat_success += 1
            if self.need_save_to_db:
                self.success_msg_list.append(msg)
            LOG.info(f"成功保存文件 id:{self.handler.get_file_id_from_msg(msg)} 到 {self.to_chat}")
            await asyncio.sleep(random.randint(1, 50))
            return True
        except Exception as e:
            self.fail_msg_list.append(msg)
            LOG.error(f"保存文件 id 到 {self.to_chat} 失败: {e}")
            await asyncio.sleep(random.randint(1, 50))
            return False

    async def save_file_to_db(self):
        self.success_msg_list = await self.handler.batch_save_file_to_db(self.success_msg_list)

    async def try_to_save_to_chat(self, msg):
        # 如果需要保存到 chat, 任务数达到一定值开始保存到 chat, 失败数达到一定值开始重试
        if self.need_save_to_chat:
            self.tasks.append(asyncio.create_task(self.save_file_to_chat(msg)))
            if len(self.tasks) >= self.task_count_per_time:
                await self.run_save_file_to_chat_tasks()
            if len(self.fail_msg_list) >= 100:
                await self.retry_save_file_to_chat_tasks()
        # 若不需要保存到 chat, 但是需要保存到数据库, 则将消息直接存入成功消息列表
        elif self.need_save_to_db:
            self.success_msg_list.append(msg)

    async def try_to_save_to_db(self):
        # 如果需要保存到数据库, 当成功消息数量达到一定值时, 则将消息存入数据库, 当剩余成功消息数量大于一定值需要报错退出
        if self.need_save_to_db:
            if len(self.success_msg_list) >= 500:
                await self.save_file_to_db()
            if len(self.success_msg_list) >= 1500:
                LOG.error("未能成功保存到数据库的消息过多, 退出程序!")
                sys.exit(1)

    def filter_file_by_type(self, msg):
        # 如果不是目标文件类型则跳过 todo: audio document how to check?
        if not msg.media or str(msg.media) != self.file_type_tag:
            return False
        return True

    def check_if_has_new_msg(self, msg, old_cur_id):
        # 没有更新的消息
        if old_cur_id > msg.id:
            LOG.warning(f"没有更新的消息: {old_cur_id} >= {msg.id}, 退出程序~")
            return False
        return True

    def test(self):
        self.handler.test_tb_files(self.max_test_count)

    def log_start(self):
        LOG.info(f"""

##################################################################
$ 启动 Tg-saver ^_^ [Made by jzh: https://github.com/akynazh/tg-saver]
$ 抓取目标 chat: {self.from_chat} 
$ 保存目标 chat: {self.to_chat}
$ 保存文件类型: {common.FileType.FILE_TAG_MAP[self.file_type]}
$ 是否保存到 chat: {self.need_save_to_chat}
$ 是否保存到数据库: {self.need_save_to_db}
$ 是否重新获取: {self.renew}
$ 是否测试: {self.need_test}
$ 是否只进行测试: {self.test_only}
$ 最大测试条数: {self.max_test_count}
$ 获取条数限制: {self.limit}
$ 代理信息: {self.proxies}
$ 数据库地址: {self.db_file}
$ Session 文件地址: {self.session_file}
##################################################################
""")

    def log_end(self, count_new_file=0):
        LOG.info(f"""

##################################################################
$ 完成任务! ^_^
$ 得到文件总数: {count_new_file}
$ 成功保存文件 id 到 chat 的数目: {self.handler.total_save_to_chat_success}
$ 成功保存文件到数据库的数目: {self.handler.total_save_to_db_success}
$ 未保存文件 id 到 chat 的数目: {len(self.fail_msg_list)}
$ 未保存文件到数据库的数目: {len(self.success_msg_list)}
##################################################################
""")

    async def save(self):
        self.log_start()
        if self.test_only:
            self.test()
            return
        count_new_file = 0
        old_cur_id = -1 if self.renew else self.handler.get_last_msg_id_from_db()
        async with Client(self.session_file, self.api_id, self.api_hash, proxy=self.proxies,
                          parse_mode=enums.ParseMode.DISABLED) as app:
            self.app = app
            has_update = True
            async for msg in app.get_chat_history(self.from_chat, limit=self.limit):
                if not self.check_if_has_new_msg(msg, old_cur_id):
                    has_update = False
                    break
                if not self.filter_file_by_type(msg):
                    continue

                count_new_file += 1
                await self.try_to_save_to_chat(msg)
                await self.try_to_save_to_db()
            if has_update:
                # 一次性跑完剩余任务并重试失败任务
                if self.need_save_to_chat:
                    await self.run_save_file_to_chat_tasks()
                    await self.retry_save_file_to_chat_tasks()
                if self.need_save_to_db:
                    await self.save_file_to_db()
        self.log_end(count_new_file)
        if self.need_test:
            self.test()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-fc", "--from_chat", type=str, required=True, help="from_chat")
    parser.add_argument("-tc", "--to_chat", type=str, required=True, help="to_chat")
    parser.add_argument("-ft", "--file_type", type=int, required=True, help="file_type")
    parser.add_argument("-ct", "--c_type", type=int, default=0, help="c_type # default 0")
    parser.add_argument("--limit", type=int, default=100, help="limit # default 100")
    parser.add_argument("--max_test_count", type=int, default=10, help="max_test_count # default 10")
    parser.add_argument("--task_count_per_time", type=int, default=100, help="task_count_per_time # default 100")
    parser.add_argument("--need_save_to_chat", action="store_false", help="need_save_to_chat # default true")
    parser.add_argument("--need_save_to_db", action="store_false", help="need_save_to_db # default true")
    parser.add_argument("--renew", action="store_true", help="renew # default false")
    parser.add_argument("--need_test", action="store_true", help="need_test # default false")
    parser.add_argument("--test_only", action="store_true", help="test_only # default false")
    args = parser.parse_args()
    saver = Saver(
        from_chat=args.from_chat,
        to_chat=args.to_chat,
        need_save_to_chat=args.need_save_to_chat,
        need_save_to_db=args.need_save_to_db,
        file_type=args.file_type,
        session_file=common.SESSION_FILE,
        api_id=common.CFG.api_id,
        api_hash=common.CFG.api_hash,
        db_file=common.CFG.db_file,
        need_test=args.need_test,
        test_only=args.test_only,
        max_test_count=args.max_test_count,
        renew=args.renew,
        proxies=common.CFG.proxy_pyrogram_json,
        limit=args.limit,
        retry_times=10,
        c_type=args.c_type,
        task_count_per_time=args.task_count_per_time
    )
    asyncio.run(saver.save())


if __name__ == '__main__':
    main()
