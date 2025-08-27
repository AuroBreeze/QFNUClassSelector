import colorlog
import os
import sys
import logging  # 新增导入logging模块
import datetime
import threading

class Log:
    _instance = None
    _initialized = False
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name="main", level="DEBUG"):
        if self._initialized:
            # 确保名称不会被后续调用修改
            return
        self._initialized = True
        self.name = name
        # 使用专用命名日志器
        self.logger = colorlog.getLogger("QFNUClassSelector")
        self.logger.propagate = False
        # 计算日志级别：优先环境变量 LOG_LEVEL，其次参数，默认 DEBUG
        env_level = os.getenv("LOG_LEVEL", "").upper()
        level_map = {
            "DEBUG": colorlog.DEBUG,
            "INFO": colorlog.INFO,
            "WARNING": colorlog.WARNING,
            "WARN": colorlog.WARNING,
            "ERROR": colorlog.ERROR,
            "CRITICAL": colorlog.CRITICAL,
        }
        chosen_level = level_map.get(env_level, level_map.get(level, colorlog.DEBUG))
        self.logger.setLevel(chosen_level)

        # 控制台格式器（彩色）
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s][%(name)s][%(levelname)s] [%(message)s]',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            })
        # 控制台处理器
        self.handler = colorlog.StreamHandler()
        self.handler.name = 'custom_stream_handler'
        self.handler.setLevel(chosen_level)
        self.handler.setFormatter(console_formatter)

        # 添加文件处理器
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.file_handler = logging.FileHandler(os.path.join(log_dir, f'{datetime.datetime.now().strftime("%Y-%m-%d")}_app.log'), encoding='utf-8')
        self.file_handler.name = 'custom_file_handler'
        # 使用非彩色格式器，避免颜色控制字符写入日志文件
        self.file_formatter = logging.Formatter(
            '[%(asctime)s][%(name)s][%(levelname)s] [%(message)s]',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.file_handler.setFormatter(self.file_formatter)
        # 确保只保留一个同名文件处理器
        for handler in self.logger.handlers[:]:
            if handler.name == 'custom_file_handler':
                self.logger.removeHandler(handler)
        self.logger.addHandler(self.file_handler)

        # 确保控制台处理器也被添加
        # 确保只保留一个同名控制台处理器
        for handler in self.logger.handlers[:]:
            if handler.name == 'custom_stream_handler':
                self.logger.removeHandler(handler)
        self.logger.addHandler(self.handler)

    def main(self, level, message):
        message = str(message)
        # 移除重复添加处理器的逻辑
        if level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARN":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        elif level == "CRITICAL":
            self.logger.critical(message)
        else:
            self.logger.error("日志输出等级设置错误")
if __name__ == '__main__':
    Log("root").main("DEBUG","Debug")