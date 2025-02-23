import json
from itertools import product
import toml

class ParamsConstructor:
    def __init__(self, course_name, teachers_name, time_period, week_day):
        self.course_name = course_name
        self.teachers_name = teachers_name
        self.time_period = time_period
        self.week_day = week_day

    def generate_params(self):
        # 构造params列表
        params_list = []
        for i, course in enumerate(self.course_name):
            # 获取对应索引的子列表
            teachers = self.teachers_name[i] if i < len(self.teachers_name) else []
            time = self.time_period[i] if i < len(self.time_period) else []
            week = self.week_day[i] if i < len(self.week_day) else []
            
            # 生成对应子列表的全排列
            combinations = list(product([course], teachers, time, week))
            
            # 如果子列表为空，生成一个包含空字段的组合
            if not combinations:
                combinations = [(course, "", "", "")]
            
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
                params_list.append(params)
        
        return params_list

    def write_to_json(self, file_path):
        params_list = self.generate_params()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(params_list, f, ensure_ascii=False, indent=4)

# 从config.toml文件中读取配置
config = toml.load("/home/aurobreeze/code/Python/QFNUClassSelector/config.toml")
course_name = config["Plan"]["Course_name"]
teachers_name = config["Plan"]["Teachers_name"]
time_period = config["Plan"]["Time_period"]
week_day = config["Plan"]["Week_day"]

# 实例化ParamsConstructor并生成params.json文件
constructor = ParamsConstructor(course_name, teachers_name, time_period, week_day)
constructor.write_to_json("params.json")