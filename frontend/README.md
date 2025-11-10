# Simple Bank - Frontend

这是一个基于 Vue 3 和 Element Plus 构建的银行核心管理系统前端界面。

## 项目简介

本项目旨在为银行员工提供一个简洁、高效的后台管理界面，用于管理客户、账户、交易和贷款等核心业务。

## 环境要求 (Prerequisites)

在开始之前，请确保您的开发环境中已安装以下软件：

- **Node.js**: `^18.0.0` 或 `^20.0.0` 或更高版本。
  - 您可以从 [Node.js 官方网站](https://nodejs.org/) 下载并安装。
  - `npm` (Node Package Manager) 会随 Node.js 一同安装。

## 安装与启动 (Installation and Setup)

请按照以下步骤在您的本地环境中设置并运行此项目。

### 1. 克隆或下载项目 (Clone or Download the Project)

首先，获取项目代码。如果您使用 Git，可以克隆此仓库：

```bash
git clone <repository-url>
```

或者，直接下载并解压项目文件。

### 2. 进入项目目录 (Navigate to the Project Directory)

使用命令行工具，进入本项目的前端文件夹：

```bash
cd path/to/your/project/frontend
```

### 3. 安装依赖 (Install Dependencies)

在 `frontend` 目录下，运行以下命令来安装项目所需的所有依赖库：

```bash
npm install
```
该命令会根据 `package.json` 文件自动下载所有必需的模块到 `node_modules` 文件夹中。

### 4. 启动开发服务器 (Run the Development Server)

安装完成后，运行以下命令来启动本地开发服务器：

```bash
npm run dev
```

该命令会启动一个热重载的开发服务器。您将在终端看到类似以下的输出：

```
  VITE vX.X.X  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 5. 在浏览器中访问 (Access in Browser)

打开您的网页浏览器，并访问终端中显示的 `Local` 地址 (通常是 `http://localhost:5173`)。

现在，您应该能看到正在运行的应用界面了。

## 项目技术栈 (Tech Stack)

- **框架 (Framework)**: [Vue 3](https://vuejs.org/)
- **UI 库 (UI Library)**: [Element Plus](https://element-plus.org/)
- **构建工具 (Build Tool)**: [Vite](https://vitejs.dev/)
- **状态管理 (State Management)**: [Pinia](https://pinia.vuejs.org/)
- **路由 (Routing)**: [Vue Router](https://router.vuejs.org/)
- **语言 (Language)**: [TypeScript](https://www.typescriptlang.org/)
- **代码规范 (Linting & Formatting)**: ESLint, Prettier
