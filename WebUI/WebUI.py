from flask import Flask, render_template, request, redirect, url_for
import toml
import os

app = Flask(__name__)

# 获取当前配置文件的路径
CONFIG_PATH = os.path.join(os.path.dirname(__file__), './config.toml')

@app.route('/')
def index():
    # 读取当前的 config.toml 文件
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:  # 添加编码参数
        config = toml.load(f)
    return render_template('index.html', config=config)

@app.route('/update', methods=['POST'])
def update():
    try:
        # 处理基础表单数据
        username = [u.strip() for u in request.form.getlist('username[]') if u.strip()]
        password = [p.strip() for p in request.form.getlist('password[]') if p.strip()]
        mode_number = request.form.get('mode_number', 'single')  # 必须最先获取模式参数
        
        # 立即验证模式与账号数量关系
        if mode_number == 'single' and len(username) > 1:
            return redirect(url_for('index'))

        # 读取当前配置（必须在表单处理之后）
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = toml.load(f)
            
        # 更新核心配置项（必须最先更新模式）
        config['Mode']['Number'] = mode_number
        config['Login']['username'] = username
        config['Login']['password'] = password
        
        # 以下处理其他配置项（保持原有逻辑）
        course_name = []
        teachers_name = []
        time_period = []
        week_day = []
        course_order = []
        # 修正课程配置处理逻辑
        course_count = 0
        while True:
            course_count += 1
            name_key = f'course_name_{course_count}'
            if not request.form.get(name_key):
                course_count -= 1
                break
            course_name.append(request.form.get(name_key))
            
            # Add null checks for all form fields
            teachers = request.form.get(f'teachers_{course_count}', '')  # Note: field name changed
            time_period_val = request.form.get(f'time_period_{course_count}', '')
            week_day_val = request.form.get(f'week_day_{course_count}', '')
            course_order_val = request.form.get(f'course_order_{course_count}', '')
        
            teachers_name.append(teachers.split(',') if teachers else [])
            time_period.append(time_period_val.split(',') if time_period_val else [])
            week_day.append(week_day_val.split(',') if week_day_val else [])
            course_order.append(course_order_val.split(',') if course_order_val else [])
    
        # 处理 multiple_judge 的空值
        multiple_judge_input = request.form.get('multiple_judge', '')
        multiple_judge = [m.strip() == 'true' for m in multiple_judge_input.split(',')] if multiple_judge_input else []
        multiple = request.form.get('multiple') == 'true'
        # Before
        # multiple_judge = [m == 'true' for m in request.form.get('multiple_judge').split(',')]
        
        # After: Add null check and default value
        multiple_judge_input = request.form.get('multiple_judge', '')
        multiple_judge = [m == 'true' for m in multiple_judge_input.split(',')] if multiple_judge_input else []
        # 修复 multiple_account 处理逻辑
        raw_accounts = request.form.get('multiple_account', '')
        multiple_account = []
        if raw_accounts.strip():
            # 分割课程账号组，并过滤空值
            course_groups = [g.strip() for g in raw_accounts.split(';') if g.strip()]
            for group in course_groups:
                # 分割单个课程内的账号，过滤空值
                accounts = [a.strip() for a in group.split(',') if a.strip()]
                multiple_account.append(accounts)
        # 在update路由中添加以下处理逻辑
        config['Plan']['sfym'] = 'sfym' in request.form
        config['Plan']['sfct'] = 'sfct' in request.form
        config['Plan']['sfxx'] = 'sfxx' in request.form
        config['Plan']['skxq_xx0103'] = request.form.get('skxq_xx0103', '1')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        interval = request.form.get('interval')
        retry_time = request.form.get('retry_time')
    
        # 读取当前的 config.toml 文件
        with open(CONFIG_PATH, 'r',encoding="utf-8") as f:
            config = toml.load(f)
    
        # 更新配置
        # 更新配置时添加模式参数
        config['Mode']['Number'] = mode_number  # 确保更新模式参数
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
        # Handle time parameters with validation
        def safe_int(value, default=0):
            try:
                return int(value)
            except (TypeError, ValueError):
                return default
    
        interval = request.form.get('interval', '60')
        retry_time = request.form.get('retry_time', '500')
        
        config['Time'] = {
            'Start_time': request.form.get('start_time', '09:00:00'),
            'End_time': request.form.get('end_time', '23:59:59'),
            'retry_time': safe_int(retry_time, 500),
            'Interval': safe_int(interval, 60)
        }
    
        config['Time']['Interval'] = int(interval)
        config['Time']['retry_time'] = int(retry_time)
    
        # 写入更新后的配置到 config.toml 文件
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            toml.dump(config, f)
    
        return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f'Update error: {str(e)}')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)