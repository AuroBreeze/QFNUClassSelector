from io import BytesIO
import requests
from PIL import Image
import base64
import ddddocr
from Module import Logging
import toml


class Login:
    def __init__(self):
        self.session = requests.Session()

        self.log = Logging.Log("Login")
        self.url_pic = "http://zhjw.qfnu.edu.cn/jsxsd/verifycode.servlet"
        self.Main_url = "http://zhjw.qfnu.edu.cn/jsxsd/framework/xsMain.jsp"
        self.login_url = "http://zhjw.qfnu.edu.cn/jsxsd/xk/LoginToXkLdap"
    def Get_pic(self):
        pic = self.session.get(self.url_pic).content
        image = Image.open(BytesIO(pic))
        return image

    def Get_code(self,image):
        code = ddddocr.DdddOcr(show_ad=False).classification(image)
        return code

    def Base_user(self):
        with open("../config.toml","r",encoding="utf-8") as f:
            config = toml.load(f)

        user_account = config["Login"]["username"][0]
        user_password = config["Login"]["password"][0]
        print(user_account)

        base_user = str(base64.b64encode(user_account.encode("utf-8")), "utf-8") + "%%%" + str(base64.b64encode(user_password.encode("utf-8")), "utf-8")

        return base_user

    def Main(self):
        self.session.get(self.Main_url)
        code = self.Get_code(self.Get_pic())
        base_user = self.Base_user()
        data = {
            "userAccount": "",
            "userPassword": "",
            "RANDOMCODE": code,
            "encoded": base_user
        }
        res = self.session.post(self.login_url,data=data).text
        #print(self.session.cookies.get_dict())
        #print(res)
        return self.session

if __name__ == '__main__':
    login = Login()
    login.Main()



