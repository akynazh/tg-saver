import re
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
    pat_flood_wait = re.compile(r"A wait of (\d+) seconds is required")
    lock = asyncio.Lock()
    total = 0

    def __init__(self, from_chat: str, to_chat: str, need_save_to_chat: bool, need_save_to_db: bool, file_type: int,
                 session_file: str, api_id: int, api_hash: str, db_file: str, need_test=False, test_only=False,
                 max_test_count=100, renew=False, proxies=None, limit=0, c_type=0, max_wait_time=30):
        """TgChat 文件保存器

        :param from_chat: 抓取文件的目标 chat
        :param to_chat: 文件保存的目标 chat
        :param need_save_to_chat: 是否需要保存文件到 chat
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
        :param c_type: 自定义 handler 的类型 [CustomHandlerType], 默认为 0, 不进行自定义
        :param max_wait_time: 最大等待时间, 默认 30s
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
        self.c_type = c_type
        self.max_wait_time = max_wait_time

        self.file_type_tag = common.FileType.FILE_TAG_MAP[self.file_type]
        self.handler = FileHandlerFactory(self.file_type, self.from_chat, self.to_chat, self.db_file,
                                          self.c_type).get_handler()

    async def run_save_file_to_chat_tasks(self):
        LOG.info(f"开始保存文件到 chat, 任务数: {len(self.tasks)}, 发送中......")
        res_list = await asyncio.gather(*self.tasks)
        count_fail = len(list(filter(lambda x: not x, res_list)))
        LOG.info(f"保存文件到 chat, 任务数: {len(self.tasks)}, 失败数: {count_fail}")
        self.tasks = []

    async def retry_save_file_to_chat_tasks(self):
        cur_retry_times = 0
        while len(self.fail_msg_list) > 0:
            if cur_retry_times > 3:
                LOG.error(f"重试次数已经达到限制, 停止重试, 剩余保存失败的文件数: {len(self.fail_msg_list)}")
                self.fail_msg_list = []
                break
            LOG.warning(
                f"重试保存文件到 chat, 剩余保存失败的文件数: {len(self.fail_msg_list)}, 已重试次数: {cur_retry_times}, 开始重试...")
            self.tasks = [asyncio.create_task(self.save_file_to_chat(msg)) for msg in self.fail_msg_list]
            self.fail_msg_list = []
            await self.run_save_file_to_chat_tasks()
            cur_retry_times += 1

    async def save_file_to_chat(self, msg):
        try:
            await self.handler.save_file_to_chat(self.app, msg)
            if self.need_save_to_db:
                self.success_msg_list.append(msg)
            LOG.info(f"成功保存文件:{self.handler.get_file_id_from_msg(msg)} 到 {self.to_chat}")
            await asyncio.sleep(random.randint(1, self.max_wait_time))
            return True
        except Exception as e:
            self.fail_msg_list.append(msg)
            LOG.error(f"保存文件到 {self.to_chat} 失败: {e}")
            wait_time = self.pat_flood_wait.findall(str(e))
            if wait_time:
                LOG.warning(f"根据限制信息提示开始休眠 {wait_time[0]}s ......")
                await asyncio.sleep(int(wait_time[0]))
            return False

    async def save_file_to_db(self):
        await self.handler.batch_save_file_to_db(self.success_msg_list)

    async def try_to_save_to_chat(self, msg=None, is_last=False):
        if self.need_save_to_chat:
            if msg:
                self.tasks.append(asyncio.create_task(self.save_file_to_chat(msg)))
            if len(self.tasks) >= 50 or is_last:
                await self.run_save_file_to_chat_tasks()
            if len(self.fail_msg_list) >= 50 or is_last:
                await self.retry_save_file_to_chat_tasks()
        elif self.need_save_to_db and msg:
            self.success_msg_list.append(msg)

    async def try_to_save_to_db(self, is_last=False):
        if self.need_save_to_db and (len(self.success_msg_list) >= 100 or is_last):
            await self.save_file_to_db()

    def filter_file_by_type(self, msg):
        # 如果不是目标文件类型则跳过
        if not msg.media or str(msg.media) != self.file_type_tag:
            return False
        return True

    def check_if_has_new_msg(self, msg, old_cur_id):
        # 没有更新的消息
        if old_cur_id > msg.id:
            LOG.info(f"没有更新的消息: {old_cur_id} >= {msg.id}")
            return False
        return True

    def test(self):
        self.handler.test_tb_files(self.max_test_count)

    async def save(self):
        if self.test_only:
            self.test()
            return
        old_cur_id = self.handler.get_last_msg_id_from_db()
        if self.renew:
            old_cur_id = -1
            self.handler.clear_tb_files()
        has_update = True
        async with Client(self.session_file, self.api_id, self.api_hash, proxy=self.proxies,
                          parse_mode=enums.ParseMode.DISABLED) as app:
            self.app = app
            async for msg in app.get_chat_history(self.from_chat, limit=self.limit):
                if not self.check_if_has_new_msg(msg, old_cur_id):
                    has_update = False
                    break
                if not self.filter_file_by_type(msg):
                    continue
                async with self.lock:
                    self.total += 1
                await self.try_to_save_to_chat(msg)
                await self.try_to_save_to_db()
            if has_update:
                await self.try_to_save_to_chat(is_last=True)
                await self.try_to_save_to_db(is_last=True)
        LOG.info(f"$ 目标文件总数: {self.total}, 成功保存总数: {self.handler.success_count}")
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
    parser.add_argument("--max_wait_time", type=int, default=30, help="max_test_count # default 30")
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
        c_type=args.c_type,
        max_wait_time=args.max_wait_time
    )
    asyncio.run(saver.save())


if __name__ == '__main__':
    main()
