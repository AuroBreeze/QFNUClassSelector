# QFNUClassSelector (Archived)

<div align="center">

[![Status](https://img.shields.io/badge/status-archived-red.svg)](https://github.com/AuroBreeze/QFNUClassSelector)
[![Python 3.12.3](https://img.shields.io/badge/Python-3.12.3-blue.svg)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/AuroBreeze/QFNUClassSelector?style=flat-square)](https://github.com/AuroBreeze/QFNUClassSelector/stargazers)

</div>

<div align="center">
  <h3>⚠️ 本项目已归档 | This Project is Archived</h3>
  <p>本项目代码逻辑完整(但是并不支持使用，个别API没有维护，自行探索)，思路清晰，但不再进行维护或更新。<br>仅供编程学习与技术研究使用。</p>
</div>

---

## ⚠️ 免责声明 (Disclaimer)

> **在使用本项目代码前，请务必仔细阅读以下条款。下载、克隆或查看本项目代码即代表您同意以下内容：**

1.  **教育目的**：本项目仅作为一个 **Python 网络编程、异步并发及自动化逻辑** 的学习案例。旨在展示 `asyncio`、`httpx` 及 WebUI 交互的技术实现。
2.  **禁止滥用**：**严禁**将本项目代码用于任何形式的攻击、干扰学校教务系统正常运行或违反学校规定的用途。
3.  **风险自负**：运行自动化脚本可能导致账号被封禁、选课资格取消或触犯相关网络安全法律法规。使用者需自行承担因使用本项目代码而产生的任何直接或间接后果。
4.  **无技术支持**：开发者不提供任何形式的使用指导、部署帮助或后续维护。

---

## 📖 项目简介

QFNUClassSelector 是一个基于 Python 实现的自动化任务管理系统示例。它展示了如何构建一个包含多任务并发处理以及网络请求状态管理的完整应用。

本项目采用了现代化的 Python 技术栈，对于希望学习以下技术的开发者具有参考价值：

* **异步并发**：使用 `asyncio` 和 `httpx` 实现高性能的网络请求处理。
* **架构设计**：包含完整的 `ConfigService` (配置服务)、`DataAccess` (数据访问) 和 `NetUtils` (网络工具) 模块化设计。
* **多任务协调**：展示了如何通过 `Semaphore` 控制并发数量以及多线程/多协程间的状态同步。

## 🛠️ 技术栈与环境

如果你想研究本项目代码，你需要具备以下基础环境：

* **Python**: 3.8+ (推荐 3.12)
* **依赖库**: 详见 `requirements.txt`
* **核心模块**:
    * `Essence/`: 核心业务逻辑与调度器
    * `config.toml`: 配置文件标准格式

## 🚀 关于运行与配置

由于本项目已归档且仅供学习，**不再提供详细的使用教程或参数说明**。

* **配置逻辑**：核心配置依赖于 `config.toml` 文件，请参考代码中的数据结构自行理解各字段含义。
* **启动入口**：
    * 命令行入口通常位于 `Essence/main.py`

代码结构清晰，注释相对完整，建议通过阅读源码来理解其运行机制。

## 🤝 贡献与致谢

感谢所有曾经关注和支持过本项目的朋友。

特别感谢 [W1ndys](https://github.com/W1ndys) 在技术层面的交流与分享。

## 📄 开源协议

本项目采用 [GNU General Public License v3.0](LICENSE) 开源协议。

---

<div align="center">
  <p>Made with ❤️ for Code & Technology</p>
</div>
