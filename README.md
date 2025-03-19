# QFNUClassSelector
> QFNU 抢课脚本 | 可视化配置界面 | 智能时间管理 | 多账号支持


<p align="center">
    <img src="https://img.shields.io/badge/version-1.4.0-blue.svg" alt="Version">
    <img src="https://img.shields.io/github/stars/AuroBreeze/QFNUClassSelector?style=flat-square" alt="Stars">
    <img src="https://img.shields.io/github/issues/AuroBreeze/QFNUClassSelector?style=flat-square" alt="Issues">
    <img src="https://img.shields.io/badge/Python-3.12.3-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/状态-开发中-green.svg" alt="Status">
    <img src="https://img.shields.io/badge/License-GPL-green.svg" alt="License">
    <img src="https://img.shields.io/github/forks/AuroBreeze/QFNUClassSelector?style=flat-square" alt="Forks">
    <img src="https://img.shields.io/github/watchers/AuroBreeze/QFNUClassSelector?style=flat-square" alt="Watchers">
    <img src="https://img.shields.io/github/last-commit/AuroBreeze/QFNUClassSelector?style=flat-square" alt="Last Commit">
</p>

<div align="center">
    <h1 >
        ✨ 请给我一个 Star! ✨
    </h1>
</div>



## 项目描述
QFNUClassSelector 是一个使用Python实现的抢课脚本，专门针对曲阜师范大学的选课系统的学生设计。该脚本可以帮助学生自动抢选课程，提高选课效率。

## 🚀 新特性
- **可视化配置界面**：通过 WebUI 轻松管理所有配置参数
- **智能时间管理**：支持设置抢课时段和智能重试间隔
- **跨午夜时间支持**：可配置 00:00 后的结束时间
- **健壮的表单验证**：自动处理空值和非法输入

## 📝 使用说明

### 🖥️ WebUI 使用
```bash
# 启动可视化配置界面
python WebUI/WebUI.py

# 访问 http://localhost:5000 进行配置
```


## 📝 免责声明

> ⚠️ 使用本脚本前请仔细阅读以下声明

1. 本脚本仅供学习和研究目的，用于了解网络编程和自动化技术的实现原理。

2. 使用本脚本可能违反学校相关规定。使用者应自行承担因使用本脚本而产生的一切后果，包括但不限于：

   - 账号被封禁
   - 选课资格被取消
   - 受到学校纪律处分
   - 其他可能产生的不良影响

3. 严禁将本脚本用于：

   - 商业用途
   - 干扰教务系统正常运行
   - 影响其他同学正常选课
   - 其他任何非法或不当用途

4. 下载本脚本即视为您已完全理解并同意本免责声明。请在下载后 24 小时内删除。

5. 开发者对使用本脚本造成的任何直接或间接损失不承担任何责任。


## 安装步骤
1. 确保已安装`Python 3.6<=version<=3.12`版本。
2. 克隆项目到本地：
   ```bash
   git clone https://github.com/AuroBreze/QFNUClassSelector.git
   cd QFNUClassSelector
   ```
## 配置文件说明
`config.toml`文件的配置项说明：

> [!WARNING]
> 
> 下面这些是必填项，一定要填写

```toml
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

```toml
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

```toml
#填写这些东西的时候，注意事项和上面一样，如果你不确定，就在子列表最后填入""表示不限制,或者只留一个空子列表
# [[],[]] == [[""],[""]]

#Time_period这个要注意，一定要按照格式填写，否则可能会出错
#课程时间(节次-节次)(1-2-,3-4-,5-6-,7-8-,9-10-11,12-13-)，可以填多个,也可填入""表示不限制(非必填)

#填这些东西的时候，一定要先去看学期课表，然后再填，不然可能会出错。
Teachers_name = [["老师1", "老师2",""], ["老师3", "老师4"],[]] # 每个课程对应的老师列表(候选功能)，可以填多个也可以留空，用逗号隔开，也可填入""表示不限制，以免最后没有这个老师导致抢课失败。(非必填)
Time_period = [["1-2-"],[],[]] # 课程时间(节次-节次)(1-2-,3-4-,5-6-,7-8-,9-10-11,12-13-)，可以填多个,也可填入""表示不限制(非必填)
Week_day = [["1","2",""],[""],[]] # 课程星期，可以填多个 星期一：1 星期二：2 星期三：3 星期四：4 星期五：5 星期六：6 星期日：7  ,也可填入""表示不限制(非必填)

```
   
## 🙏 致谢

特别感谢以下贡献者：

- [W1ndys](https://github.com/W1ndys) - 技术分享

## 🔗 友情链接

- [QFNUCourseSelector](https://github.com/W1ndys/QFNUCourseSelector)

> QFNU 抢课脚本 | 强智教务抢课脚本 | 强智教务 2017 | 大学抢课脚本 | 学院抢课脚本 | 光速抢课 | 秒级抢课
> Author: W1ndys

## 📄 许可证

本项目采用 [GPL-3.0 许可证](./LICENSE)

## 📞 联系我

- **邮箱**: [1732373074@aliyun.com](mailto:1732373074@aliyun.com)

