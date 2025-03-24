import os
import toml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config.toml')

# 初始化默认配置
DEFAULT_CONFIG = {
    "Mode": {
        "Number": "single",
        "Select": ["Start"]
    },
    "Login": {
        "username": [],
        "password": []
    },
    "Plan": {
        "Course_name": [],
        "Teachers_name": [],
        "Time_period": [],
        "Week_day": [],
        "Course_order": [],
        "sfym": False,
        "sfct": False,
        "sfxx": False,
        "skxq_xx0103": "1"
    },
    "Time": {
        "Start_time": "09:00:00",
        "End_time": "23:59:59",
        "retry_time": 500,
        "Interval": 60
    }
}

def ensure_config_exists():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            toml.dump(DEFAULT_CONFIG, f)

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return toml.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        toml.dump(config, f)