from Module import Logging,URL_encode
import time

class Select_Class:
    def __init__(self,session):
        self.log = Logging.Log("Select_Class")
        self.session = session
        self.url = "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk"

        # 选课学分情况 http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xsxk_tzsm
        # 必修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInBxxk
        # 选修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInXxxk 查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkXxxk?
        # 本学期计划选课.json http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInBxqjhxk 查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkBxqjhxk?
        # 专业内跨年级选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInKnjxk  查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkKnjxk?
        # 计划外选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInFawxk 查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkFawxk?
        # 公选课选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk 查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?
        # 辅修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInFxzyxk 查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkFxxk?

    def Return_Data(self,Fixed_Data,kcxx="",skls="",skxq="",skjc="",sfym="false",sfct="false",sfxx="true",skxq_xx0103=""):
        self.params = Fixed_Data(output="Params",kcxx=kcxx, skls=skls, skxq=skxq, skjc=skjc, sfym=sfym, sfct=sfct, sfxx=sfxx, skxq_xx0103=skxq_xx0103).Return_Data()
        self.data = Fixed_Data(output="Data").Return_Data()
    def main(self):
        res = self.session.get(url=self.url,params=self.params).text
        res = self.session.post(url=self.url,params=self.params,data=self.data).json()
        print(res)


class Submit_ClassSelection:
    def __init__(self,session,jx0404id="202420252011613",kcid="530128"):
        self.session = session
        self.log = Logging.Log("Submit_ClassSelection")
        # 获取时间戳
        self.timestamp = int(round(time.time() * 1000))
        #print(timestamp)
        res = session.get(url=f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/iscx?jx0404id={str(jx0404id)}&kcid={str(kcid)}").text
        #print(res)
        res = session.get(
            url=f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/knjxkOper?kcid={str(kcid)}&cfbs=null&jx0404id={str(jx0404id)}&xkzy=&trjf=&_=" + str(
                self.timestamp)).text
        #print(res)
        self.log.main("INFO",res)


