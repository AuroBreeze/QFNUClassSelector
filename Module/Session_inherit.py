import re
from bs4 import BeautifulSoup
from Module import Logging
from Module import Timer
from Module import login
import time

class Session_Inherit:
    def __init__(self,index):
        self.session = login.mainss(index)  # 继承session
        self.index = index  # 保存当前登录的序号
        self.config = Timer.Timer().Return_config()
        self.url_list = []  # 保存所有选课的url
        """
        0:# 选课学分情况 http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xsxk_tzsm
        1:# 必修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInBxxk
        2:# 选修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInXxxk
        3:# 本学期计划选课.json http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInBxqjhxk
        4:# 专业内跨年级选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInKnjxk
        5:# 计划外选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInFawxk
        6:# 公选课选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk
        7:# 辅修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInFxzyxk
        """
        self.Progressively_Inherit()
    def Progressively_Inherit(self):  # 继承session，session按序访问保持会话JSESSIONID
        count = 0
        """
        以下都是需要逐步遍历的网页。
        :return:
        """
        while True:
            try:
                url_1 = "http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xklc_list"
                response = self.session.get(url=url_1).text
                soup = BeautifulSoup(response, "lxml")

                #若没有选课，则从这里开始，下面的代码都会报错。
                #若有选课，则从这里开始，下面的代码都可以正常运行。
                Logging.Log("Inherit_Session").main("DEBUG", "选课学分情况页面分界线，若在此处及以下出现DEBUG报错，则说明没有到选课时间")

                fragment = soup.select("#jrxk")[0]["href"]
                url_2 = "http://zhjw.qfnu.edu.cn" + fragment
                res = self.session.get(url=url_2).text

                num = re.findall("/jsxsd/xsxk/xklc_view(.*?)=(.*)", fragment)
                url_3 = f"http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid={num[0][1]}"
                res = self.session.get(url=url_3).text

                soup = BeautifulSoup(res, "lxml")
                list = soup.select("#topmenu  li")
                for i in list:
                    url = "http://zhjw.qfnu.edu.cn" + i.a["href"]
                    self.url_list.append(url)
                    # print(i.a.string + " " + url)
                # print("session继承成功")
                Logging.Log("Inherit_Session").main("INFO", "session继承成功")
            except Exception as e:
                Logging.Log("Inherit_Session").main("DEBUG", f"session继承失败，原因：{e}")
                Logging.Log("Inherit_Session").main("DEBUG", f"第{count + 1}次,间隔：{self.config['retry_time']/1000}秒,正在尝试重新继承session......")
                count += 1
                if count >= 100:
                    Logging.Log("Inherit_Session").main("INFO", f"Session重新获取......")
                    count = 0
                    Session_judge = self.Get_Session_New()
                    if Session_judge == False:
                        Logging.Log("Inherit_Session").main("ERROR", "Session获取失败，请联系开发者")

                time.sleep(self.config['retry_time']/1000)
    def Get_Session_New(self):
        session_old = self.session
        self.session = login.mainss(self.index)
        if session_old.cookies.get_dict() !=self.session.cookies.get_dict():
            Logging.Log("Inherit_Session").main("INFO", "Session重新获取成功")
            return True
        else:
            Logging.Log("Inherit_Session").main("ERROR", "Session重新获取失败")
            return False

    def Return_Session(self):
        return self.session
if __name__ == '__main__':
    session = Session_Inherit(0).Return_Session()