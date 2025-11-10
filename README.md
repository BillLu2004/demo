[HOW_TO_RUN.md](https://github.com/user-attachments/files/23444761/HOW_TO_RUN.md)
# 如何在本地运行此全栈应用

本文档将指导您如何在本地计算机上成功设置并同时运行本项目的**前端**和**后端**服务。

## 1. 环境要求 (Prerequisites)

在开始之前，请确保您的计算机上已安装以下软件：

- **[Node.js](https://nodejs.org/)**: 用于运行前端项目。推荐 `v18.x` 或 `v20.x` LTS 版本。
- **[Python](https://www.python.org/)**: 用于运行后端项目。推荐 `3.10` 或更高版本。
- **[PostgreSQL](https://www.postgresql.org/)**: 本项目使用的数据库。

**重要**: 请确保您的 PostgreSQL 数据库中包含一个名为 `mybank1` 的数据库，并且有一个用户名为 `postgres`、密码为 `123456` 的用户可以访问它。如果您的数据库配置不同，请在启动后端前，先修改 `backend/bank_project/settings.py` 文件中的 `DATABASES` 配置。

## 2. 操作步骤

您需要打开 **两个** 独立的终端（或命令行窗口），一个用于后端，一个用于前端。

---

### 终端一：启动后端 (Django)

**a. 进入后端目录**

```bash
cd path/to/your/project/backend
```

**b. 创建并激活 Python 虚拟环境**

如果您是第一次设置，需要先创建虚拟环境：
```bash
python -m venv venv
```

然后，**激活**它：
- 在 Windows (PowerShell/CMD) 上:
  ```powershell
  .\venv\Scripts\activate
  ```
- 在 macOS 或 Linux 上:
  ```bash
  source venv/bin/activate
  ```
激活成功后，您会在命令行提示符前看到 `(venv)` 字样。

**c. 安装后端依赖**

```bash
pip install -r requirements.txt
```

**d. 初始化数据库**

如果您是第一次设置，需要运行以下命令来创建数据库表：
```bash
python manage.py migrate
```

**e. (可选) 填充初始数据**

为了让应用有内容，您可以运行种子脚本来填充模拟数据：
```bash
python seed_data.py
```

**f. 启动后端服务器**

```bash
python manage.py runserver
```

如果一切顺利，您会看到服务在 `http://127.0.0.1:8000/` 上运行。**请保持此终端窗口持续运行。**

---

### 终端二：启动前端 (Vue)

**a. 进入前端目录**

```bash
cd path/to/your/project/frontend
```

**b. 安装前端依赖**

如果您是第一次设置，需要运行：
```bash
npm install
```

**c. 启动前端开发服务器**

```bash
npm run dev
```

终端会显示一个 `Local:` 地址，例如 `http://localhost:5177/`。

---

## 3. 访问应用

当**两个终端服务都已成功启动**后，打开您的网页浏览器，访问前端终端中显示的 `Local:` 地址。现在，您应该可以与完整的银行管理系统进行交互了。
