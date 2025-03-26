from Module import Logging,Welcome,Session_inherit,Select_class,Timer
import time

class QFNUClassSelector:
    def __init__(self):
        self.log = Logging.Log()
    def run(self):
        time_start = time.time()

        Welcome.main()
        # Check_toml.main().Return_bool()
        self.log.main("INFO", "QFNUClassSelector started")

        # if Timer.Timer().run() == False:
        #     self.log.main("INFO", "程序正在退出")
        #     time_end = time.time()
        #     self.log.main("INFO", f"程序运行耗时: {time_end - time_start}s")
        #     return
        # index = 0
        # session  = Session_inherit.Session_Inherit(index).Return_Session()
        session = None

        Select_class.Select_Class(session).run()

        time_end = time.time()
        self.log.main("INFO", f"Time used: {time_end - time_start}s")
    def MultiAccount(self):
        pass

if __name__ == '__main__':
    QFNUClassSelector().run()
