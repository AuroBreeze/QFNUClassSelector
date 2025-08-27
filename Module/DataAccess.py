import json
from Module import Logging
from Module.ConfigService import ConfigService

class DataAccess:
    def __init__(self):
        self.log = Logging.Log("DataAccess")
        self._urls = [
            "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkXxxk",  # 选修选课API
            "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkBxqjhxk",  # 本学期计划选课API
            "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkKnjxk",  # 专业内跨年级选课API
            "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkFawxk",  # 计划外选课API
            "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk",  # 公选课选课API
            "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkFxxk",  # 辅修选课API
        ]
        self._query_data = {
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
            "mDataProp_11": "czOper",
        }

    def get_urls(self):
        return self._urls

    def get_query_data(self):
        return self._query_data

    def load_params(self, path: str = None):
        # 优先使用传入的 path；否则尝试从配置 Paths.params 获取；最后回退默认路径
        cfg_path = ConfigService().get_value("Paths", "params", "./params.json")
        target = path or cfg_path or "./params.json"
        try:
            with open(target, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.log.main("ERROR", f"读取参数文件失败: {e}, 路径: {target}")
            raise
