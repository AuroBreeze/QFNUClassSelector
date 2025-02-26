from Module import Logging, Data
import time
import toml


class Load_Source:  # 载入所有必须的资源
    def __init__(self):
        self.log = Logging.Log("Load_Source")
        # self.url = "http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk"

        self.Get_Course_order()
        self.Get_Source()

    def Get_Course_order(self):
        with open("./config.toml", "r", encoding="utf-8") as f:
            config = toml.load(f)
        self.curse_order = config["Plan"]["Course_order"]
        self.curse_name = config["Plan"]["Course_name"]

    def Get_Source(self):
        self.url_list = Data.Fixed_Data(output="URL").Return_Data()
        self.data = Data.Fixed_Data(output="Data").Return_Data()
        self.params = Data.Fixed_Data(output="Params").Return_Data()

    def Return_Data(self, output):
        if output == "Params":
            return self.params
        elif output == "Data":
            return self.data
        elif output == "URL":
            return self.url_list
        elif output == "Order":
            return self.curse_order
        elif output == "Name":
            return self.curse_name
        else:
            self.log.main("WARN", "参数错误，请检测参数设置")
        pass


class Submit_ClassSelection:
    def __init__(self, session, jx0404id="202420252011613", kcid="530128"):
        self.session = session
        self.log = Logging.Log("Submit_ClassSelection")
        # 获取时间戳
        self.timestamp = int(round(time.time() * 1000))
        # print(timestamp)
        res = session.get(
            url=f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/iscx?jx0404id={str(jx0404id)}&kcid={str(kcid)}"
        ).text
        # print(res)
        res = session.get(
            url=f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/knjxkOper?kcid={str(kcid)}&cfbs=null&jx0404id={str(jx0404id)}&xkzy=&trjf=&_="
            + str(self.timestamp)
        ).text
        # print(res)
        self.log.main("INFO", res)


class Select_Class:
    def __init__(self, session):
        self.session = session  # 继承session数据
        self.log = Logging.Log("Select_Class")
        self.Order_list = Load_Source().Return_Data("Order")  # 载入选课顺序列表
        self.url_list = Load_Source().Return_Data("URL")  # 载入默认选课列表
        self.course_name = Load_Source().Return_Data("Name")  # 载入课程名称列表
        self.params = Load_Source().Return_Data("Params")  # 载入默认请求参数
        self.data = Load_Source().Return_Data("Data")  # 载入默认请求数据

    def Get_Json_data(self, index, params, data):  # 发送请求包，获取课程数据
        res = self.session.get(url=self.url_list[index], params=params).text
        json_data = self.session.post(
            url=self.url_list[index], params=params, data=data
        ).json()
        return json_data

    def run(self):
        for i in range(len(self.Order)):
            if self.Order[i] == []:
                self.default_order()  # 默认选课顺序
                continue
            for j in range(len(self.Order[i])):
                if self.Order[i][j] == "":
                    self.default_order()
                    continue
                self.plan_order(self.Order[i][j])  # 已设置的选课顺序

    def default_order(self):
        for index in range(len(self.url_list)):
            try:
                for name in self.course_name:
                    for name_params in self.params[name]:
                        json_data =self.Get_Json_data(
                            index=index, params=self.params, data=self.data
                        )
                        judge = self.Json_Process(json_data)
                        
                        if judge:
                            Submit_ClassSelection(self.session)
                        
            except Exception as e:
                self.log.main("ERROR", f"{self.url_list[index]}请求失败")
                self.log.main("ERROR", f"失败原因：{e}")

            pass
        pass

    def plan_order(self, index):
        pass

    def Json_Process(self,json_data) -> bool:
        pass
if __name__ == "__main__":
    Select_Class().run()
