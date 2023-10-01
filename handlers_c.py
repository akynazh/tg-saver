import re
from handlers import VideoHandler


class SgpVideoHandler(VideoHandler):
    C_TYPE = 101
    AV_PAT = re.compile(r"[a-z0-9]+[-_](?:ppv-)?[a-z0-9]+")

    def save_file_to_db(self, msg, ori_msg_id):
        file_id = self.get_file_id_from_msg(msg)
        content = self.get_file_content_from_msg(msg)
        ids = self.AV_PAT.findall(content.lower())
        if ids:
            self.conn.cursor().execute(f"""INSERT INTO {self.tb_name}(
            av_id, msg_id, file_id, file_type, content, ori_chat_name, ori_msg_id)
                            VALUES(?, ?, ?, ?, ?, ?, ?)""",
                                       (ids[0], msg.id, file_id, self.file_type, content, self.from_chat, ori_msg_id))
            self.conn.commit()
