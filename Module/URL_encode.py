import urllib.parse #实现URL编码
from Module import Logging

class Encode:
    def __init__(self, text):
        self.log = Logging.Log("URL")
        "%E4%B9%92%E4%B9%93%E7%90%83"
        try:
            if text == "":
                self.log.main("WARN", "URL_encode.py 没有输入需要编码的文本,请重新输入")
            # 需要编码的字符串
            self.text = f"{text}"
            # URL 编码
            self.encoded_text = urllib.parse.quote(self.text)
            # print(self.encoded_text)
        except:
            self.log.main("ERROR", "URL编码出现问题")
    def Get_encode(self):
        return self.encoded_text


