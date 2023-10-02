import sys

import asyncio
import argparse
from pyrogram import Client, enums
import common
import handlers


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


LOG = common.Logger(path_log_file=f"{common.PATH_ROOT}/log.txt").logger

HANDLERS_MAP = {
    common.FileTypes.VIDEO: handlers.VideoHandler,
    common.FileTypes.PHOTO: handlers.PhotoHandler,
    common.FileTypes.DOCUMENT: handlers.DocumentHandler,
}
try:
    import handlers_c

    for handler in all_subclasses(handlers.FileHandler):
        if handler.C_TYPE != 0:
            HANDLERS_MAP[handler.C_TYPE] = handler
except ImportError:
    pass


class Saver:
    UGLY_WORDS = ["@", "http", "https", "群", "赌", "搜", "网址"]

    def __init__(self,
                 from_chat: str,
                 to_chat: str,
                 file_type: int,
                 limit=0,
                 c_type=0,
                 renew=False,
                 enable_ms=False):
        """TgChat 文件保存器

        :param from_chat: 抓取文件的目标 chat 的带 @ 名称
        :param to_chat: 文件保存的目标 chat 的带 @ 名称
        :param file_type: 文件类型 [FileTypes]
        :param limit: 消息限制数, 默认 0 即不限制
        :param c_type: 自定义 handler 的类型, 默认为 0, 不进行自定义
        :param renew: 尝试获取最新消息, 默认为 False
        :param enable_ms: 是否同步到 meilisearch, 默认为 False
        """
        self.from_chat = from_chat
        self.to_chat = to_chat
        self.file_type = file_type
        self.limit = limit
        self.c_type = c_type
        self.renew = renew
        self.enable_ms = enable_ms

        self.success_count = 0
        self.fail_count = 0
        self.max_fail_count = int(self.limit / 5)
        self.file_type_tag = common.FileTypes.TAG_MAP[file_type]
        handler_args = [file_type, from_chat, to_chat, enable_ms]
        self.handler = HANDLERS_MAP[file_type](*handler_args) if c_type == 0 \
            else HANDLERS_MAP[c_type](*handler_args)

    def check_if_file_is_ok(self, msg) -> bool:
        return self.check_if_has_no_markup(msg) \
            and self.check_if_content_is_ok(msg) \
            and self.check_if_is_target_file_type(msg)

    def check_if_content_is_ok(self, msg) -> bool:
        l_content = self.handler.get_file_content_from_msg(msg).lower()
        return True if not any(word in l_content for word in self.UGLY_WORDS) else False

    def check_if_is_target_file_type(self, msg) -> bool:
        return True if msg.media and str(msg.media) == self.file_type_tag else False

    def check_if_has_no_markup(self, msg):
        return True if not msg.reply_markup else False

    async def save(self):
        async with Client(common.SESSION_FILE, common.CFG.api_id, common.CFG.api_hash,
                          proxy=common.CFG.proxy_pyrogram_json,
                          parse_mode=enums.ParseMode.DISABLED) as app:
            self.handler.APP = app
            lock = asyncio.Lock()
            last_min_msg_id = self.handler.get_last_msg_id()
            last_max_msg_id = self.handler.get_last_msg_id(get_max=True)
            offset_id = 0 if self.renew else last_min_msg_id
            cur_min_msg_id = last_min_msg_id if last_min_msg_id != 0 else sys.maxsize
            cur_max_msg_id = last_max_msg_id
            async for msg in app.get_chat_history(self.from_chat, limit=self.limit, offset_id=offset_id):
                async with lock:
                    cur_min_msg_id = min(cur_min_msg_id, msg.id)
                    cur_max_msg_id = max(cur_max_msg_id, msg.id)
                if self.renew and last_max_msg_id >= msg.id:
                    break
                if self.check_if_file_is_ok(msg):
                    try:
                        await self.handler.save_file(msg)
                        LOG.info(f"保存成功: {msg.id}")
                        self.success_count += 1
                    except Exception as e:
                        LOG.error(f"保存失败: {msg.id}, {e}")
                        self.fail_count += 1
                        if self.fail_count >= self.max_fail_count:
                            LOG.error(f"任务失败: 保存失败数超过 {self.max_fail_count}, 直接退出")
                            return
            self.handler.update_last_msg_id(cur_min_msg_id)
            self.handler.update_last_msg_id(cur_max_msg_id, update_max=True)
            LOG.info(f"任务完成: 成功数: {self.success_count}, 失败数: {self.fail_count}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-fc", "--from_chat", type=str, required=True, help="from_chat")
    parser.add_argument("-tc", "--to_chat", type=str, required=True, help="to_chat")
    parser.add_argument("-ft", "--file_type", type=int, required=True, help="file_type")
    parser.add_argument("-ct", "--c_type", type=int, default=0, help="c_type # default 0")
    parser.add_argument("-lm", "--limit", type=int, default=100, help="limit # default 0, no limit")
    parser.add_argument("-rn", "--renew", action="store_true", help="renew # default False")
    parser.add_argument("-ms", "--enable_ms", action="store_true", help="enable_ms # default False")

    args = parser.parse_args()
    saver = Saver(
        from_chat=args.from_chat,
        to_chat=args.to_chat,
        file_type=args.file_type,
        limit=args.limit,
        c_type=args.c_type,
        renew=args.renew,
        enable_ms=args.enable_ms
    )
    asyncio.run(saver.save())


if __name__ == '__main__':
    main()
