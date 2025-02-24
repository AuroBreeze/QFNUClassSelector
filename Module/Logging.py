import colorlog

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