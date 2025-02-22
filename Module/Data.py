from Module import Logging
import toml

class Fixed_Data:
    def __init__(self, output, kcxx, skls, skxq, skjc, sfym, sfct, sfxx, skxq_xx0103):
        self.log = Logging.Log("Data")

        self.output = output # 返回固定参数

        self.kcxx = kcxx #课程号
        self.skls = skls #老师
        self.skxq = skxq #星期
        self.skjc = skjc #节次
        self.sfym = sfym #是否过滤已满的课程 默认true
        self.sfct = sfct #是否过滤冲突的课程 默认true
        self.sfxx = sfxx #是否过滤限选的课程 默认true
        self.skxq_xx0103 = skxq_xx0103 #1:曲阜 2：日照 68FD936EFC564F6E88EC852F9E8019C2：曲阜西校区

        self.count_Te_1 = 0 # 教师列表index
        self.count_Te_2 = 0 # 教师子列表index
        self.count_Courses = 0 # 课程数量
        self.time_Pr_1 = 0 # 时间列表index
        self.time_Pr_2 = 0 # 时间子列表index
        self.Wd_1 = 0 # 星期列表index
        self.Wd_2 = 0 # 星期子列表index


        self.parmas = {
            "kcxx": self.kcxx,
            "skls": self.skls,
            "skxq": self.skxq,
            "skjc": self.skjc,
            "sfym": self.sfym,
            "sfct": self.sfct,
            "sfxx": self.sfxx,
            "skxq_xx0103": skxq_xx0103
        }
        self.data_str = {
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
            "mDataProp_11": "czOper"
        }

        self.config = None

    def Load_Config(self, config_file):  # 加载配置文件
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                self.config = toml.load(f)
        except FileNotFoundError:
            self.log.main("ERROR", "Config file not found")
        except Exception as e:
            self.log.main("ERROR", "Failed to load config file: " + str(e))

    def Return_Data(self):  # 拼接查询需要的参数
        if self.output == None:
            return
        elif self.output == "Data":
            return self.data_str
        elif self.output == "Params":
            return self.parmas
        else:
            self.log.main("ERROR", "Return_Data: 无效的请求参数")

# 退选API：http://zhjw.qfnu.edu.cn/jsxsd/xsxkjg/xstkOper?jx0404id=202420252011613&tkyy=&_=1739945760325 退课请求参数：jx0404id 课程号，tkyy 退课原因，_ 时间戳