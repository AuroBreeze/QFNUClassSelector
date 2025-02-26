from flask import Flask, render_template, request, redirect, url_for
import toml
import os

app = Flask(__name__)

# 获取当前配置文件的路径
CONFIG_PATH = os.path.join(os.path.dirname(__file__), './config.toml')

@app.route('/')
def index():
    # 读取当前的 config.toml 文件
    with open(CONFIG_PATH, 'r') as f:
        config = toml.load(f)
    return render_template('index.html', config=config)

@app.route('/update', methods=['POST'])
def update():
    # 获取表单数据
    username = request.form.get('username').split(',')
    password = request.form.get('password').split(',')
    course_name = []
    teachers_name = []
    time_period = []
    week_day = []
    course_order = []
    course_count = 0
    while request.form.get(f'course_name_{course_count + 1}'):
        course_count += 1
        course_name.append(request.form.get(f'course_name_{course_count}'))
        teachers_name.append(request.form.get(f'teachers_name_{course_count}').split(','))
        time_period.append(request.form.get(f'time_period_{course_count}').split(','))
        week_day.append(request.form.get(f'week_day_{course_count}').split(','))
        course_order.append(request.form.get(f'course_order_{course_count}').split(','))
    multiple = request.form.get('multiple') == 'true'
    multiple_judge = [m == 'true' for m in request.form.get('multiple_judge').split(',')]
    multiple_account = [a.split(',') for a in request.form.get('multiple_account').split(';')]
    sfym = request.form.get('sfym') == 'true'
    sfct = request.form.get('sfct') == 'true'
    sfxx = request.form.get('sfxx') == 'true'
    skxq_xx0103 = request.form.get('skxq_xx0103')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    interval = request.form.get('interval')
    retry_time = request.form.get('retry_time')

    # 读取当前的 config.toml 文件
    with open(CONFIG_PATH, 'r') as f:
        config = toml.load(f)

    # 更新配置
    config['Login']['username'] = username
    config['Login']['password'] = password
    config['Plan']['Course_name'] = course_name
    config['Plan']['Teachers_name'] = teachers_name
    config['Plan']['Time_period'] = time_period
    config['Plan']['Week_day'] = week_day
    config['Plan']['Course_order'] = course_order
    config['Plan']['Multiple'] = multiple
    config['Plan']['Multiple_Judge'] = multiple_judge
    config['Plan']['Multiple_account'] = multiple_account
    config['Plan']['sfym'] = sfym
    config['Plan']['sfct'] = sfct
    config['Plan']['sfxx'] = sfxx
    config['Plan']['skxq_xx0103'] = skxq_xx0103
    config['Time']['Start_time'] = start_time
    config['Time']['End_time'] = end_time
    config['Time']['Interval'] = int(interval)
    config['Time']['retry_time'] = int(retry_time)

    # 写入更新后的配置到 config.toml 文件
    with open(CONFIG_PATH, 'w') as f:
        toml.dump(config, f)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)