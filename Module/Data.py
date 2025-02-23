from Module import Logging
import toml

class Fixed_Data:
    def __init__(self, output, kcxx, skls, skxq, skjc, sfym, sfct, sfxx, skxq_xx0103):
        self.log = Logging.Log("Data")
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

    def Load_Config(self, config_file="./params.json"):  # 加载配置文件
        pass

    def Return_Data(self):  # 拼接查询需要的参数
        if self.output == None:
            return
        elif self.output == "Data":
            return self.data_str
        else:
            self.log.main("ERROR", "Return_Data: 无效的请求参数")

# 退选API：http://zhjw.qfnu.edu.cn/jsxsd/xsxkjg/xstkOper?jx0404id=202420252011613&tkyy=&_=1739945760325 退课请求参数：jx0404id 课程号，tkyy 退课原因，_ 时间戳