# import os
# import sys
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from Module import Check_toml,Welcome,Logging,Params_constructor
from Module import Check_toml,Welcome,Logging,Params_constructor
import time
class main:
    def __init__(self):
        time_1 = time.time()
        self.log = Logging.Log("Check_Main")
        Welcome.main()
        #time.sleep(0.1)
        judge = Check_toml.main().Return_bool()
        #print(judge)
        if judge:
            self.log.main("INFO", "配置文件检查通过")
            Params_constructor.ParamsConstructor().write_to_json()
            time_2 = time.time()
            self.log.main("INFO", "检查用时："+str(time_2-time_1)+"秒")
        else:
            time_2 = time.time()
            self.log.main("ERROR", "config.toml配置文件检查未通过")
            self.log.main("INFO", "用时："+str(time_2-time_1)+"秒")

if __name__ == '__main__':
    main()
