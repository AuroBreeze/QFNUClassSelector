from Module import URL_encode, login,Logging,Welcome,Session_inherit,Select_class,Submit_class,Data

class QFNUClassSelector:
    def __init__(self):
        pass

    def run(self):
        Welcome.main()
        #Logging.Log().main("info", "QFNUClassSelector started")
        session = login.mainss()
        session  = Session_inherit.Session_Inherit(session).Return_Session()
        Select_class.Select_Class(session,Data.Fixed_Data,kcxx=f"{URL_encode.Encode("乒乓球")}")
        Submit_class.Submit_ClassSelection(session,jx0404id="202420252011613",kcid="530128")
if __name__ == '__main__':
    QFNUClassSelector().run()

