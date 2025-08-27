from Module import Logging, URL_encode
from Module.NetUtils import NetUtils
import time
import os
import json
from Module.ConfigService import ConfigService
from Module.DataAccess import DataAccess 

class Load_Source:  # 载入所有必须的资源
    def __init__(self):
        self.log = Logging.Log("Load_Source")

        self.Get_Course_order()
        self.Get_Source()

        self.Candidate = False

    def Get_Course_order(self):
        plan = ConfigService().get_plan()
        time_cfg = ConfigService().get_time()
        self.curse_order = plan.get("Course_order", [])
        self.curse_name = plan.get("Course_name", [])
        self.interval = time_cfg.get("Interval", 1)  # 获取配置文件中的间隔时间(毫秒)

    def Get_Source(self):
        self._da = DataAccess()
        self.url_list = self._da.get_urls()
        self.data = self._da.get_query_data()
        self.params = self._da.load_params()

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
        elif output == "Interval":
            return self.interval
        else:
            self.log.main("WARN", "参数错误，请检测参数设置")
        pass


class Submit_ClassSelection:
    def __init__(self,session,jx0404id,kcid):
        self.session = session
        self.log = Logging.Log("Submit_ClassSelection")
        self.net = NetUtils()
        # 获取时间戳
        self.timestamp = int(round(time.time() * 1000))
        # print(timestamp)

        self.jx0404id = jx0404id
        self.kcid = kcid
        # 请求超时配置
        self.request_timeout = ConfigService().get_value("Time", "request_timeout_sec", 10)

    def main(self):
        # 预检
        pre_url = f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/iscx?jx0404id={str(self.jx0404id)}&kcid={str(self.kcid)}"
        resp, err = self.net.request_with_retry(self.session, "GET", pre_url, timeout=self.request_timeout)
        if err is not None and err not in ("ok",):
            self.log.main("ERROR", f"预检请求失败: {err}")
            return False

        try:
            url_submit = (
                f"http://zhjw.qfnu.edu.cn/jsxsd/xsxkkc/knjxkOper?kcid={str(self.kcid)}&cfbs=null&jx0404id={str(self.jx0404id)}&xkzy=&trjf=&_="
                + str(self.timestamp)
            )
            r, err = self.net.request_with_retry(self.session, "GET", url_submit, timeout=self.request_timeout)
            if err is not None and err not in ("ok",):
                # 非致命网络/服务器错误已重试，返回失败
                self.log.main("DEBUG", f"选课请求失败: {err}")
                return False
            # 优先解析JSON
            try:
                res_json = r.json()
                msg = res_json.get("message", "")
                if "成功" in msg:
                    self.log.main("INFO", "✅ 选课成功")
                    return True
            except Exception:
                pass
            # 回退到文本包含判断
            txt = r.text if r is not None else ""
            if "选课成功" in txt or '成功' in txt:
                self.log.main("INFO", "✅ 选课成功")
                return True
            self.log.main("DEBUG", f"🔍 选课返回：{txt[:200]}")
            return False
        except Exception as e:
            self.log.main("ERROR", f"提交选课请求失败: {e}")
            return False

