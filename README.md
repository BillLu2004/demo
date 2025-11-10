[HOW_TO_RUN.md](https://github.com/user-attachments/files/23444782/HOW_TO_RUN.md)
# 如何在本地运行此全栈应用

本文档将指导您如何在本地计算机上成功设置并同时运行本项目的**前端**和**后端**服务。

## 1. 环境要求 (Prerequisites)

- **[Node.js](https://nodejs.org/)**: `v18.x` 或 `v20.x` LTS 版本。
- **[Python](https://www.python.org/)**: `3.10` 或更高版本。
- **[PostgreSQL](https://www.postgresql.org/)**: 本项目使用的数据库。

---

## 2. 数据库配置详解 (非常重要)

在启动后端服务之前，您**必须**在您的计算机上配置好本地数据库。后端服务需要连接到一个真实运行的 PostgreSQL 数据库才能工作。

**a. 确保 PostgreSQL 已安装并运行**

请确保您已在本地安装了 PostgreSQL，并且它的服务正在运行中。

**b. 创建数据库 (如果不存在)**

您需要一个专门为本项目使用的数据库。推荐的数据库名叫 `mybank1`。您可以使用 `pgAdmin` 或其他数据库工具执行以下 SQL 命令来创建它：

```sql
CREATE DATABASE mybank1;
```

**c. 准备数据库用户信息**

您需要一个可以访问 `mybank1` 数据库的用户名和密码。您可以直接使用安装 PostgreSQL 时创建的默认 `postgres` 超级用户，也可以为本项目创建一个专用的新用户。

**d. 配置 `.env` 文件**

这是最关键的一步。本项目的后端使用 `.env` 文件来管理数据库连接信息，以避免将密码等敏感信息直接写入代码。

1.  在 `backend` 目录下，找到一个名为 `.env.example` 的模板文件。
2.  **复制**这个文件，并在**同一目录**下创建一个名为 `.env` 的新文件。
3.  **打开并编辑**您刚刚创建的 `.env` 文件，将其中的值修改为您**自己本地**的数据库配置。

**示例 `.env` 文件内容：**
```ini
# PostgreSQL Database Configuration
DB_NAME=mybank1                 # 您的数据库名
DB_USER=your_postgres_username  # 您的 PostgreSQL 用户名
DB_PASSWORD=your_password       # 您设置的密码
DB_HOST=localhost               # 通常保持 localhost 不变
DB_PORT=5432                    # 通常保持 5432 不变
```

**只有正确完成了这一步，后续的后端服务才能成功启动。**

---

## 3. 后端 (Django) 启动步骤

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
