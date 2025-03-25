import colorlog
import os
import sys
import logging  # 新增导入logging模块
import datetime

class Log:
    def __init__(self, name="main", level="INFO"):
        self.name = name
        if level == "INFO":
            self.logger = colorlog.getLogger(self.name)
            self.logger.setLevel(colorlog.INFO)
            self.handler = colorlog.StreamHandler()
            self.handler.setLevel(colorlog.INFO)
        elif level == "DEBUG":
            self.logger = colorlog.getLogger(self.name)
            self.logger.setLevel(colorlog.DEBUG)
            self.handler = colorlog.StreamHandler()
            self.handler.setLevel(colorlog.DEBUG)
        # 修改日志格式，使其更美观
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s][%(name)s][%(levelname)s] [%(message)s]',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            })
        
        # 添加文件处理器
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.file_handler = logging.FileHandler(os.path.join(log_dir, f'{datetime.datetime.now().strftime("%Y-%m-%d")}_app.log'), encoding='utf-8')  # 修改日志文件编码为UTF-8
        # 使用非彩色格式器，避免颜色控制字符写入日志文件
        self.file_formatter = logging.Formatter(
            '[%(asctime)s][%(name)s][%(levelname)s] [%(message)s]',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(self.file_handler)

    def main(self, level, message):
        message = str(message)
        # 检查是否已经添加了 handler
        if not self.logger.handlers:
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)
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