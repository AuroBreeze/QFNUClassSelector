from flask import Flask, render_template, Response
from config_module.routes_config import config_bp
from check_module.routes_check import check_config_bp

app = Flask(__name__)
app.register_blueprint(config_bp, url_prefix='/config')
# 修正蓝图的 URL 前缀，确保与访问路径一致
app.register_blueprint(check_config_bp, url_prefix='/check_config')

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/guide')
def guide():
    return render_template('./guide.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('./disclaimer.html')

if __name__ == '__main__':
    app.run(debug=True)