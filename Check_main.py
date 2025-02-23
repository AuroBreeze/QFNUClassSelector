from Module import Check_toml,Welcome,Logging,Params_constructor

class main:
    def __init__(self):
        self.log = Logging.Log("Check_Main")
        Welcome.main()
        judge = Check_toml.main().Return_bool()
        if judge:
            self.log.main("INFO", "配置文件检查通过")
            Params_constructor.ParamsConstructor().write_to_json()
        else:
            self.log.main("ERROR", "配置文件检查未通过")
            self.log.main("ERROR", "按任意键退出...")
            input()
            exit()
if __name__ == '__main__':
    main()
