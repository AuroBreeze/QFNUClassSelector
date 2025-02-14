import urllib.parse


class URL_encode:
    def __init__(self, text="乒乓球"):
        "%E4%B9%92%E4%B9%93%E7%90%83"
        # 需要编码的字符串
        self.text = f"{text}"
        # URL 编码
        self.encoded_text = urllib.parse.quote(self.text)
        #print(self.encoded_text)

    def Get_encode(self):
        return self.encoded_text

data = URL_encode()
ee =data
print(type(ee))
