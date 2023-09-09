from database import BotDb


class VideoHandler:

    def __init__(self, title: str, file_id: str, msg_id: int, video_type: int):
        self.title = title
        self.file_id = file_id
        self.msg_id = msg_id
        self.video_type = video_type

    def get_cav_video(self) -> dict:
        return {
            "title": self.title,
            "file_id": self.file_id,
            "msg_id": self.msg_id
        }

    def get_sgp_video(self):
        # 取得番号
        t1 = self.title.find("<")
        t2 = self.title.find(">")
        if t1 != -1 and t2 != -1:
            av_id = self.title[t1 + 1:t2]
        else:
            av_id = "-"
        # 添加 av
        return {
            "av_id": av_id,
            "title": self.title,
            "file_id": self.file_id,
            "msg_id": self.msg_id
        }

    def get_video_by_type(self) -> dict:
        try:
            if self.video_type == BotDb.TYPE_SGP:
                return self.get_sgp_video()
            elif self.video_type == BotDb.TYPE_CAV:
                return self.get_cav_video()
        except Exception:
            return {}


class PhotoHandler:
    pass
