import re
from bs4 import BeautifulSoup
from Module import Logging

class Session_Inherit:
    def __init__(self,session):
        self.session = session #Get_Session()  # 继承session
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
        """
        以下都是需要逐步遍历的网页。
        :return:
        """

        url_1 = "http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xklc_list"
        response = self.session.get(url=url_1).text
        soup = BeautifulSoup(response, "lxml")

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
            #print(i.a.string + " " + url)

        #print("session继承成功")
        Logging.Log("Inherit_Session").main("INFO", "session继承成功")


    def Return_Session(self):
        return self.session
if __name__ == '__main__':
    pass