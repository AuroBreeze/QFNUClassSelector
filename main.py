from Module import URL_encode, login,Logging,Welcome,Session_inherit,Select_class,Submit_class,Data,Check_toml

class QFNUClassSelector:
    def __init__(self):
        pass

    def run(self):
        Welcome.main()
        bool_config = Check_toml.main().Return_bool()
        if bool_config == False:
            return
        Logging.Log().main("INFO", "QFNUClassSelector started")

        #session = login.mainss(0)
        index = 0
        session  = Session_inherit.Session_Inherit(index).Return_Session()
        Select_class.Select_Class(session,Data.Fixed_Data,kcxx=f"{URL_encode.Encode("乒乓球")}")
        Submit_class.Submit_ClassSelection(session,jx0404id="202420252011613",kcid="530128")
    def MultiAccount(self):
        pass

if __name__ == '__main__':
    QFNUClassSelector().run()

