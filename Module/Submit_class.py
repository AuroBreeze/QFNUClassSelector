import time

class Submit_ClassSelection:
    def __init__(self,session,jx0404id="202420252011613",kcid="530128"):
        self.session = session
        # 获取时间戳
        self.timestamp = int(round(time.time() * 1000))
        #print(timestamp)
        res = session.get(url=f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/iscx?jx0404id={str(jx0404id)}&kcid={str(kcid)}").text
        #print(res)
        res = session.get(
            url=f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/knjxkOper?kcid={str(kcid)}&cfbs=null&jx0404id={str(jx0404id)}&xkzy=&trjf=&_=" + str(
                self.timestamp)).text
        print(res)

