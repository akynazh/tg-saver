import asyncio
import random
import time

from database import BotDb
from pyrogram import Client, enums
from handlers import VideoHandler
import logging

LOG = logging.getLogger(__name__)


class Saver:
    MSG_MEDIA_TYPE_VIDEO = "MessageMediaType.VIDEO"
    MSG_MEDIA_TYPE_PHOTO = "MessageMediaType.PHOTO"

    def __init__(self, from_chat: str, to_chat: str, need_send: bool, media_type: int, session_file: str, api_id: int,
                 api_hash: str, db_file: str, proxies=None, limit=0):
        self.from_chat = from_chat
        self.to_chat = to_chat
        self.need_send = need_send
        self.media_type = media_type
        self.session_file = session_file
        self.api_id = api_id
        self.api_hash = api_hash
        self.db_file = db_file
        self.proxies = proxies
        self.limit = limit

        self.db = BotDb(self.db_file)

    async def run_tasks(self, tasks):
        fail = 0
        LOG.info(f"任务数: {len(tasks)}, 发送中......")
        start = time.time()
        res_list = await asyncio.gather(*tasks)
        end = time.time()
        for res in res_list:
            fail = fail if res else fail + 1
        LOG.info(f"完成任务, 失败数: {fail}, 耗时: {end - start}s")
        return []

    async def save_to_bot(self, app, file_id, title):
        try:
            # 链接文件到某个 chat
            await asyncio.sleep(random.randint(3, 8))
            await app.send_video(chat_id=self.to_chat, video=file_id, caption=title)
            return True
        except Exception as e:
            LOG.error(f"发送 {file_id} 失败: {e}")
            return False

    async def save_video(self):
        # 加载上次记录
        old_cur_id = self.db.select_cur_msg_id(self.media_type)
        new_cur_id = 0
        count_new_video = 0
        new_videos = []
        async with Client(self.session_file, self.api_id, self.api_hash, proxy=self.proxies,
                          parse_mode=enums.ParseMode.DISABLED) as app:
            tasks = []
            async for message in app.get_chat_history(self.from_chat, limit=self.limit):
                msg_id = message.id
                # 没有更新的消息
                if old_cur_id > msg_id:
                    LOG.warning(f"没有更新的消息: {old_cur_id} > {msg_id}")
                    return
                # 更新最新消息 id
                new_cur_id = max(new_cur_id, msg_id)
                # 如果不是视频则跳过
                if not message.media or str(message.media) != Saver.MSG_MEDIA_TYPE_VIDEO:
                    continue
                title = message.caption
                file_id = message.video.file_id
                handler = VideoHandler(title, file_id, msg_id, self.media_type)
                v = handler.get_video_by_type()
                if v and v != {}:
                    count_new_video += 1
                    new_videos.append(v)
                if self.need_send:
                    tasks.append(asyncio.create_task(self.save_to_bot(app, file_id, title)))
                if len(tasks) == 50:
                    tasks = await self.run_tasks(tasks)
            await self.run_tasks(tasks)
        LOG.info(f"得到最新视频数量: {count_new_video}")
        self.db.batch_insert_medias(new_videos, self.media_type)
