import toml
from Module import Logging
from threading import Lock

class ConfigService:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self.log = Logging.Log("ConfigService")
        self._config = None
        self._path = "./config.toml"
        self.reload()

    def reload(self):
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                self._config = toml.load(f)
            self.log.main("DEBUG", "配置加载完成")
        except Exception as e:
            self.log.main("ERROR", f"读取配置文件失败: {e}")
            raise

    def get_raw(self):
        return self._config

    # Login
    def get_login(self):
        return self._config.get("Login", {})

    # Mode
    def get_mode(self):
        return self._config.get("Mode", {})

    # Plan
    def get_plan(self):
        return self._config.get("Plan", {})

    # Time
    def get_time(self):
        return self._config.get("Time", {})

    # Generic accessor
    def get_value(self, section: str, key: str, default=None):
        try:
            return self._config.get(section, {}).get(key, default)
        except Exception:
            return default
