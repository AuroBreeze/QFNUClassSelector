from flask import Flask, render_template
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

# 移除原有update路由和配置相关函数
if __name__ == '__main__':
    app.run(debug=True)