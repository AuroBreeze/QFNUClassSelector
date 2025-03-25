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
            for line in main():
                yield f"data: {line}\n\n"
                import time
                time.sleep(1)  # 添加延迟以确保实时显示
            yield "data: 配置文件检查通过\n\n"
        except Exception as e:
            yield f"data: 检查过程中出现错误: {str(e)}\n\n"
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)