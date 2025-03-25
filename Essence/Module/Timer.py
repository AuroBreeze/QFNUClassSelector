import datetime
import time
import toml
from Module import Logging
class Timer: # 定时任务类，执行定时任务的时间计时逻辑
    def __init__(self):
        self.log = Logging.Log("Timer")
        with open("./config.toml","r",encoding="utf-8") as f:
            self.config = toml.load(f)
        self.start_time = self.config["Time"]["Start_time"]
        self.end_time = self.config["Time"]["End_time"]
        self.retry_time = self.config["Time"]["retry_time"]
        self.interval = self.config["Time"]["Interval"]
    def run(self):
        while True:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            #print(f"当前时间：{now}")

            if now < self.start_time:
                self.log.main("INFO", f"选课未执行：当前时间：{now}, 等待时间：{self.start_time}开始, 间隔时间：{self.retry_time/1000}秒")
                time.sleep(self.retry_time/1000)
                continue
            if now >= self.start_time and now < self.end_time:
                self.log.main("INFO", f"选课执行：当前时间：{now}")
                self.log.main("INFO", "选课开始")
                return True
            if now >= self.end_time:
                self.log.main("INFO", f"选课结束:当前时间：{now}")
                return False

    def Return_config(self):
        config = {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "retry_time": self.retry_time,
            "interval": self.interval,
        }
        return config
if __name__ == '__main__':
    timer = Timer()
    timer.run()