from flask import Flask, render_template, Response
from config_module.routes_config import config_bp

app = Flask(__name__)
app.register_blueprint(config_bp, url_prefix='/config')

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/guide')
def guide():
    return render_template('./guide.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('./disclaimer.html')

# 新增检查配置文件路由
@app.route('/check_config')
def check_config():
    return render_template('./check_config.html')

# 新增运行检查配置文件的路由
@app.route('/check_config/run')
def run_check_config():
    from Check_main import main
    def generate():
        try:
            check_instance = main()  # 实例化main类
            if hasattr(check_instance, 'log'):  # 检查实例是否有log属性
                log_messages = check_instance.log.get_messages()  # 获取日志信息
                for message in log_messages:
                    yield f"data: {message}\n\n"
                    import time
                    time.sleep(0.5)  # 缩短延迟时间以加快实时显示
            else:
                yield "data: 无法获取日志信息\n\n"
            yield "data: 配置文件检查完成\n\n"
        except Exception as e:
            yield f"data: 检查过程中出现错误: {str(e)}\n\n"
        finally:
            yield "event: close\n\n"  # 添加关闭事件以确保前端知道流已结束
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)