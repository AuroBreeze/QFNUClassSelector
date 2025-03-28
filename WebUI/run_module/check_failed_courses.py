import json
import time
import os

def check_failed_courses():
    max_attempts = 50  # 最大尝试次数
    attempt_interval = 3  # 每次尝试的间隔时间（秒）

    for attempt in range(max_attempts):
        if os.path.exists('failed_courses.json'):
            try:
                with open('failed_courses.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            except Exception as e:
                return {"error": str(e)}
        else:
            time.sleep(attempt_interval)

    return {}  # 如果文件未生成，返回空的JSON对象