from io import BytesIO
import requests
from PIL import Image
import base64
import ddddocr
from Module import Logging
from Module.ConfigService import ConfigService
from Module.NetUtils import NetUtils


class Login:
    def __init__(self):
        self.session = requests.Session()

        self.log = Logging.Log("Login")
        self.url_pic = "http://zhjw.qfnu.edu.cn/jsxsd/verifycode.servlet"
        self.Main_url = "http://zhjw.qfnu.edu.cn/jsxsd/framework/xsMain.jsp"
        self.login_url = "http://zhjw.qfnu.edu.cn/jsxsd/xk/LoginToXkLdap"
        self.net = NetUtils()
        self.timeout = ConfigService().get_value("Time", "request_timeout_sec", 10)
    def Get_pic(self):
        resp, err = self.net.request_with_retry(self.session, "GET", self.url_pic, timeout=self.timeout)
        if err is not None and err not in ("ok",):
            self.log.main("ERROR", f"获取验证码失败: {err}")
            raise RuntimeError("fetch captcha failed")
        pic = resp.content if resp is not None else b""
        image = Image.open(BytesIO(pic))
        return image

    def Get_code(self,image):
        code = ddddocr.DdddOcr(show_ad=False).classification(image)
        return code

    def Base_user(self):
        login_cfg = ConfigService().get_login()
        user_account = login_cfg.get("username", [""])[0]
        user_password = login_cfg.get("password", [""])[0]
        if not user_account or not user_password:
            self.log.main("ERROR", "账号或密码为空，请检查config.toml")
            raise ValueError("empty credentials")

        base_user = str(base64.b64encode(user_account.encode("utf-8")), "utf-8") + "%%%" + str(base64.b64encode(user_password.encode("utf-8")), "utf-8")

        return base_user

    def Main(self):
        # 访问主页，准备登录
        _, err = self.net.request_with_retry(self.session, "GET", self.Main_url, timeout=self.timeout)
        if err is not None and err not in ("ok",):
            self.log.main("ERROR", f"访问主页失败: {err}")
            raise RuntimeError("visit main failed")
        code = self.Get_code(self.Get_pic())
        base_user = self.Base_user()
        data = {
            "userAccount": "",
            "userPassword": "",
            "RANDOMCODE": code,
            "encoded": base_user
        }
        resp, err = self.net.request_with_retry(self.session, "POST", self.login_url, data=data, timeout=self.timeout)
        if err is not None and err not in ("ok",):
            self.log.main("ERROR", f"登录请求失败: {err}")
            raise RuntimeError("login request failed")
        res_text = resp.text if resp is not None else ""
        self.log.main("INFO", "登录请求已发送")

        # 基于返回内容做初步错误判断
        known_errors = [
            "验证码错误", "用户名或密码错误", "登陆失败", "登录失败", "错误"
        ]
        if any(err in res_text for err in known_errors):
            self.log.main("ERROR", f"登录失败：{','.join([e for e in known_errors if e in res_text])}")
            raise ValueError("login failed: known error in response")

        # 验证是否可访问受保护页面，判断是否真正登录成功
        try:
            probe_url = "http://zhjw.qfnu.edu.cn/jsxsd/xsxk/xklc_list"
            probe_res, err2 = self.net.request_with_retry(self.session, "GET", probe_url, timeout=self.timeout)
            if err2 is not None and err2 not in ("ok",):
                self.log.main("ERROR", f"登录后探测失败: {err2}")
                raise ValueError("login failed: probe failed")
            probe_txt = probe_res.text if probe_res is not None else ""
            if probe_res.status_code != 200:
                self.log.main("ERROR", f"登录后探测失败，状态码: {probe_res.status_code}")
                raise ValueError("login failed: bad status code")
            # 若仍出现登录表单关键字段，视为未登录
            login_markers = ["userAccount", "LoginToXkLdap", "verifycode.servlet", "登录"]
            if any(m in probe_txt for m in login_markers):
                self.log.main("ERROR", "登录未生效，仍看到登录页特征")
                raise ValueError("login failed: still on login page")
        except Exception:
            # 往外抛出，让调用方感知错误
            raise

        self.log.main("INFO", "登录成功")
        return self.session

if __name__ == '__main__':
    login = Login()
    login.Main()



