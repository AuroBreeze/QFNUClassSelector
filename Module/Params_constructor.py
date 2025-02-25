import json
from itertools import product
import toml
from Module import Logging,URL_encode

class ParamsConstructor:
    def __init__(self):
        self.log = Logging.Log("Params_constructor")
        try:
            # 从config.toml文件中读取配置
            self.config = toml.load("./config.toml")
        except Exception as e:
            self.log.main("ERROR","config.toml文件读取失败，请检查文件路径或格式是否正确")
            self.log.main("ERROR","退出程序")
            exit()

        self.course_name = self.config["Plan"]["Course_name"]
        self.teachers_name = self.config["Plan"]["Teachers_name"]
        self.time_period = self.config["Plan"]["Time_period"]
        self.week_day = self.config["Plan"]["Week_day"]

    def generate_params(self):
        # 构造params字典，键为课程名称，值为该课程对应的参数列表
        params_dict = {}
        for i, course in enumerate(self.course_name):
            
            # 获取对应索引的子列表
            teachers = self.teachers_name[i] if i < len(self.teachers_name) else []
            #print(teachers)
            
            time = self.time_period[i] if i < len(self.time_period) else []
            week = self.week_day[i] if i < len(self.week_day) else []
            
            
            #检测
            self.log.main("DEBUG","生成检测数据，请查看下列数据")
            self.log.main("DEBUG",f"课程名称：{course}, 教师名称：{teachers}, 时间段：{time}, 星期：{week}")
            
            
            # 转为URL编码格式
            course = str(URL_encode.Encode(course).Get_encode())
            teachers = [str(URL_encode.Encode(teacher).Get_encode()) for teacher in teachers]#转为URL编码格式
            
            #检测
            self.log.main("DEBUG","转为URL编码格式后的数据，请查看下列数据")
            self.log.main("DEBUG",f"课程名称：{course}, 教师名称：{teachers}, 时间段：{time}, 星期：{week}")
            
            # 生成对应子列表的全排列
            combinations = list(product([course], teachers, time, week))
            
            
            # 如果子列表为空，生成一个包含空字段的组合
            if not combinations:
                combinations = [(course, "", "", "")]

            course_params = []
            for combination in combinations:
                course, teachers, time, week = combination
                # 确保每个字段只有一个值
                teacher = teachers if teachers else ""
                period = time if time else ""
                day = week if week else ""
                params = {
                    "kcxx": course,
                    "skls": teacher,
                    "skxq": day,
                    "skjc": period,
                    "sfym": True,
                    "sfct": True,
                    "sfxx": True,
                    "skxq_xx0103": 1
                }
                course_params.append(params)
            params_dict[course] = course_params
        
        return params_dict

    def write_to_json(self, file_path="./params.json"):
        try:
            params_dict = self.generate_params()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(params_dict, f, ensure_ascii=False, indent=4)
            self.log.main("INFO", f"params.json文件已生成，路径：{file_path}")

        except Exception as e:
            self.log.main("ERROR", f"params.json文件生成失败，错误信息：{e}")
            self.log.main("ERROR","退出程序")
            exit()

# 实例化ParamsConstructor并生成params.json文件
constructor = ParamsConstructor()
constructor.write_to_json()