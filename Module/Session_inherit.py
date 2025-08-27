import re
import random
from bs4 import BeautifulSoup
from Module import Logging
from Module import login
from Module.ConfigService import ConfigService
import time
from Module.NetUtils import NetUtils

class Session_Inherit:
    def __init__(self,index, session=None):
        # 可注入已有 session，未提供则内部登录
        self.session = session or login.Login(index).Main()
        self.log= Logging.Log("Inherit_Session")
        self.index = index  # 保存当前登录的序号
        # 统一配置来源
        time_cfg = ConfigService().get_time()
        self.retry_time = time_cfg.get("retry_time", 3000)  # 毫秒
        self.max_attempts = time_cfg.get("inherit_max_attempts", 20)
        self.request_timeout = time_cfg.get("request_timeout_sec", 10)
        self.net = NetUtils()

        self.url_list = []

        self.Progressively_Inherit()
    def Progressively_Inherit(self):  # 继承session，session按序访问保持会话JSESSIONID
        count = 0
        """
        以下都是需要逐步遍历的网页。
        :return:
        """
        while True:
            try:
                self.log.main("INFO", "正在尝试继承session......")

                url_1 = "http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xklc_list"
                resp1, err1 = self.net.request_with_retry(self.session, "GET", url_1, timeout=self.request_timeout)
                if err1 is not None and err1 not in ("ok",):
                    raise RuntimeError(f"step1 failed: {err1}")
                response = resp1.text if resp1 is not None else ""
                soup = BeautifulSoup(response, "lxml")

                #若没有选课，则从这里开始，下面的代码都会报错。
                #若有选课，则从这里开始，下面的代码都可以正常运行。
                self.log.main("DEBUG", "选课学分情况页面分界线，若在此处及以下出现DEBUG报错，则说明没有到选课时间")

                fragment = soup.select("#jrxk")[0]["href"]
                url_2 = "http://zhjw.qfnu.edu.cn" + fragment
                resp2, err2 = self.net.request_with_retry(self.session, "GET", url_2, timeout=self.request_timeout)
                if err2 is not None and err2 not in ("ok",):
                    raise RuntimeError(f"step2 failed: {err2}")
                res = resp2.text if resp2 is not None else ""
                #print(url_2)


                num = re.findall("/jsxsd/xsxk/xklc_view(.*?)=(.*)", fragment)
                url_3 = f"http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid={num[0][1]}"
                resp3, err3 = self.net.request_with_retry(self.session, "GET", url_3, timeout=self.request_timeout)
                if err3 is not None and err3 not in ("ok",):
                    raise RuntimeError(f"step3 failed: {err3}")
                res = resp3.text if resp3 is not None else ""
                #print(url_3)

                soup = BeautifulSoup(res, "lxml")
                list = soup.select("#topmenu  li")
                for i in list:
                    url = "http://zhjw.qfnu.edu.cn" + i.a["href"]
                    self.url_list.append(url)
                    # print(i.a.string + " " + url)
                # print("session继承成功")
                #print(self.url_list)
                self.log.main("INFO", "session继承成功")
                return True
            except Exception as e:
                self.log.main("DEBUG", f"session继承失败，原因：{e}")
                self.log.main("DEBUG", f"第{count + 1}次,间隔：{self.retry_time/1000}秒,正在尝试重新继承session......")
                count += 1
                if count >= self.max_attempts:  # 达到最大尝试次数后刷新登录
                    self.log.main("INFO", f"Session重新获取......")
                    count = 0
                    Session_judge = self.Get_Session_New()
                    if Session_judge == False:
                        self.log.main("ERROR", "Session获取失败，请联系开发者")

                # 指数退避 + 抖动
                backoff_ms = min(self.retry_time * (2 ** max(count-1, 0)), 30000)
                jitter = random.uniform(0.9, 1.1)
                sleep_s = (backoff_ms * jitter) / 1000.0
                time.sleep(sleep_s)
    def Get_Session_New(self): # 重新获取session
        session_old = self.session
        self.session = login.Login(self.index).Main()
        if session_old.cookies.get_dict() !=self.session.cookies.get_dict():
            self.log.main("INFO", "Session重新获取成功")
            return True
        else:
            self.log.main("ERROR", "Session重新获取失败")
            return False

    def Return_Session(self):
        return self.session
if __name__ == '__main__':
    session = Session_Inherit(0).Return_Session()