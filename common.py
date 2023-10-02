import os
import logging
from logging.handlers import RotatingFileHandler
from config import Config

PATH_ROOT = f'{os.path.expanduser("~")}/.tg_saver'
SESSION_FILE = f"{PATH_ROOT}/session"
CFG = Config(path_config_file=f"{PATH_ROOT}/config.yaml")


class FileTypes:
    VIDEO = 1
    PHOTO = 2
    DOCUMENT = 3

    TAG_MAP = {
        VIDEO: "MessageMediaType.VIDEO",
        PHOTO: "MessageMediaType.PHOTO",
        DOCUMENT: "MessageMediaType.DOCUMENT",
    }


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
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        r_file_handler = RotatingFileHandler(path_log_file, maxBytes=1024 * 1024 * 16, backupCount=1)
        r_file_handler.setFormatter(formatter)
        self.logger.addHandler(r_file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(log_level)
