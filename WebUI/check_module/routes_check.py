from flask import Blueprint, render_template, Response
from .Check_main import main
from datetime import datetime

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
            log_file_path = f"/home/code/QFNUClassSelector/log/{today}_app.log"
            
            # 清空日志文件
            open(log_file_path, 'w').close()
            
            # 运行检查配置
            check_instance = main()
            
            # 读取日志文件内容并逐条输出
            with open(log_file_path, 'r') as log_file:
                for line in log_file:
                    yield f"data: {line.strip()}\n\n"
                    import time
                    time.sleep(0.1)  # 适当的延迟以保证前端显示流畅
            yield "data: 配置文件检查完成\n\n"
        except Exception as e:
            yield f"data: 检查过程中出现错误: {str(e)}\n\n"
        finally:
            yield "event: close\n\n"  # 添加关闭事件以确保前端知道流已结束
    return Response(generate(), mimetype='text/event-stream')