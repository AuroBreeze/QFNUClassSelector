# QFNUClassSelector

<div align="center">

[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](https://github.com/AuroBreeze/QFNUClassSelector/releases)
[![Stars](https://img.shields.io/github/stars/AuroBreeze/QFNUClassSelector?style=flat-square)](https://github.com/AuroBreeze/QFNUClassSelector/stargazers)
[![Issues](https://img.shields.io/github/issues/AuroBreeze/QFNUClassSelector?style=flat-square)](https://github.com/AuroBreeze/QFNUClassSelector/issues)
[![Python 3.12.3](https://img.shields.io/badge/Python-3.12.3-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/AuroBreeze/QFNUClassSelector/commits/main)
[![License: GPL](https://img.shields.io/badge/License-GPL-green.svg)](LICENSE)
[![Forks](https://img.shields.io/github/forks/AuroBreeze/QFNUClassSelector?style=flat-square)](https://github.com/AuroBreeze/QFNUClassSelector/network/members)
[![Watchers](https://img.shields.io/github/watchers/AuroBreeze/QFNUClassSelector?style=flat-square)](https://github.com/AuroBreeze/QFNUClassSelector/watchers)
[![Last Commit](https://img.shields.io/github/last-commit/AuroBreeze/QFNUClassSelector?style=flat-square)](https://github.com/AuroBreeze/QFNUClassSelector/commits/main)

</div>

<div align="center">
  <h1>✨ 请给我一个 Star! ⭐</h1>
  <p>如果这个项目对你有帮助，请考虑点个 Star 支持一下！</p>
</div>

## 📖 项目介绍

QFNUClassSelector 是一个专为曲阜师范大学学生设计的智能选课助手，通过自动化脚本帮助学生快速、高效地完成选课。支持多账号管理、智能时间规划、可视化配置界面等功能，让选课变得简单高效。

### ✨ 核心功能

- 🚀 **多账号支持**：支持同时管理多个账号的选课任务
- 🖥️ **可视化配置**：提供直观的Web界面进行配置管理
- ⏰ **智能时间管理**：支持定时抢课和自动重试机制
- 📊 **实时监控**：实时显示选课状态和日志信息
- 🔄 **多模式支持**：支持抢课模式和候选模式
- 🛡️ **稳定可靠**：完善的错误处理和重试机制

## 🚀 最新动态

### 版本 2.0.0 新特性

### ✨ 新增功能

#### 核心功能
- 新增多账号选课模式，支持同时为多个账号配置不同的选课方案
- 实现智能重试机制，提高抢课成功率
- 新增课程冲突检测功能
- 支持课程时间偏好设置
- **新增异步并发选课功能** - 使用 asyncio 和 httpx 实现高性能并发请求
- **增强多账号协调机制** - 优化多账号登录和选课流程同步

### 🔧 优化与修复

#### 性能优化
- 优化配置同步机制，修复多窗口配置不同步问题
- 改进资源加载策略，降低内存占用
- **新增并发控制** - 引入 Semaphore 限制并发数量，提高系统稳定性

#### 功能改进

- 优化课程搜索算法，提高搜索效率
- **重构代码架构** - 新增 ConfigService、DataAccess、NetUtils 等模块，提高可维护性
- **优化异常处理** - 改进选课流程异常处理逻辑，确保程序健壮性

#### 问题修复
- 修复多账号模式下登录状态异常问题
- 修复特定情况下配置保存失败的问题
- 修复课程时间解析错误
- 修复部分浏览器兼容性问题
- **修复未定义变量问题** - 使用 Load_Source() 替代 _da 变量
- **优化失败课程处理** - 增加失败课程列表生成判断逻辑
## 🚀 快速开始

### 环境要求
- Python 3.8+
- Windows/Linux/macOS
- 现代浏览器（推荐 Chrome/Firefox 最新版）

### 🛠️ 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/AuroBreeze/QFNUClassSelector.git
   cd QFNUClassSelector
   ```

2. **创建虚拟环境（推荐）**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

### 🖥️ 使用 WebUI（推荐）

1. **启动服务**
   ```bash
   python WebUI/WebUI.py
   ```

2. **访问界面**
   打开浏览器访问 [http://localhost:5000](http://localhost:5000)

3. **主要功能**
   - 配置管理：`/config/disposition`
   - 配置检查：`/check_config`（支持SSE实时日志）
   - 启动运行：`/run`（实时日志 + 失败课程查询）

### 💻 命令行模式

#### 直接运行
```bash
python Essence/main.py
```

#### 无界面模式
```bash
python WebUI/run_module/run_main.py
```

> 💡 两种模式都会遵循 `config.toml` 中 `[Time]` 部分设置的 `Start_time` 和 `End_time`

### 🔍 参数生成
运行前建议先生成参数文件：

```bash
# 检查配置并生成 params.json
python WebUI/check_module/Check_main.py
```

## ⚙️ 配置说明

### 配置文件结构
项目使用 `config.toml` 进行配置，主要包含以下部分：

```toml
[Login]  # 账号密码配置
username = ["学号1", "学号2"]  # 支持多账号
password = ["密码1", "密码2"]  # 与账号一一对应

[Mode]  # 运行模式
Number = "single"  # single: 单账号模式, multiple: 多账号模式
Select = ["Start", "End"]  # 选课模式

[Plan]  # 选课计划
Course_name = ["课程1", "课程2"]  # 必填：要选的课程
Course_order = [["1", ""], ["2", ""]]  # 选课顺序
Multiple = false  # 是否启用多选

[Time]  # 定时设置
Start_time = "09:00:00"  # 开始时间
End_time = "09:10:00"   # 结束时间
retry_time = 500       # 重试间隔(ms)
Interval = 60          # 检查间隔(s)

[Async]  # 并发设置
max_concurrency = 8    # 最大并发数
```

### 详细配置说明

#### 1. 登录配置
```toml
[Login]
username = ["学号1", "学号2"]  # 支持多账号
password = ["密码1", "密码2"]  # 与账号一一对应
```

#### 2. 选课模式
- `Number`: 单账号(`single`)或多账号(`multiple`)模式
- `Select`: 抢课模式(`Start`)或候补模式(`End`)，可同时启用

#### 3. 课程筛选
- `Teachers_name`: 指定任课教师
- `Time_period`: 上课时间(1-2节, 3-4节等)
- `Week_day`: 上课星期(1-7表示周一到周日)
- `sfym`: 是否过滤已满课程
- `sfct`: 是否过滤冲突课程
- `sfxx`: 是否过滤限选课程

## 📱 使用技巧

### 选课策略
1. **提前准备**：在选课前完成配置并测试
2. **多方案备选**：为每个课程准备多个备选方案
3. **时间规划**：合理安排选课时间，避开高峰期
4. **网络环境**：确保网络稳定，建议使用校园网

### 常见问题
1. **登录失败**
   - 检查账号密码是否正确
   - 确认网络连接正常
   - 验证码识别是否正常

2. **选课不成功**
   - 检查课程代码和名称是否正确
   - 确认选课时间是否已到
   - 查看日志定位具体问题

3. **性能优化**
   - 适当调整并发数
   - 优化选课策略，减少不必要的请求

## ⚠️ 免责声明

> **重要**：使用前请仔细阅读

1. **仅限学习研究**
   - 本工具仅用于学习网络编程和自动化技术
   - 请勿用于实际选课或干扰学校正常教学秩序

2. **使用风险**
   - 可能违反学校相关规定
   - 可能导致账号异常或选课资格被取消
   - 使用者需自行承担一切后果

3. **禁止行为**
   - 商业用途或盈利目的
   - 干扰教务系统正常运行
   - 影响他人正常选课
   - 任何非法或不当用途

4. **使用须知**
   - 下载即表示同意本声明
   - 建议在测试环境中使用
   - 请勿用于实际选课

5. **责任声明**
   - 开发者不承担任何直接或间接责任
   - 使用者需自行承担所有风险

## 配置文件说明
`config.toml`文件的配置项说明：

> [!WARNING]
> 
> 下面这些是必填项，一定要填写
> 
> 注意：如果启用了多账号模式，请确保 `username` 和 `password` 列表长度一致

```
#这是登陆必填项，在双引号中填写账号和密码

[Server] #账号与密码,支持多账号进行抢课
username = [""]#(必填)
password = [""]#(必填)


[Plan]#这个也是必填项，在双引号中填写课程名，可自行增加，但要确保课程名正确，否则不能抢课
Course_name = ["课程1","课程2","课程3"] # 课程名字,可以填多个(必填)

[Time]#设置定时任务
Start_time = "09:00:00" # 定时任务开始时间 (必填)
End_time = "09:10:00" # 定时任务结束时间，结束后自动启用END模式 (必填)
```

> [!NOTE]
> 
> 下面是选填项，可以帮助你，快速选到你想选的课程

```
[Plan]
#注意每个子列表中最后一定要留一个空字符，否则，程序只会寻找你设置的顺序里的
#注意不要填入重复的数字

#选择顺序  我的大一上选课在本学期计划里选的体育   大一下在专业内跨年级选课选的体育
#0：选修选课 1：本学期计划内选课 2：专业内跨年级选课 3：计划外选课 4：公选课选课 5：辅修选课
#默认顺序： 0->1->2->3->4->5
#示例[["2","3",""],["2",""],[""]]

Course_order = [["1",""],[""],[""]] # 课程选择顺序，如果你知道你选择的课程在本学期计划内，或专业内跨年级等，就在子列表中填入顺序，程序会按顺序进行查找课程，或者说你并不确定，那就留一个空字符，程序也会按照默认顺序进行查找课程(非必填)
#推荐填写 Course_order = [["1","2",""],["2","3","4",""],[""]]
#程序会先按你设置的顺序查找课程，如果找不到，就按照默认顺序查找课程
```

```
#填写这些东西的时候，注意事项和上面一样，如果你不确定，就在子列表最后填入""表示不限制,或者只留一个空子列表
# [[],[]] == [[""],[""]]

#Time_period这个要注意，一定要按照格式填写，否则可能会出错
#课程时间(节次-节次)(1-2-,3-4-,5-6-,7-8-,9-10-11,12-13-)，可以填多个,也可填入""表示不限制(非必填)

#填这些东西的时候，一定要先去看学期课表，然后再填，不然可能会出错。
Teachers_name = [["老师1", "老师2",""], ["老师3", "老师4"],[]] # 每个课程对应的老师列表(候选功能)，可以填多个也可以留空，用逗号隔开，也可填入""表示不限制，以免最后没有这个老师导致抢课失败。(非必填)
Time_period = [["1-2-"],[],[]] # 课程时间(节次-节次)(1-2-,3-4-,5-6-,7-8-,9-10-11,12-13-)，可以填多个,也可填入""表示不限制(非必填)
Week_day = [["1","2",""],[""],[]] # 课程星期，可以填多个 星期一：1 星期二：2 星期三：3 星期四：4 星期五：5 星期六：6 星期日：7  ,也可填入""表示不限制(非必填)

```
   
## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。在提交代码前，请确保：

1. 代码符合 PEP 8 规范
2. 添加适当的注释和文档
3. 更新相关测试用例

## 🙏 致谢

特别感谢以下贡献者：

- [W1ndys](https://github.com/W1ndys) - JSON数据分享和技术讨论
- 所有贡献者和用户 - 感谢你们的反馈与支持

## 🔗 相关项目

- [QFNUCourseSelector](https://github.com/W1ndys/QFNUCourseSelector) - W1ndys的项目
## 📄 开源协议

本项目采用 [GNU General Public License v3.0](LICENSE) 开源协议。

## 📞 联系我们

- **邮箱**: [1732373074@aliyun.com](mailto:1732373074@aliyun.com)
- **GitHub Issues**: [提交问题](https://github.com/AuroBreeze/QFNUClassSelector/issues)
- **讨论区**: [GitHub Discussions](https://github.com/AuroBreeze/QFNUClassSelector/discussions)

---

<div align="center">
  <p>QFNU 抢课脚本 | 智能选课助手 | 多账号支持 | 可视化配置</p>
  <p>© 2023 QFNUClassSelector | Made with ❤️ for QFNU Students</p>
</div>


