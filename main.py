from Module import Logging,Welcome,Session_inherit,Select_class,Check_toml,Timer
import time

class QFNUClassSelector:
    def __init__(self):
        self.log = Logging.Log()
        pass

    def run(self):
        time_start = time.time()

        Welcome.main()
        bool_config = Check_toml.main().Return_bool()
        if bool_config == False:
            return
        self.log.main("INFO", "QFNUClassSelector started")

        if Timer.Timer().run() == False:
            self.log.main("INFO", "Time is up, exiting...")
            time_end = time.time()
            self.log.main("INFO", f"Time used: {time_end - time_start}s")
            return
        #session = login.mainss(0)
        index = 0
        session  = Session_inherit.Session_Inherit(index).Return_Session()


        #Select_class.Select_Class(session,Data.Fixed_Data,kcxx=f"{URL_encode.Encode("乒乓球")}")

        #Submit_class.Submit_ClassSelection(session,jx0404id="202420252011613",kcid="530128")

        time_end = time.time()
        self.log.main("INFO", f"Time used: {time_end - time_start}s")
    def MultiAccount(self):
        pass

if __name__ == '__main__':

    QFNUClassSelector().run()

    #print("Time used:", time_end - time_start)

