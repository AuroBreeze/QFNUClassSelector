from Module import Logging,Data
import time
import toml

class Select_Class:
    def __init__(self,session):
        self.log = Logging.Log("Select_Class")
        self.session = session
        #self.url = "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk"

        self.Get_Course_order()
        self.Get_Source()

    def Get_Course_order(self):
        with open("./config.toml","r",encoding="utf-8") as f:
            config = toml.load(f)
        self.curse_order = config["Plan"]["Course_order"]
    def Get_Source(self):
        self.url_list = Data.Fixed_Data(output="Url").Return_Data()
        self.data = Data.Fixed_Data(output="Data").Return_Data()
        self.params = Data.Fixed_Data(output="Params").Return_Data()

    def main(self,index,params):
        res = self.session.get(url=self.url_list[0],params=params).text
        res = self.session.post(url=self.url_list[0],params=params,data=self.data).json()
        #print(res)


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

class Main:
    def __init__(self):
        pass

if __name__ == '__main__':
    print(Select_Class(None).curse_order)