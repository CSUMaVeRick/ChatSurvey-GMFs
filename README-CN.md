# GMF Questionnaire - 转基因食品问卷调查系统

基于 Streamlit 的在线问卷调查系统，用于研究公众对转基因食品的态度和观念。

---

## 📋 项目概述

本项目是由北京师范大学新闻传播学院与瑞士苏黎世大学传播系联合开展的学术研究问卷，通过交互式 AI 对话系统收集公众对转基因食品的观点。

---

## 🚀 快速开始

### 前置要求

- Python 3.10 或更高版本
- uv 包管理器

### 安装步骤

**步骤 1：同步虚拟环境**

```bash
uv sync
```

**步骤 2：配置 API 密钥**

编辑文件 `.streamlit/secrets.toml` 并填写您的 API 凭据：

```toml
model_api = "your-api-endpoint"
model_key = "your-api-key"
model_name = "your-model-name"
```

> **提示**：Demo 版本已注释掉数据库提交功能，本地运行无需配置数据库部分。

**步骤 3：运行程序**

```bash
streamlit run main.py
```

---

## 📖 使用说明

### 参与者指南

1. **阅读知情同意书**
   - 点击"我同意参加"继续

2. **输入被试编号**
   - 您应该从研究团队获得此编号

3. **完成问卷**
   - 填写个人信息（年龄、性别、教育程度等）
   - 回答关于人工智能知识和科学家信任度的问题
   - 表达您对转基因食品的态度

4. **与 AI 对话**
   - 描述您对转基因食品的关注点（20-100 字）
   - 与 AI 助手进行最多 5 轮对话

5. **提交问卷**
   - 完成对话后的问题
   - 点击"提交"完成

### 研究者指南

问卷收集以下数据：

- 人口统计学信息
- AI 使用情况和知识评估
- 对科学家的信任度
- 对转基因食品的前后态度
- AI 对话历史记录
- 注意力检测题目

---

## 📁 项目结构

```
GMF-questionnaire/
├── main.py                    # 主程序文件
├── pyproject.toml             # 项目依赖
├── README.md                  # 英文说明文档
├── README-CN.md               # 中文说明文档（本文件）
├── .streamlit/
│   ├── config.toml           # Streamlit 配置
│   └── secrets.toml          # API 密钥和机密
└── .venv/                     # 虚拟环境
```

---

## 🔧 配置说明

### API 配置

编辑 `.streamlit/secrets.toml`：

```toml
# AI 模型配置
model_api = "https://api.deepseek.com"
model_key = "sk-your-api-key"
model_name = "deepseek-chat"

# 数据库配置（可选）
[connections.postgresql]
dialect = "postgresql"
host = "your-database-host"
port = "your-port"
database = "your-database-name"
username = "your-username"
password = "your-password"
```

### 主题配置

编辑 `.streamlit/config.toml`：

```toml
[theme]
base = "light"
primaryColor = "#1e783b"
textColor = "#000000"
```

---

## 🛠️ 依赖项

| 包名 | 版本 | 用途 |
|---------|---------|---------|
| streamlit | >=1.52.0 | Web 应用框架 |
| langchain | >=1.1.0 | AI 对话管理 |
| langchain-openai | >=1.1.0 | 大语言模型集成 |
| sqlalchemy | >=2.0.44 | 数据库连接 |
| pandas | - | 数据处理 |

---

## ⚠️ 注意事项

1. **API 密钥安全**
   - 切勿将 `secrets.toml` 提交到版本控制系统

2. **数据库提交**
   - Demo 模式下已禁用数据库提交功能
   - 取消 `main.py` 中数据库代码的注释即可启用

3. **注意力检测**
   - 问卷包含注意力检测题目
   - 参与者必须通过这些检测才能使回答有效

---

## 📧 支持

如有问题或技术困难，请联系研究团队。

---

## 📜 许可证

本项目仅用于学术研究目的。

---

## 📚 引用

如果您在研究中使用本问卷或参考此项目，请引用：

> Xi, Q., Zeng, J., Li, Z., & Schäfer, M. S. (2026). Personalized Persuasion Through Conversational AI: Can DeepSeek Change Perceptions of Genetically Modified Foods in China? *Media and Communication*, 14(0). https://www.cogitatiopress.com/mediaandcommunication/article/view/11451

---

**版本**: 0.1.0
**最后更新**: 2026-03-12
