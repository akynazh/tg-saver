import os
from config import Config

PATH_ROOT = f'{os.path.expanduser("~")}/.tg_saver'
if not os.path.exists(PATH_ROOT):
    os.mkdir(PATH_ROOT)
CFG = Config(path_config_file=f"{PATH_ROOT}/config.yaml")
SESSION_FILE = f"{PATH_ROOT}/session"


class FileType:
    VIDEO = 1
    PHOTO = 2
    DOCUMENT = 3

    FILE_TAG_MAP = {
        VIDEO: "MessageMediaType.VIDEO",
        PHOTO: "MessageMediaType.PHOTO",
        DOCUMENT: "MessageMediaType.DOCUMENT",
    }

import logging


class Logger:
    """日志记录器"""

    def __init__(self, path_log_file: str, log_level=logging.INFO):
        """初始化日志记录器

        :param str path_log_file: 日志记录文件
        :param int log_level: 记录级别, 默认 INFO 级别
        """
        self.logger = logging.getLogger()
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(message)s")
        file_handler = logging.FileHandler(path_log_file)
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(log_level)