class Select_Class:
    def __init__(self, session):
        self.session = session  # 继承session数据
        self.log = Logging.Log("Select_Class")
        self.request_timeout = ConfigService().get_value("Time","request_timeout_sec",10)

        self.Order_list = Load_Source().Return_Data("Order")  # 载入设置的选课顺序列表
        
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
        self.sleep_time = Load_Source().Return_Data("Interval")

        self.jx0404id = None
        self.jx02id_get = None
        # 标记最近一次查询是否命中空 aaData（页面无该课程）
        self._aa_empty = False

    def Get_Json_data(self, index, params, data):  # 发送请求包，获取课程数据
        try:
            # 预热 GET（很多场景服务端记录上一次访问）
            _, _ = NetUtils().request_with_retry(self.session, "GET", self.url_list[index], params=params, timeout=self.request_timeout)
            # 主请求 POST
            resp, err = NetUtils().request_with_retry(self.session, "POST", self.url_list[index], params=params, data=data, timeout=self.request_timeout)
            if err is not None and err not in ("ok",):
                self.log.main("DEBUG", f"课程查询失败: {err}")
                return {}
            try:
                obj = resp.json() if resp is not None else {}
                try:
                    snippet = json.dumps(obj, ensure_ascii=False)[:500]
                    self.log.main("DEBUG", f"🔎 JSON返回片段: {snippet}")
                except Exception:
                    pass
                return obj
            except Exception:
                self.log.main("ERROR", "课程查询返回非JSON，尝试从文本解析失败")
                self.log.main("DEBUG", f"🔍 返回片段: {resp.text[:200] if resp is not None else ''}")
                return {}
        except Exception as e:
            self.log.main("ERROR", f"获取课程数据失败: {e}")
            return {}

    def run(self):
        while True:
            if self.Check_failed_courses()==True:
                self.log.main("INFO", "✅ 抢课模式运行中......")
                #执行正常抢课
                for i in range(len(self.Order_list)):
                    if self.Order_list[i] == []:
                        self.default_order()  # 默认选课顺序
                        continue
                    self.plan_order(self.Order_list[i])  # 已设置的选课顺序
                generated = self.Save_Failed_Courses_To_Json()
                # 如果本轮没有失败（不生成失败列表文件），则结束主循环，避免无限正常模式循环
                if not generated:
                    self.log.main("INFO", "✅ 本轮没有失败项，结束运行")
                    break
            else:#存在失败的课程
                self.log.main("INFO", "❌蹲课模式运行中......")
                time.sleep(5)
                self.failed_order(self.Order_list_fail)

    def failed_order(self,config):#候选选课
        count = 0
        while True:
            try:
                with open("./failed_courses.json","r",encoding="utf-8") as f:
                    self.Order_fail = json.load(f)

                judge_json=False
                for index,value in self.Order_fail.items():
                    if value!=[]:
                        judge_json=True
                if judge_json==False:
                    self.log.main("INFO", "✅全部课程选择成功")
                    break

            except:
                self.log.main("ERROR","❌ 读取失败课程列表失败，请检查failed_courses.json文件是否存在")
            self.Order_list_fail = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": []}  # 清空选课失败的课程，准备重新写入
            for index, courses in self.Order_fail.items():
                index = int(index)
                for name in courses:
                    try:
                        judge_submit = False
                        total = len(self.params[name])
                        for p_idx, name_params in enumerate(self.params[name], start=1):
                            self.log.main("DEBUG", f"🔁 [{self.name_url[index]}] 课程“{name}” 使用第 {p_idx}/{total} 个参数进行查询")
                            json_data = self.Get_Json_data(
                                index=index, params=name_params, data=self.data
                            )
                            judge = self.Json_Process(json_data)

                            if judge:
                                judge_submit = Submit_ClassSelection(self.session, self.jx0404id,
                                                                     self.jx02id_get).main()
                                if judge_submit:
                                    self.log.main("INFO",
                                                  f"✅ {name}选课成功，选课所在页面:{self.name_url[index]}，选课网址:{self.url_list[index]}")
                                    if name in self.course_name:
                                        self.course_name.remove(name)
                                    break
                            else:
                                pass
                        if judge_submit:
                            break
                        else:
                            if self._aa_empty:
                                self.log.main("INFO", f"ℹ️ {self.name_url[index]} 无该课程“{name}”，已跳过失败记录")
                            else:
                                self.log.main("WARN", f"⚠️ {name}选课失败，程序选课所在页面{self.name_url[index]}，选课网址:{self.url_list[index]} ")
                                self.Order_list_fail[str(index)].append(name)

                    except Exception as e:
                        self.log.main("ERROR", f"❌ {self.name_url[index]}请求失败:{self.url_list[index]}")
                        self.log.main("ERROR", f"❌ 失败原因：{e}")
                        self.Order_list_fail[str(index)].append(name)
            judge_success = self.Save_Failed_Courses_To_Json()
            if judge_success == False:
                self.log.main("INFO","✅全部课程选择成功")
                break

            count+=1
            self.log.main("INFO", f"✅ 蹲课模式运行中,等待总时间：{count * self.sleep_time}秒,间隔时间为:{self.sleep_time}秒")
            time.sleep(self.sleep_time)


    def default_order(self):
        for name in list(self.course_name):
            for index in range(len(self.url_list)):
                try:
                    judge_submit = False
                    total = len(self.params[name])
                    for p_idx, name_params in enumerate(self.params[name], start=1):
                        self.log.main("DEBUG", f"🔁 [{self.name_url[index]}] 课程“{name}” 使用第 {p_idx}/{total} 个参数进行查询")
                        json_data = self.Get_Json_data(
                                index=index, params=name_params, data=self.data
                            )
                        judge = self.Json_Process(json_data)

                        if judge:
                            judge_submit = Submit_ClassSelection(self.session, self.jx0404id,
                                                                     self.jx02id_get).main()
                            if judge_submit:
                                self.log.main("INFO", f"✅ {name}选课成功，选课所在页面:{self.name_url[index]}，选课网址:{self.url_list[index]}")
                                if name in self.course_name:
                                    self.course_name.remove(name)
                                break
                        else:
                            pass
                    if judge_submit:
                        break
                    else:
                        if self._aa_empty:
                            self.log.main("INFO", f"ℹ️ {self.name_url[index]} 无该课程“{name}”，已跳过失败记录")
                        else:
                            self.log.main("WARN", f"⚠️ {name}选课失败，选课所在页面:{self.name_url[index]}，选课网址:{self.url_list[index]}")
                            self.Order_list_fail[str(index)].append(name)

                except Exception as e:
                    self.log.main("ERROR", f"❌ {self.name_url[index]}请求失败:{self.url_list[index]}")
                    self.log.main("ERROR", f"❌ 失败原因：{e}")
                    self.Order_list_fail[str(index)].append(name)
        # 重新载入选课列表（避免使用未定义的 self._da）
        self.url_list = Load_Source().Return_Data("URL")


    def plan_order(self, Order_list):
        for index in Order_list:
            if index == "":
                self.default_order()
                continue
            else:
                index = int(index)
                # 不修改url_list，避免索引错位
                for name in list(self.course_name):
                    try:
                        judge_submit = False
                        total = len(self.params[name])
                        for p_idx, name_params in enumerate(self.params[name], start=1):
                            self.log.main("DEBUG", f"🔁 [{self.name_url[index]}] 课程“{name}” 使用第 {p_idx}/{total} 个参数进行查询")
                            json_data = self.Get_Json_data(
                                index=index, params=name_params, data=self.data
                            )
                            judge = self.Json_Process(json_data)

                            if judge:
                                judge_submit = Submit_ClassSelection(self.session, self.jx0404id,
                                                                     self.jx02id_get).main()
                                if judge_submit:
                                    self.log.main("INFO", f"✅ {name}选课成功")
                                    if name in self.course_name:
                                        self.course_name.remove(name)
                                    break
                            else:
                                pass
                        if judge_submit:
                            break
                        else:
                            if self._aa_empty:
                                self.log.main("INFO", f"ℹ️ {self.name_url[index]} 无该课程“{name}”，已跳过失败记录")
                            else:
                                self.log.main("WARN", f"⚠️ {name}选课失败，选课所在页面:{self.name_url[index]}，选课网址:{self.url_list[index]}")
                                self.Order_list_fail[str(index)].append(name)
                    except Exception as e:
                        self.log.main("ERROR", f"❌ {self.name_url[index]}请求失败:{self.url_list[index]}")
                        self.log.main("ERROR", f"❌ 失败原因：{e}")
                        self.Order_list_fail[str(index)].append(name)

    def Json_Process(self,json_data) -> bool:
        """解析课程查询结果
        返回 True: 命中课程，可继续提交
        返回 False: 未命中课程；若 aaData 为空，则标记页面无此课程，用于不加入失败列表
        """
        self._aa_empty = False
        try:
            if isinstance(json_data, dict) and "aaData" in json_data:
                aa = json_data.get("aaData", [])
                if isinstance(aa, list) and len(aa) == 0:
                    # 页面无此课程，标记以便调用方不加入失败列表
                    self._aa_empty = True
                    self.log.main("DEBUG", "🔍 aaData 为空：该页面无此课程")
                    return False
                Data = aa[0]
                self.jx0404id = str(Data["jx0404id"])
                self.jx02id_get = str(Data["jx02id"])
                return True
        except Exception:
            pass
        self.log.main("DEBUG","🔍 未查询到所选课程（非空aaData或结构异常）")
        self.log.main("DEBUG",f"🔍 json数据:{json_data}")
        return False

    def Save_Failed_Courses_To_Json(self):
        """将未选课成功的结果保存到json文件中"""
        failed_courses = {}
        is_empty = True  # 标记是否所有列表为空
        for index, courses in self.Order_list_fail.items():
            if courses:
                # 对课程列表进行去重
                failed_courses[str(index)] = list(set(courses))
                is_empty = False  # 如果有非空列表，标记为False

        if is_empty:
            # 若此前存在失败列表文件，删除之，保持语义一致：本轮全部成功 => 无失败列表
            try:
                if os.path.exists("./failed_courses.json"):
                    os.remove("./failed_courses.json")
            except Exception:
                pass
            self.log.main("INFO", "✅ 全部课程选择成功，本轮未生成失败列表")
            return False  # 如果所有列表为空，返回False

        try:
            with open("./failed_courses.json", "w", encoding="utf-8") as f:
                import json
                json.dump(failed_courses, f, ensure_ascii=False, indent=4)
            self.log.main("INFO", "未选课成功的课程已保存到failed_courses.json文件中")
            return True
        except Exception as e:
            self.log.main("ERROR", f"保存未选课成功的课程到文件时出错: {e}")
            return False

    def Check_failed_courses(self):
        try:
            if not os.path.exists("./failed_courses.json"):
                return True
            with open("./failed_courses.json", "r", encoding="utf-8") as f:
                import json
                failed_courses = json.load(f)
                # 若存在任意非空列表则返回字典，否则返回True表示无失败项
                has_any = any(courses for courses in failed_courses.values())
                return failed_courses if has_any else True
        except Exception as e:
            self.log.main("ERROR", f"读取未选课成功的课程时出错: {e}")
            return True

if __name__ == "__main__":
    Select_Class(None)
    pass