from Module import Logging,Welcome,Session_inherit,Select_class,Params_constructor
from Module.ConfigService import ConfigService
import time
import asyncio


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

        # 多账号分支
        mode_number = ConfigService().get_mode().get("Number", "single")
        if str(mode_number).lower() == "multiple":
            self.MultiAccount()
            time_end = time.time()
            self.log.main("INFO", f"程序运行耗时: {time_end - time_start}s")
            return

        # 单账号分支
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

        async def _run_async_flow():
            try:
                await Select_class.Select_Class(session).run()
            except Exception as e:
                self.log.main("ERROR", f"选课流程异常：{e}")
                # 不再抛出，保证统计耗时与退出
                return

        # 运行异步流程
        asyncio.run(_run_async_flow())

        time_end = time.time()
        self.log.main("INFO", f"程序运行耗时: {time_end - time_start}s")
        
    def MultiAccount(self):
        # 运行多账号异步流程
        asyncio.run(self._multi_account_async())
    async def _multi_account_async(self):
        # 生成 params.json 一次（所有账号共用）
        params_path = ConfigService().get_value("Paths", "params", "./params.json")
        Params_constructor.ParamsConstructor().write_to_json(file_path=params_path)

        login_cfg = ConfigService().get_login()
        usernames = login_cfg.get("username", []) or []
        if not usernames:
            self.log.main("ERROR", "多账号模式下未配置任何用户名 [Login].username")
            return

        # 读取计划配置
        plan = ConfigService().get_plan()
        course_names = plan.get("Course_name", []) or []
        multiple_judge_list = plan.get("Multiple_Judge", []) or []
        multiple_accounts_cfg = plan.get("Multiple_account", []) or []

        # 规范化长度
        if len(multiple_judge_list) < len(course_names):
            multiple_judge_list = multiple_judge_list + [False] * (len(course_names) - len(multiple_judge_list))
        if len(multiple_accounts_cfg) < len(course_names):
            multiple_accounts_cfg = multiple_accounts_cfg + [[] for _ in range(len(course_names) - len(multiple_accounts_cfg))]

        # 账号名->索引 映射
        name_to_index = {u: i for i, u in enumerate(usernames)}

        # 构造每个账号的课程白名单
        per_account_courses = {i: set() for i in range(len(usernames))}
        for i, cname in enumerate(course_names):
            specified_accounts = multiple_accounts_cfg[i] if i < len(multiple_accounts_cfg) else []
            if not specified_accounts:
                # 为空 => 所有账号都参与该课程
                for acc_idx in per_account_courses.keys():
                    per_account_courses[acc_idx].add(cname)
            else:
                for acc_name in specified_accounts:
                    if acc_name in name_to_index:
                        per_account_courses[name_to_index[acc_name]].add(cname)
                    else:
                        self.log.main("WARN", f"在 Multiple_account 中配置了未知账号名：{acc_name}")

        # 多选标志映射：课程 -> 是否允许多账号同时抢
        multiple_judge_map = {}
        for i, cname in enumerate(course_names):
            allow_multi = False
            if i < len(multiple_judge_list):
                allow_multi = bool(multiple_judge_list[i])
            multiple_judge_map[cname] = allow_multi

        # 共享完成集合（当某课程 multiple_judge_map[c]==False，被任一账号抢到后，其他账号应跳过）
        shared_completed = set()
        
        # 记录每个账号的选课状态 {account_index: set(已选课程)}
        account_progress = {}
        # 记录每个账号的会话
        account_sessions = {}
        
        # 初始化所有账号的选课状态
        for idx in range(len(usernames)):
            if per_account_courses[idx]:  # 只处理有分配课程的账号
                account_progress[idx] = set()
                try:
                    session = Session_inherit.Session_Inherit(idx).Return_Session()
                    account_sessions[idx] = session
                except Exception as e:
                    self.log.main("ERROR", f"账号 {usernames[idx]} 登录失败: {e}")
        
        if not account_sessions:
            self.log.main("ERROR", "没有有效的账号可以执行选课")
            return
            
        # 持续选课，直到所有账号都选完所有课程或达到最大重试次数
        max_retries = 3  # 最大重试次数
        retry_count = 0
        
        while retry_count < max_retries:
            tasks = []
            has_unfinished = False
            
            for idx, session in account_sessions.items():
                # 获取该账号未完成的课程
                remaining_courses = per_account_courses[idx] - account_progress.get(idx, set())
                if not remaining_courses:
                    continue
                    
                has_unfinished = True
                self.log.main("INFO", f"账号 {usernames[idx]} 开始选课，剩余课程: {', '.join(remaining_courses)}")
                
                # 创建选课任务
                task = asyncio.create_task(
                    Select_class.Select_Class(
                        session,
                        allowed_courses=remaining_courses,
                        shared_completed=shared_completed,
                        multiple_judge_map=multiple_judge_map
                    ).run()
                )
                tasks.append((idx, task))
            
            if not has_unfinished:
                self.log.main("SUCCESS", "所有账号已完成选课")
                break
                
            # 等待本轮所有任务完成
            results = {}
            for idx, task in tasks:
                try:
                    result = await task
                    results[idx] = result
                except Exception as e:
                    self.log.main("ERROR", f"账号 {usernames[idx]} 选课出错: {e}")
            
            # 更新选课进度
            for idx, result in results.items():
                if result:  # 如果返回了已选课程列表
                    if isinstance(result, list):
                        account_progress[idx].update(result)
                    elif isinstance(result, set):
                        account_progress[idx].update(result)
            
            retry_count += 1
            if retry_count < max_retries and has_unfinished:
                self.log.main("INFO", f"第 {retry_count} 轮选课完成，开始下一轮...")
                await asyncio.sleep(5)  # 等待5秒后重试
        
        # 检查最终选课结果
        all_success = True
        for idx in account_sessions.keys():
            if per_account_courses[idx] - account_progress.get(idx, set()):
                failed = per_account_courses[idx] - account_progress.get(idx, set())
                self.log.main("ERROR", f"账号 {usernames[idx]} 未完成选课: {', '.join(failed)}")
                all_success = False
            
        if all_success:
            self.log.main("SUCCESS", "所有账号选课全部完成！")
        else:
            self.log.main("WARN", "部分账号选课未完成，请检查日志并重试")
            await asyncio.gather(*tasks, return_exceptions=True)

    def MultiAccount(self):
        asyncio.run(self._multi_account_async())

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
