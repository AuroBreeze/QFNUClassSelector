from Module import Logging, Data
import time
import toml

class Load_Source:  # 载入所有必须的资源
    def __init__(self):
        self.log = Logging.Log("Load_Source")

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
    def __init__(self,session,jx0404id,kcid):
        self.session = session
        self.log = Logging.Log("Submit_ClassSelection")
        # 获取时间戳
        self.timestamp = int(round(time.time() * 1000))
        # print(timestamp)

        self.jx0404id = jx0404id
        self.kcid = kcid

    def main(self):

        res = self.session.get(
            url=f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/iscx?jx0404id={str(self.jx0404id)}&kcid={str(self.kcid)}"
        ).text
        # print(res)
        res = self.session.get(
            url=f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/knjxkOper?kcid={str(self.kcid)}&cfbs=null&jx0404id={str(self.jx0404id)}&xkzy=&trjf=&_="
                + str(self.timestamp)
        ).text
        try:
            if res["message"] == "选课成功":
                self.log.main("INFO", "✅ 选课成功")
                return True
        except:
            self.log.main("DEBUG", f"🔍 Post返回json数据：{res}")
            return False

class Select_Class:
    def __init__(self, session):
        self.session = session  # 继承session数据
        self.log = Logging.Log("Select_Class")

        self.Order_list = Load_Source().Return_Data("Order")  # 载入设置的选课顺序列表
        self.Order_list_success ={
            "0": [],
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": []
            } #增加搜索到的课程所在的URL
        
        self.Order_list_fail = {
            "0": [],
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": []
            } #增加搜索失败的课程所在的URL
        
        self.url_list = Load_Source().Return_Data("URL")  # 载入默认选课列表
        self.name_url = ["选修选课","本学期计划选课","专业内跨年级选课","计划外选课","公选课选课","辅修选课"]

        self.course_name = Load_Source().Return_Data("Name")  # 载入课程名称列表
        self.params = Load_Source().Return_Data("Params")  # 载入默认请求参数
        self.data = Load_Source().Return_Data("Data")  # 载入默认请求数据

        self.jx0404id = None
        self.jx02id_get = None

    def Get_Json_data(self, index, params, data):  # 发送请求包，获取课程数据
        res = self.session.get(url=self.url_list[index], params=params).text
        json_data = self.session.post(
            url=self.url_list[index], params=params, data=data
        ).json()
        return json_data

    def run(self):
        for i in range(len(self.Order_list)):
            if self.Order_list[i] == []:
                self.default_order()  # 默认选课顺序
                continue
            self.plan_order(self.Order_list[i])  # 已设置的选课顺序

    def default_order(self):
        for name in self.course_name:
            for index in range(len(self.url_list)):
                try:
                    judge_submit = False
                    for name_params in self.params[name]:
                        json_data = self.Get_Json_data(
                                index=index, params=name_params, data=self.data
                            )
                        judge = self.Json_Process(json_data)

                        if judge:
                            judge_submit = Submit_ClassSelection(self.session, self.jx0404id,
                                                                     self.jx02id_get).main()
                            if judge_submit:
                                self.log.main("INFO", f"✅ {name}选课成功")
                                self.Order_list_success[str(index)].append(name)
                                break
                        else:
                            pass
                    if judge_submit:
                        break
                    else:
                        self.log.main("WARN", f"⚠️ {name}选课失败")
                        self.Order_list_fail[str(index)].append(name)

                except Exception as e:
                    self.log.main("ERROR", f"❌ {self.name_url[index]}请求失败:{self.url_list[index]}")
                    self.log.main("ERROR", f"❌ 失败原因：{e}")
        self.url_list = Load_Source().Return_Data("URL")  # 重新载入选课列表


    def plan_order(self, Order_list):
        for index in Order_list:
            if index == "":
                self.default_order()
                continue
            else:
                index = int(index)
                self.url_list.pop(int(index))
            try:
                for name in self.course_name:
                    judge_submit = False
                    for name_params in self.params[name]:
                        json_data = self.Get_Json_data(
                            index=index, params=name_params, data=self.data
                        )
                        judge = self.Json_Process(json_data)

                        if judge:
                            judge_submit = Submit_ClassSelection(self.session, self.jx0404id, self.jx02id_get).main()
                            if judge_submit:
                                self.log.main("INFO", f"✅ {name}选课成功")
                                self.Order_list_success[str(index)].append(name)
                                break
                        else:
                            pass
                    if judge_submit:
                        break
                    else:
                        self.log.main("WARN", f"⚠️ {name}选课失败")
                        self.Order_list_fail[str(index)].append(name)
            except Exception as e:
                self.log.main("ERROR", f"❌ {self.name_url[index]}请求失败:{self.url_list[index]}")
                self.log.main("ERROR", f"❌ 失败原因：{e}")

    def Json_Process(self,json_data) -> bool:
        try:
            Data = json_data["aaData"][0]
            self.jx0404id = str(Data["jx0404id"])
            self.jx02id = str(Data["jx02id"])
            return True
        except:
            self.log.main("DEBUG","🔍 未查询到所选课程")
            self.log.main("DEBUG",f"🔍 json数据:{json_data}")
            return False
if __name__ == "__main__":
    Select_Class(None)
    pass