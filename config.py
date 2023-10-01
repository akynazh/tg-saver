import yaml
import logging

LOG = logging.getLogger(__name__)


class Config:
    def __init__(self, path_config_file: str):
        with open(path_config_file, "r", encoding="utf8") as f:
            config = yaml.safe_load(f)
        self.api_id = int(config["api_id"])
        self.api_hash = config["api_hash"]
        self.db_file = config["db_file"]
        self.use_proxy = config["use_proxy"] if config["use_proxy"] else "0"
        self.scheme = config["scheme"]
        self.hostname = config["hostname"]
        self.port = int(config["port"])
        if not self.api_id or not self.api_hash or not self.db_file:
            LOG.error(f"读取配置文件出错: 缺失参数")
            raise AttributeError

        self.proxy_addr = ""
        self.proxy_json = {}
        self.proxy_pyrogram_json = {}
        if self.use_proxy == "1":
            if not self.scheme or not self.hostname or not self.port:
                LOG.error(f"读取配置文件出错: 开启了代理但是缺失相关参数")
                raise AttributeError
            self.proxy_addr = f"{self.scheme}://{self.hostname}:{self.port}"
            self.proxy_json = {"http": self.proxy_addr, "https": self.proxy_addr}
            self.proxy_pyrogram_json = {"scheme": self.scheme, "hostname": self.hostname, "port": self.port}
            LOG.info(f'设置代理: "{self.proxy_addr}"')
