from requests import session
from bs4 import BeautifulSoup
import login
import re
import time
import urllib.parse #实现URL编码


class URL_encode:
    def __init__(self, text="乒乓球"):
        "%E4%B9%92%E4%B9%93%E7%90%83"
        # 需要编码的字符串
        self.text = f"{text}"
        # URL 编码
        self.encoded_text = urllib.parse.quote(self.text)
        #print(self.encoded_text)
    def Get_encode(self):
        return self.encoded_text

class Get_Session: # 获取session
    def __init__(self):
        self.session = login.mainss()
    def Return_Session(self):
        return self.session

class Fixed_Data:

    # 固定提交的表单
    # sEcho=1&iColumns=12&sColumns=&iDisplayStart=0&iDisplayLength=15&mDataProp_0=kch&mDataProp_1=kcmc&mDataProp_2=fzmc&mDataProp_3=xf&mDataProp_4=skls&mDataProp_5=sksj&mDataProp_6=skdd&mDataProp_7=xqmc&mDataProp_8=xkrs&mDataProp_9=syrs&mDataProp_10=ctsm&mDataProp_11=czOper

    def __init__(self,output,kcxx="",skls="",skxq="",skjc="",sfym="false",sfct="false",sfxx="true",skxq_xx0103=""):
        self.kcxx = kcxx # kcxx ：课程(URL编码)
        self.skls = skls # skls 老师(URL编码)
        self.skxq = skxq # skxq 星期 1 2 3 4 5 6 7 可为空
        self.skjc = skjc # skjc 节次 1-2- 3-4- 5-6- 7-8- 9-10-11 12-13- 可为空
        self.sfym = sfym # sfym 是否过滤已满的课程 默认false
        self.sfct = sfct # sfct 是否过滤冲突的课程 默认false
        self.sfxx = sfxx # sfxx 是否过滤限选的课程 默认true
        self.skxq_xx0103 = skxq_xx0103 # skxq_xx0103 1:曲阜 2：日照 68FD936EFC564F6E88EC852F9E8019C2：曲阜西校区

        self.output = output # 返回固定参数

        self.frame = f"kcxx={self.kcxx}&skls={self.skls}&skxq={self.skxq}&skjc={self.skjc}&sfym={self.sfym}&sfct={self.sfct}&sfxx={self.sfxx}&skxq_xx0103={self.skxq_xx0103}"
        self.data_str = { #POST表单,查询课程表需要的参数
            "sEcho": "1",
            "iColumns": "12",
            "sColumns": "",
            "iDisplayStart": "0",
            "iDisplayLength": "15",
            "mDataProp_0": "kch",
            "mDataProp_1": "kcmc",
            "mDataProp_2": "fzmc",
            "mDataProp_3": "xf",
            "mDataProp_4": "skls",
            "mDataProp_5": "sksj",
            "mDataProp_6": "skdd",
            "mDataProp_7": "xqmc",
            "mDataProp_8": "xkrs",
            "mDataProp_9": "syrs",
            "mDataProp_10": "ctsm",
            "mDataProp_11": "czOper"}


    def Return_Data(self): #拼接查询需要的参数
        if self.output == None:
            return
        if self.output == "Data":
            return self.data_str
        if self.output == "Frame":
            #print(self.frame)
            return self.frame


class Session_Inherit:
    def __init__(self,session):
        self.session = session#Get_Session()  # 继承session
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
        response = session.get(url=url_1).text
        soup = BeautifulSoup(response, "lxml")

        fragment = soup.select("#jrxk")[0]["href"]
        url_2 = "http://zhjw.qfnu.edu.cn" + fragment
        res = session.get(url=url_2).text

        num = re.findall("/jsxsd/xsxk/xklc_view(.*?)=(.*)", fragment)
        url_3 = f"http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid={num[0][1]}"
        res = session.get(url=url_3).text

        soup = BeautifulSoup(res, "lxml")
        list = soup.select("#topmenu  li")
        for i in list:
            url = "http://zhjw.qfnu.edu.cn" + i.a["href"]
            self.url_list.append(url)
            print(i.a.string + " " + url)

        print("session继承成功")

# 选课学分情况 http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xsxk_tzsm
# 必修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInBxxk
# 选修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInXxxk
# 本学期计划选课.json http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInBxqjhxk
# 专业内跨年级选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInKnjxk
# 计划外选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInFawxk
# 公选课选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk
# 辅修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInFxzyxk

class Select_Class:
    def __init__(self,kcxx="",skls="",skxq="",skjc="",sfym="false",sfct="false",sfxx="true",skxq_xx0103=""):
        self.frame = Fixed_Data(output="Frame",kcxx=kcxx, skls=skls, skxq=skxq, skjc=skjc, sfym=sfym, sfct=sfct, sfxx=sfxx, skxq_xx0103=skxq_xx0103).Return_Data()
        self.data = Fixed_Data(output="Data").Return_Data()
        self.url = "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkKnjxk?" + self.frame
        print(self.url)

    def main(self):
        res = session.get(url=self.url).text
        res = session.post(url=self.url,data=self.data).json()
        #print(res)

class Submit_ClassSelection:
    def __init__(self,jx0404id="202420252011613",kcid="530128"):
        # 获取时间戳
        self.timestamp = int(round(time.time() * 1000))
        #print(timestamp)
        res = session.get(url=f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/iscx?jx0404id={str(jx0404id)}&kcid={str(kcid)}").text
        #print(res)
        res = session.get(
            url=f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/knjxkOper?kcid={str(kcid)}&cfbs=null&jx0404id={str(jx0404id)}&xkzy=&trjf=&_=" + str(
                self.timestamp)).text
        print(res)


if __name__ == '__main__':
    session = Get_Session().Return_Session()
    Session_Inherit(session)
    name=URL_encode("乒乓球").Get_encode()
    select = Select_Class(kcxx=name).main()
    Submit_ClassSelection()
