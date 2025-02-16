class Select_Class:
    def __init__(self,session,Fixed_Data,kcxx="",skls="",skxq="",skjc="",sfym="false",sfct="false",sfxx="true",skxq_xx0103=""):
        self.frame = Fixed_Data(output="Frame",kcxx=kcxx, skls=skls, skxq=skxq, skjc=skjc, sfym=sfym, sfct=sfct, sfxx=sfxx, skxq_xx0103=skxq_xx0103).Return_Data()
        self.data = Fixed_Data(output="Data").Return_Data()
        self.session = session
        self.url = "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?" + self.frame
        print(self.url)

    def main(self):
        res = self.session.get(url=self.url).text
        res = self.session.post(url=self.url,data=self.data).json()
        print(res)

