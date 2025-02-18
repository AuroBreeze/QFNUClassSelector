class Fixed_Data:
    # 固定提交的表单
    # sEcho=1&iColumns=12&sColumns=&iDisplayStart=0&iDisplayLength=15&mDataProp_0=kch&mDataProp_1=kcmc&mDataProp_2=fzmc&mDataProp_3=xf&mDataProp_4=skls&mDataProp_5=sksj&mDataProp_6=skdd&mDataProp_7=xqmc&mDataProp_8=xkrs&mDataProp_9=syrs&mDataProp_10=ctsm&mDataProp_11=czOper
    def __init__(self,output,kcxx="",skls="",skxq="",skjc="",sfym="false",sfct="false",sfxx="true",skxq_xx0103=""):

        self.output = output # 返回固定参数
        self.parmas = {
            "kcxx": kcxx,# kcxx ：课程(URL编码)
            "skls": skls,# skls 老师(URL编码)
            "skxq": skxq,# skxq 星期 1 2 3 4 5 6 7 可为空
            "skjc": skjc,# skjc 节次 1-2- 3-4- 5-6- 7-8- 9-10-11 12-13- 可为空
            "sfym": sfym,# sfym 是否过滤已满的课程 默认false
            "sfct": sfct,# sfct 是否过滤冲突的课程 默认false
            "sfxx": sfxx,# sfxx 是否过滤限选的课程 默认true
            "skxq_xx0103": skxq_xx0103# skxq_xx0103 1:曲阜 2：日照 68FD936EFC564F6E88EC852F9E8019C2：曲阜西校区
        }
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
        if self.output == "Params":
            return self.parmas


# 选课学分情况 http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xsxk_tzsm
# 必修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInBxxk
# 选修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInXxxk 查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkXxxk?
# 本学期计划选课.json http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInBxqjhxk 查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkBxqjhxk?
# 专业内跨年级选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInKnjxk  查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkKnjxk?
# 计划外选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInFawxk 查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkFawxk?
# 公选课选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk 查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?
# 辅修选课 http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/comeInFxzyxk 查询请求：http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkFxxk?