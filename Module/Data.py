from Module import Logging
import json

class Fixed_Data:
    def __init__(self,output="Data"):
        self.log = Logging.Log("Data")
        
        self.output = output
        
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

        
        try:
            with open("./params.json","r",encoding="utf-8") as f:
                self.config_json = json.load(f)
        except:
            self.log.main("ERROR", "Fixed_Data: 读取配置文件(params.json)失败")
            self.log.main("ERROR","程序已退出")
            exit()

    def Return_Data(self):  # 拼接查询需要的参数
        if self.output == None:
            return
        elif self.output == "Data":
            return self.data_str
        elif self.output == "Params":
            return self.config_json
        else:
            self.log.main("ERROR", "Return_Data: 无效的请求参数")

# 退选API：http://zhjw.qfnu.edu.cn/jsxsd/xsxkjg/xstkOper?jx0404id=202420252011613&tkyy=&_=1739945760325 退课请求参数：jx0404id 课程号，tkyy 退课原因，_ 时间戳

if __name__ == "__main__":
    Fixed_Data = Fixed_Data("Data", None)
    pass