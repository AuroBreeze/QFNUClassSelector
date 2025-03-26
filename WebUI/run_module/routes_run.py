from flask import Blueprint, Response
from ..Essence.main import QFNUClassSelector
import time

run_bp = Blueprint('run', __name__, template_folder='../../templates')

@run_bp.route('/')
def run_interface():
    return render_template("run.html")

@run_bp.route('/stream')
def run_stream():
    def generate():
        try:
            # 初始化主程序
            runner = QFNUClassSelector()
            
            # 清空日志文件
            log_path = "../log/runtime.log"
            open(log_path, 'w').close()

            # 启动运行线程
            import threading
            thread = threading.Thread(target=runner.run)
            thread.start()

            # 实时读取日志
            with open(log_path, 'r', encoding='utf-8') as f:
                while thread.is_alive():
                    line = f.readline()
                    if line:
                        yield f"data: {line.strip()}\n\n"
                        time.sleep(0.05)
                    else:
                        time.sleep(0.1)

            yield "data: 运行已完成\n\n"
        except Exception as e:
            yield f"data: 运行错误: {str(e)}\n\n"
        finally:
            yield "event: close\n\n"

    return Response(generate(), mimetype='text/event-stream')