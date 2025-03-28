from flask import Blueprint, Response, render_template, jsonify
from .run_main import QFNUClassSelector
import time
from datetime import datetime
import os
from .check_failed_courses import check_failed_courses

run_bp = Blueprint('run', __name__, template_folder='../../templates')

@run_bp.route('/')
def run_interface():
    return render_template("run.html")

@run_bp.route('/start')
def run_stream():
    def generate():
        try:
            # 初始化主程序
            runner = QFNUClassSelector()
            
            # 获取当前日期并构造日志文件路径
            today = datetime.now().strftime('%Y-%m-%d')
            log_path = f"./log/{today}_app.log"
            
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

@run_bp.route('/failed_courses')
def get_failed_courses():
    data = check_failed_courses()
    return jsonify(data)