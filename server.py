# pip install "fastapi[all]"
# uvicorn server:APP --reload --host 0.0.0.0 --port 8000

from pyrogram import Client
from fastapi.responses import UJSONResponse
from fastapi import FastAPI
from pydantic import BaseModel
from common import CFG
import logging

LOG = logging.getLogger(__name__)
APP = FastAPI()


class Item(BaseModel):
    chat_name: str
    media_type: int
    file_id_list: list


"""
curl "localhost:8000/send" \
  -X POST \
  -H 'content-type: application/json; charset=UTF-8' \
  -H 'origin: https://www.fxiaoke.com' \
  -H 'referer: https://www.fxiaoke.com/XV/UI/Home' \
  -d '{"chat_name": "@zh_testt_bot", "media_type": "1", "file_id_list": [
    "BAACAgUAAx0CTGyOMQACBNhk_KZMRJLXGhNrEdCo8-IqjAK89QACYAsAAiQcqVfoEawx7fFuOB4E",
    "BAACAgUAAx0CTGyOMQACBNZk_KZMUP7LekGyULk6esejlnG4NAACRwkAAk4liVdiWSogUbBthB4E",
    "BAACAgUAAx0CTGyOMQACBNpk_KZMcmZgtEtVBv-Xy7UTU-cjoQACLgoAAgqbsVeSi38I6Xx-th4E"]}'
"""


@APP.post("/send", response_class=UJSONResponse)
async def batch_send_files(item: Item):
    chat_name = item.chat_name
    file_id_list = item.file_id_list
    media_type = item.media_type
    count_fail = 0
    async with Client(common.SESSION_FILE, CFG.api_id, CFG.api_hash, proxy=CFG.proxy_pyrogram_json) as app:
        for file_id in file_id_list:
            LOG.info(f"发送文件 {file_id} 到 {chat_name}")
            try:
                if media_type == 1:
                    await app.send_video(chat_id=chat_name, video=file_id)
                elif media_type == 2:
                    await app.send_photo(chat_id=chat_name, photo=file_id)
            except Exception:
                count_fail += 1
        LOG.info(f"总共发送 {len(file_id_list)} 个文件, 其中 {count_fail} 个文件发送失败")
        return {"total": len(file_id_list), "fail": count_fail, "code": 200}
