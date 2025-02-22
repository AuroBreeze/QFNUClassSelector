import requests
from PIL import Image
from io import BytesIO
import ddddocr
import os
import toml
from Module import Logging

# 设置基本的URL和数据

# 验证码请求URL
RandCodeUrl = "http://zhjw.qfnu.edu.cn/verifycode.servlet"
# 登录请求URL
loginUrl = "http://zhjw.qfnu.edu.cn/Logon.do?method=logonLdap"
# 初始数据请求URL
dataStrUrl = "http://zhjw.qfnu.edu.cn/Logon.do?method=logon&flag=sess"

log = Logging.Log("Login")
def get_ocr_res(cap_pic_bytes):  # 识别验证码
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.classification(cap_pic_bytes)
    return res

def get_initial_session():
    """
    创建会话并获取初始数据
    返回: (session对象, cookies字典, 初始数据字符串)
    """
    session = requests.session()
    response = session.get(dataStrUrl, timeout=1000)
    cookies = session.cookies.get_dict()
    return session, cookies, response.text


def handle_captcha(session, cookies):
    """
    获取并识别验证码
    返回: 识别出的验证码字符串
    """
    response = session.get(RandCodeUrl, cookies=cookies)

    # 添加调试信息
    if response.status_code != 200:
        #print(f"请求验证码失败，状态码: {response.status_code}")
        log.main("ERROR","请求验证码失败，状态码: {response.status_code}")
        return None

    try:
        image = Image.open(BytesIO(response.content))
    except Exception as e:
        #print(f"无法识别图像文件: {e}")
        log.main("ERROR","无法识别图像文件: {e}")
        return None

    return get_ocr_res(image)


def generate_encoded_string(data_str, user_account, user_password):
    """
    生成登录所需的encoded字符串
    参数:
        data_str: 初始数据字符串
        user_account: 用户账号
        user_password: 用户密码
    返回: encoded字符串
    """
    res = data_str.split("#")
    code, sxh = res[0], res[1]
    data = f"{user_account}%%%{user_password}"
    encoded = ""
    b = 0

    for a in range(len(code)):
        if a < 20:
            encoded += data[a]
            for _ in range(int(sxh[a])):
                encoded += code[b]
                b += 1
        else:
            encoded += data[a:]
            break
    return encoded


def login(session, cookies, user_account, user_password, random_code, encoded):
    """
    执行登录操作
    返回: 登录响应结果
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Origin": "http://zhjw.qfnu.edu.cn",
        "Referer": "http://zhjw.qfnu.edu.cn/",
        "Upgrade-Insecure-Requests": "1",
    }

    data = {
        "userAccount": user_account,
        "userPassword": user_password,
        "RANDOMCODE": random_code,
        "encoded": encoded,
    }

    return session.post(
        loginUrl, headers=headers, data=data, cookies=cookies, timeout=1000
    )

def simulate_login(user_account, user_password):
    """
    模拟登录过程
    返回: (session对象, cookies字典)
    抛出:
        Exception: 当验证码错误时
    """
    session, cookies, data_str = get_initial_session()

    for attempt in range(3):  # 尝试三次
        random_code = handle_captcha(session, cookies)
        #print(f"验证码: {random_code}\n")
        encoded = generate_encoded_string(data_str, user_account, user_password)
        response = login(
            session, cookies, user_account, user_password, random_code, encoded
        )

        # 检查响应状态码和内容
        if response.status_code == 200:
            if "验证码错误!!" in response.text:
                #print(f"验证码识别错误，重试第 {attempt + 1} 次\n")
                log.main("ERROR",f"验证码识别错误，重试第 {attempt + 1} 次\n")
                continue  # 继续尝试
            if "密码错误" in response.text:
                #raise Exception("用户名或密码错误")
                log.main("ERROR","用户名或密码错误")
            #print("登录成功，cookies已返回\n")
            log.main("INFO","登录成功，cookies已返回\n")
            return session
        else:
            raise Exception("登录失败")

    #raise Exception("验证码识别错误，请重试")
    log.main("ERROR","验证码识别错误，请重试")


def mainss(index):
    """
    主函数，协调整个程序的执行流程
    """
    with open("./config.toml", "r", encoding="utf-8"):
        config = toml.load("./config.toml")
    user_account = config["Server"]["username"][index]
    user_password = config["Server"]["password"][index]

    #print(f"正在登录账号: {user_account}...")

    # 模拟登录并获取会话

    session = simulate_login(user_account, user_password)
    #print(session)
    log.main("INFO",session)
    return session

if __name__ == "__main__":
    mainss(0)
