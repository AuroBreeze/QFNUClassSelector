from Module import Logging,Welcome,Session_inherit,Select_class,Params_constructor
from Module.ConfigService import ConfigService
import time


class QFNUClassSelector:
    def __init__(self):
        self.log = Logging.Log()
        pass
    def run(self):
        time_start = time.time()
        Welcome.main()
        self.log.main("INFO", "QFNUClassSelector started")

        if not self._should_start_now():
            self.log.main("INFO", "程序正在退出")
            time_end = time.time()
            self.log.main("INFO", f"程序运行耗时: {time_end - time_start}s")
            return

        index = 0
        try:
            session  = Session_inherit.Session_Inherit(index).Return_Session()
        except Exception as e:
            self.log.main("ERROR", f"登录失败：{e}")
            self.log.main("INFO", "请检查 config.toml 中的 [Login] 用户名/密码，并确认验证码识别正常")
            return
        # 生成 params.json 到配置的路径（默认 ./params.json）
        params_path = ConfigService().get_value("Paths", "params", "./params.json")
        Params_constructor.ParamsConstructor().write_to_json(file_path=params_path)
        
        
        try:
            Select_class.Select_Class(session).run()
        except Exception as e:
            self.log.main("ERROR", f"选课流程异常：{e}")
            return

        time_end = time.time()
        self.log.main("INFO", f"程序运行耗时: {time_end - time_start}s")
    def MultiAccount(self):
        pass

    def _should_start_now(self) -> bool:
        """根据配置决定是否启用时间窗口控制。启用则惰性导入 Timer 调用 run()。未启用则直接开始。
        config: [Time]
          enable_window = true  # 关闭则跳过计时器
        """
        try:
            time_cfg = ConfigService().get_time()
        except Exception:
            # 配置读取失败时，默认直接开始，避免阻塞
            return True

        enable = time_cfg.get("enable_window", True)
        if not enable:
            self.log.main("INFO", "已禁用时间窗口控制，立即开始")
            return True

        # 惰性导入，避免对 Timer 的强耦合
        from Module import Timer as _TimerModule
        return bool(_TimerModule.Timer().run())

if __name__ == '__main__':
    QFNUClassSelector().run()
