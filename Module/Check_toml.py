import toml
from Module import Logging
import re

class main:
    def __init__(self):
        self.bool = True  # True表示配置文件正确，False表示配置文件错误
        try:
            with open('./config.toml', 'r') as f:
                self.config = toml.load(f)
        except FileNotFoundError:
            Logging.Log("Check_config").main("ERROR", '未找到config.toml文件')
            self.bool = False

    def check_config(self):
        required_fields = {
            'Server': ['username', 'password'],
            'Mode': ['Number', 'Select'],
            'Plan': ['Course_name', 'Multiple', 'Multiple_Judge', 'Multiple_account'],
            'Time': ['Start_time', 'End_time']
        }

        for section, fields in required_fields.items():
            if section not in self.config:
                Logging.Log("Check_config").main("ERROR", f'config.toml文件中缺少{section}部分')
                self.bool = False
                continue

            for field in fields:
                if field not in self.config[section]:
                    Logging.Log("Check_config").main("ERROR", f'部分{section}中缺少字段{field}')
                    self.bool = False

        # 新增对username和password长度的检测及对username和password是否为空或全空格的检测
        if 'Server' in self.config:
            username = self.config['Server'].get('username', '')
            password = self.config['Server'].get('password', '')
            if len(username) != len(password):
                Logging.Log("Check_config").main("ERROR", 'config.toml文件中username和password的长度必须一致')
                self.bool = False
            if not username or not password:
                Logging.Log("Check_config").main("ERROR", 'config.toml文件中username和password不能为空')
                self.bool = False
            # 新增检查username和password是否为空或全空格
            for i in range(len(username)):
                if not username[i] or username[i].isspace():
                    Logging.Log("Check_config").main("ERROR", 'config.toml文件中username不能为空或全空格')
                    self.bool = False
            for i in range(len(password)):
                if not password[i] or password[i].isspace():
                    Logging.Log("Check_config").main("ERROR", 'config.toml文件中password不能为空或全空格')
                    self.bool = False

        self.check_mode_section()
        self.check_plan_section()
        self.check_time_section()

    def check_mode_section(self):
        # 检查Mode部分Number字段的值是否为single或multiple
        if self.config['Mode'].get('Number') not in ['single', 'multiple']:
            Logging.Log("Check_config").main("ERROR", 'config.toml文件中Mode部分Number字段的值必须为single或multiple')
            self.bool = False

        # 检查Mode部分Select字段的值是否为Start或End
        for select in self.config['Mode'].get('Select', []):
            if select not in ['Start', 'End']:
                Logging.Log("Check_config").main("ERROR", 'config.toml文件中Mode部分Select字段的值必须为Start或End')
                self.bool = False

    def check_plan_section(self):
        # 检查Plan部分Multiple字段的值是否为true或false
        if self.config['Plan'].get('Multiple') not in [True, False]:
            Logging.Log("Check_config").main("ERROR", 'config.toml文件中Plan部分Multiple字段的值必须为true或false')
            self.bool = False

        # 当Multiple为True时，检查Multiple_Judge的长度是否与Course_name匹配
        if self.config['Plan'].get('Multiple', False):
            course_names = self.config['Plan'].get('Course_name', [])
            multiple_judge = self.config['Plan'].get('Multiple_Judge', [])
            if len(course_names) != len(multiple_judge):
                Logging.Log("Check_config").main("ERROR", 'config.toml文件中Plan部分Multiple_Judge的长度与Course_name不匹配')
                self.bool = False

        # 当Multiple为True时，检查Multiple_account的长度是否与Course_name匹配
            multiple_account = self.config['Plan'].get('Multiple_account', [])
            if len(course_names) != len(multiple_account):
                Logging.Log("Check_config").main("ERROR", 'config.toml文件中Plan部分Multiple_account的长度与Course_name不匹配')
                self.bool = False

        # 检查Course_name的参数数量与Teachers_name，Time_period，Week_day，Multiple_account的子列表数量相同
        course_names = self.config['Plan'].get('Course_name', [])
        teachers_name = self.config.get('Plan', {}).get('Teachers_name', [])
        time_period = self.config.get('Plan', {}).get('Time_period', [])
        week_day = self.config.get('Plan', {}).get('Week_day', [])
        multiple_account = self.config.get('Plan', {}).get('Multiple_account', [])

        if len(course_names) != len(teachers_name):
            Logging.Log("Check_config").main("ERROR", 'config.toml文件中Plan部分Teachers_name的子列表数量与Course_name不匹配')
            self.bool = False
        if len(course_names) != len(time_period):
            Logging.Log("Check_config").main("ERROR", 'config.toml文件中Plan部分Time_period的子列表数量与Course_name不匹配')
            self.bool = False
        if len(course_names) != len(week_day):
            Logging.Log("Check_config").main("ERROR", 'config.toml文件中Plan部分Week_day的子列表数量与Course_name不匹配')
            self.bool = False
        if len(course_names) != len(multiple_account):
            Logging.Log("Check_config").main("ERROR", 'config.toml文件中Plan部分Multiple_account的子列表数量与Course_name不匹配')
            self.bool = False

        # 检查Time_period中的每个子列表是否包含2到3个元素，且每个元素是否为字符串
        valid_time_periods = ['1-2', '3-4', '5-6', '7-8', '9-10-11', '12-13']
        for period in time_period:
            if not isinstance(period, list):
                Logging.Log("Check_config").main("ERROR", 'config.toml文件中Time_period中的每个子列表必须为列表类型')
                self.bool = False
                continue
            if period:  # 允许子列表为空
                for item in period:
                    if not isinstance(item, str) or item not in valid_time_periods:
                        Logging.Log("Check_config").main("ERROR", f'config.toml文件中Time_period中的元素必须为字符串类型且值在{valid_time_periods}中')
                        self.bool = False

        # 检查Week_day中的每个子列表是否包含1到7个元素，且每个元素是否为字符串且值在1到7之间
        for day in week_day:
            if not isinstance(day, list):
                Logging.Log("Check_config").main("ERROR", 'config.toml文件中Week_day中的每个子列表必须为列表类型')
                self.bool = False
                continue
            if day:  # 允许子列表为空
                for item in day:
                    if not isinstance(item, str) or not item.isdigit() or int(item) < 1 or int(item) > 7:
                        Logging.Log("Check_config").main("ERROR", 'config.toml文件中Week_day中的每个元素必须为字符串类型且值在1到7之间')
                        self.bool = False

    def check_time_section(self):
        # 检查Start_time和End_time的时间格式是否正确
        time_format = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')
        start_time = self.config['Time'].get('Start_time')
        end_time = self.config['Time'].get('End_time')

        if not time_format.match(start_time):
            Logging.Log("Check_config").main("ERROR", 'config.toml文件中Start_time格式不正确，应为HH:MM')
            self.bool = False
        if not time_format.match(end_time):
            Logging.Log("Check_config").main("ERROR", 'config.toml文件中End_time格式不正确，应为HH:MM')
            self.bool = False
    def Return_bool(self):
        self.check_config()
        if self.bool:
            Logging.Log("Check_config").main("INFO", 'config.toml配置文件正确')
        else:
            Logging.Log("Check_config").main("ERROR", 'config.toml配置文件错误')
        # 返回配置文件是否正确
        return self.bool

if __name__ == '__main__':
    main().check_config()