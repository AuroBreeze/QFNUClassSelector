from Module import Logging

class Welcome:
    def __init__(self):
        self.log = Logging.Log()
        self.log.main("INFO", "欢迎使用选课小助手")
        self.log.main("INFO", "PowerBy: AuroBreeze W1ndys")
        self.log.main("INFO", "Lisence： GPL-V3")
        self.log.main("INFO", "Version： 1.0.0")
        self.log.main("INFO", "项目地址：https://github.com/AuroBreeze/QFNUClassSelector")
        self.log.main("INFO", "免责声明")
        self.log.main("INFO", "1. 本脚本仅供学习和研究目的，用于了解网络编程和自动化技术的实现原理。")
        self.log.main("INFO", "2. 使用本脚本可能违反学校相关规定。使用者应自行承担因使用本脚本而产生的一切后果，包括但不限于：(1):账号被封禁 (2):选课资格被取消 (3):受到学校纪律处分 (4):其他可能产生的不良影响")
        self.log.main("INFO", "3. 严禁将本脚本用于：(1):干扰教务系统正常运行 (2):影响其他同学正常选课 (3):其他任何非法或不当用途")
        self.log.main("INFO", "4. 使用本脚本表示使用者已经充分了解并同意以上声明。")
        self.log.main("INFO", "5. 开发者对使用本脚本造成的任何直接或间接损失不承担任何责任。")

if __name__ == '__main__':
    Welcome()