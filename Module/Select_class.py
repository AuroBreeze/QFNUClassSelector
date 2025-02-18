class Select_Class:
    def __init__(self,session,Fixed_Data,kcxx="",skls="",skxq="",skjc="",sfym="false",sfct="false",sfxx="true",skxq_xx0103=""):
        self.params = Fixed_Data(output="Params",kcxx=kcxx, skls=skls, skxq=skxq, skjc=skjc, sfym=sfym, sfct=sfct, sfxx=sfxx, skxq_xx0103=skxq_xx0103).Return_Data()
        self.data = Fixed_Data(output="Data").Return_Data()
        self.session = session
        self.url = "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk"

    def main(self):
        res = self.session.get(url=self.url,params=self.params).text
        res = self.session.post(url=self.url,params=self.params,data=self.data).json()
        print(res)

