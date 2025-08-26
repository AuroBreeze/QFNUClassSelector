import re
from bs4 import BeautifulSoup
from Module import Logging
from Module import Timer
from Module import login
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class Session_Inherit:
    def __init__(self,index):
        self.session = login.Login().Main()  # 继承session
        self.log= Logging.Log("Inherit_Session")
        self.index = index  # 保存当前登录的序号
        self.config = Timer.Timer().Return_config()
        # 为会话增加重试策略（网络抖动/5xx时自动重试）
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.url_list = []

        self.Progressively_Inherit()
    def Progressively_Inherit(self):  # 继承session，session按序访问保持会话JSESSIONID
        count = 0
        timeout = self.config.get('request_timeout', 5)  # 单次请求超时时间（秒）
        """
        以下都是需要逐步遍历的网页。
        :return:
        """
        while True:
            try:
                self.log.main("INFO", "正在尝试继承session......")

                url_1 = "http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xklc_list"
                response = self.session.get(url=url_1, timeout=timeout)
                response.raise_for_status()
                response = response.text
                soup = BeautifulSoup(response, "lxml")

                #若没有选课，则从这里开始，下面的代码都会报错。
                #若有选课，则从这里开始，下面的代码都可以正常运行。
                self.log.main("DEBUG", "选课学分情况页面分界线，若在此处及以下出现DEBUG报错，则说明没有到选课时间")

                fragment = soup.select("#jrxk")[0]["href"]
                url_2 = "http://zhjw.qfnu.edu.cn" + fragment
                res = self.session.get(url=url_2, timeout=timeout)
                res.raise_for_status()
                res = res.text
                #print(url_2)


                num = re.findall("/jsxsd/xsxk/xklc_view(.*?)=(.*)", fragment)
                url_3 = f"http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid={num[0][1]}"
                res = self.session.get(url=url_3, timeout=timeout)
                res.raise_for_status()
                res = res.text
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
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                self.log.main("DEBUG", f"网络请求失败（超时/连接错误）：{e}，timeout={timeout}s")
                self.log.main("DEBUG", f"第{count + 1}次,间隔：{self.config['retry_time']/1000}秒,正在尝试重新继承session......")
                count += 1
                if count >= 20:  # 尝试20次，若失败则退出
                    self.log.main("INFO", f"Session重新获取......")
                    count = 0
                    Session_judge = self.Get_Session_New()
                    if Session_judge == False:
                        self.log.main("ERROR", "Session获取失败，请联系开发者")
            except Exception as e:
                self.log.main("DEBUG", f"session继承失败，原因：{e}")
                self.log.main("DEBUG", f"第{count + 1}次,间隔：{self.config['retry_time']/1000}秒,正在尝试重新继承session......")
                count += 1
                if count >= 20:  # 尝试20次，若失败则退出
                    self.log.main("INFO", f"Session重新获取......")
                    count = 0
                    Session_judge = self.Get_Session_New()
                    if Session_judge == False:
                        self.log.main("ERROR", "Session获取失败，请联系开发者")

                time.sleep(self.config['retry_time']/1000)

    def Get_Session_New(self): # 重新获取session
        session_old = self.session
        self.session = login.Login().Main()
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