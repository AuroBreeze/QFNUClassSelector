import datetime
import time
from Module import Logging
from Module.ConfigService import ConfigService
class Timer: # 定时任务类，执行定时任务的时间计时逻辑
    def __init__(self):
        self.log = Logging.Log("Timer")
        # 统一由 ConfigService 提供配置
        self.config = ConfigService().get_time()
        # 原始字符串（用于展示/返回）
        self.start_time_str = self.config["Start_time"]
        self.end_time_str = self.config["End_time"]
        # 解析为 time 对象（用于比较）
        self.start_time = self._parse_time(self.start_time_str)
        self.end_time = self._parse_time(self.end_time_str)
        self.retry_time = self.config["retry_time"]
        self.interval = self.config["Interval"]
    def run(self):
        while True:
            now_dt = datetime.datetime.now()
            now_time = now_dt.time()
            now_str = now_dt.strftime("%H:%M:%S")

            if now_time < self.start_time:
                self.log.main("INFO", f"选课未执行：当前时间：{now_str}, 等待时间：{self.start_time_str} 开始, 间隔时间：{self.retry_time/1000}秒")
                time.sleep(self.retry_time/1000)
                continue
            if now_time >= self.start_time and now_time < self.end_time:
                self.log.main("INFO", f"选课执行：当前时间：{now_str}")
                self.log.main("INFO", "选课开始")
                return True
            if now_time >= self.end_time:
                self.log.main("INFO", f"选课结束: 当前时间：{now_str}")
                return False

    def Return_config(self):
        config = {
            "start_time": self.start_time_str,
            "end_time": self.end_time_str,
            "retry_time": self.retry_time,
            "interval": self.interval,
        }
        return config
    def _parse_time(self, s: str) -> datetime.time:
        """将 'HH:MM' 或 'HH:MM:SS' 解析为 datetime.time 对象"""
        s = s.strip()
        for fmt in ("%H:%M:%S", "%H:%M"):
            try:
                dt = datetime.datetime.strptime(s, fmt)
                return dt.time()
            except ValueError:
                continue
        # 解析失败时给出清晰日志并回退到整点 00 秒
        self.log.main("ERROR", f"时间格式错误：'{s}'，请使用 'HH:MM' 或 'HH:MM:SS'")
        # 为避免崩溃，回退到 00:00:00
        return datetime.time(0, 0, 0)
if __name__ == '__main__':
    timer = Timer()
    timer.run()