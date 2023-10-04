import re
from handler.base import VideoHandler, MediaGroupHandler


class JavHandler(VideoHandler):
    C_TYPE = 101
    AV_PAT = re.compile(r"[a-z0-9]+[-_](?:ppv-)?[a-z0-9]+")

    def save_file_to_db(self, new_msg, old_msg):
        file_id = self.get_file_id_from_msg(new_msg)
        ids = self.AV_PAT.findall(self.get_file_content_from_msg(new_msg).lower())
        self.conn.cursor().execute(f"""INSERT INTO {self.tb_name}(
        av_id, msg_id, file_id, file_type, content, ori_chat_name, ori_msg_id)
                        VALUES(?, ?, ?, ?, ?, ?, ?)""",
                                   (ids[0], new_msg.id, file_id, self.file_type, ids[0], self.from_chat, old_msg.id))
        self.conn.commit()

    def check_if_content_is_ok(self, msg) -> bool:
        return super().check_if_content_is_ok(msg) and self.AV_PAT.findall(
            self.get_file_content_from_msg(msg).lower()) != []


class JavMediaGroupHandler(MediaGroupHandler):
    C_TYPE = 102
    AV_PAT = re.compile(r"[a-z0-9]+[-_](?:ppv-)?[a-z0-9]+")

    def gen_id_from_content(self, content) -> str:
        ids = self.AV_PAT.findall(content.lower())
        return ids[0] if ids else super().gen_id_from_content(content)
