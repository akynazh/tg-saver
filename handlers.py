from database import BotDb
import re


class VideoHandler:
    AV_PAT = re.compile(r"[a-z0-9]+[-_](?:ppv-)?[a-z0-9]+")

    def __init__(self, title: str, file_id: str, msg_id: int, video_type: int):
        self.title = title
        self.file_id = file_id
        self.msg_id = msg_id
        self.video_type = video_type

    def get_cav_video(self):
        return {
            "title": self.title,
            "file_id": self.file_id,
            "msg_id": self.msg_id
        }

    def get_sgp_video(self):
        ids = VideoHandler.AV_PAT.findall(self.title.lower())
        if not ids or len(ids) == 0:
            return None
        # 添加 av
        return {
            "av_id": ids[0],
            "title": self.title,
            "file_id": self.file_id,
            "msg_id": self.msg_id
        }

    def get_video_by_type(self):
        try:
            if self.video_type == BotDb.TYPE_SGP:
                return self.get_sgp_video()
            elif self.video_type == BotDb.TYPE_CAV:
                return self.get_cav_video()
        except Exception:
            return None


class PhotoHandler:
    pass
