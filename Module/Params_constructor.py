import json
from itertools import product
from Module import Logging,URL_encode
from Module.ConfigService import ConfigService

class ParamsConstructor:
    def __init__(self):
        self.log = Logging.Log("Params_constructor")
        # 生成的参数应包含的稳定键名
        self._expected_keys = {"kcxx", "skls", "skxq", "skjc", "sfym", "sfct", "sfxx", "skxq_xx0103"}
        try:
            plan_cfg = ConfigService().get_plan()
        except Exception:
            self.log.main("ERROR","读取配置失败，退出程序")
            exit()

        self.course_name = plan_cfg.get("Course_name", [])
        self.teachers_name = plan_cfg.get("Teachers_name", [])
        self.time_period = plan_cfg.get("Time_period", [])
        self.week_day = plan_cfg.get("Week_day", [])

        # 规范化与校验
        self._normalize_and_validate()

    def _normalize_and_validate(self):
        n = len(self.course_name)
        if not isinstance(self.teachers_name, list):
            self.teachers_name = []
        if not isinstance(self.time_period, list):
            self.time_period = []
        if not isinstance(self.week_day, list):
            self.week_day = []

        # 对齐长度：当子列表数量少于课程数量时，补空列表
        if len(self.teachers_name) < n:
            self.log.main("WARN", f"Teachers_name 数量({len(self.teachers_name)})少于 Course_name 数量({n})，将以空列表补齐")
            self.teachers_name += [[] for _ in range(n - len(self.teachers_name))]
        if len(self.time_period) < n:
            self.log.main("WARN", f"Time_period 数量({len(self.time_period)})少于 Course_name 数量({n})，将以空列表补齐")
            self.time_period += [[] for _ in range(n - len(self.time_period))]
        if len(self.week_day) < n:
            self.log.main("WARN", f"Week_day 数量({len(self.week_day)})少于 Course_name 数量({n})，将以空列表补齐")
            self.week_day += [[] for _ in range(n - len(self.week_day))]

        # 若多出元素，记录告警但保留（不影响按索引迭代）
        if len(self.teachers_name) > n:
            self.log.main("WARN", f"Teachers_name 数量({len(self.teachers_name)})多于 Course_name 数量({n})，多余项将被忽略")
        if len(self.time_period) > n:
            self.log.main("WARN", f"Time_period 数量({len(self.time_period)})多于 Course_name 数量({n})，多余项将被忽略")
        if len(self.week_day) > n:
            self.log.main("WARN", f"Week_day 数量({len(self.week_day)})多于 Course_name 数量({n})，多余项将被忽略")

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
            #course = str(URL_encode.Encode(course).Get_encode())
            #teachers = [str(URL_encode.Encode(teacher).Get_encode()) for teacher in teachers]#转为URL编码格式

            # 防出错 + 规范化：去除首尾空白；过滤纯空字符串；保留整体为空时的占位逻辑
            course = str(course).strip()
            teachers = [str(teacher).strip() for teacher in teachers if str(teacher).strip() != ""]
            time = [str(t).strip() for t in time if str(t).strip() != ""]
            week = [str(w).strip() for w in week if str(w).strip() != ""]
            
            #检测
            self.log.main("DEBUG","转为URL编码格式后的数据，请查看下列数据")
            self.log.main("DEBUG",f"课程名称：{course}, 教师名称：{teachers}, 时间段：{time}, 星期：{week}")
            
            # 生成对应子列表的全排列
            # 对空或仅包含空字符串的列表使用占位符[""]，以便仍能按教师展开
            teachers_list = teachers if teachers else [""]
            time_list = time if time else [""]
            week_list = week if week else [""]

            combinations = list(product([course], teachers_list, time_list, week_list))
            
            course_params = []
            seen = set()
            for combination in combinations:
                course, teachers, time, week = combination
                # 确保每个字段只有一个值
                teacher = teachers if teachers else ""
                period = time if time else ""
                day = week if week else ""
                sig = (teacher, period, day)
                if sig in seen:
                    continue
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
                seen.add(sig)
            params_dict[course] = course_params
        
        return params_dict

    # 仅返回内存结果的读取接口（读/写分离）
    def get_params(self):
        params = self.generate_params()
        self._validate_params_structure(params)
        return params

    # 校验每条参数的键名稳定性与完整性
    def _validate_params_structure(self, params_dict: dict):
        for cname, plist in params_dict.items():
            for p in plist:
                keys = set(p.keys())
                if not self._expected_keys.issubset(keys):
                    missing = self._expected_keys - keys
                    self.log.main("ERROR", f"课程[{cname}] 参数缺少必要键: {missing}")
                    raise ValueError(f"params missing keys: {missing}")
        # 可扩展：对值类型做进一步校验

    # 打印参数生成摘要统计
    def _summarize(self, params_dict: dict):
        total = 0
        for cname, plist in params_dict.items():
            cnt = len(plist)
            total += cnt
            self.log.main("INFO", f"参数生成：课程[{cname}] 组合数={cnt}")
        self.log.main("INFO", f"参数生成：总组合数={total}")

    def write_to_json(self, file_path="./params.json"):
        try:
            params_dict = self.generate_params()
            self._validate_params_structure(params_dict)
            self._summarize(params_dict)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(params_dict, f, ensure_ascii=False, indent=4, sort_keys=True)
            self.log.main("INFO", f"params.json文件已生成，路径：{file_path}")

        except Exception as e:
            self.log.main("ERROR", f"params.json文件生成失败，错误信息：{e}")
            self.log.main("ERROR","退出程序")
            exit()

# 实例化ParamsConstructor并生成params.json文件
# constructor = ParamsConstructor()
# constructor.write_to_json()

if __name__ == '__main__':
    constructor = ParamsConstructor()
    constructor.write_to_json()