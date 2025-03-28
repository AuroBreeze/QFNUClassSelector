from flask import Blueprint, render_template, Response
from .Check_main import main
from datetime import datetime
import time

check_config_bp = Blueprint('check_config', __name__, template_folder='../../templates')

@check_config_bp.route('/')
def check_config():
    return render_template("check_config.html")

@check_config_bp.route('/run')
def run_check_config():
    def generate():
        try:
            # 获取当前日期并构造日志文件路径
            today = datetime.now().strftime('%Y-%m-%d')
            log_file_path = f"./log/{today}_app.log"
            
            # 清空日志文件
            open(log_file_path, 'w').close()

            # 运行检查配置
            check_instance = main()
            
            # 读取日志文件内容并逐条输出
            with open(log_file_path, 'r',encoding="utf-8") as log_file:
                print(log_file)
                for line in log_file:
                    yield f"data: {line.strip()}\n\n"
                    time.sleep(0.05)  # 适当的延迟以保证前端显示流畅
            yield "data: 配置文件检查完成\n\n"
        except Exception as e:
            pass
            #yield f"data: 检查过程中出现错误: {str(e)}\n\n"  # 将错误信息传递给前端
            #yield "event: close\n\n"  # 仅在发生错误时触发关闭事件
    return Response(generate(), mimetype='text/event-stream')