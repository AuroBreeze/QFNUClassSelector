# 📌 QFNUClassSelector 版本发布说明

## 🔖 v2.0.0 (2025-08-27)

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
- 优化数据库查询性能，减少响应时间
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

### ⬇️ 下载

- [v1.5.0 发布包](https://github.com/AuroBreeze/QFNUClassSelector/releases/tag/v1.5.0)
- [完整更新日志](https://github.com/AuroBreeze/QFNUClassSelector/commits/main)

### 📋 系统要求

- Python 3.8+
- 现代浏览器 (Chrome 90+, Firefox 88+, Edge 90+)
- Windows 10+/macOS 10.15+/Linux (x86_64)

### 🔄 升级说明

从旧版本升级的用户请先备份您的配置文件 (`config.toml`)，然后按照以下步骤操作：

1. 下载最新版本
2. 解压到新目录
3. 复制旧版配置文件到新目录
4. 运行 `pip install -r requirements.txt` 更新依赖
5. 启动程序

### 📞 问题反馈

如遇到任何问题，请提交 [Issue](https://github.com/AuroBreeze/QFNUClassSelector/issues) 或通过邮件联系我们。

---

<div align="center">
  <p>© 2025 QFNUClassSelector | Made with ❤️ for QFNU Students</p>
</div>
