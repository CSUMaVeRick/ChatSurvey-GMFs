# GMF Questionnaire

A Streamlit-based online questionnaire system for researching public attitudes toward genetically modified foods.

---

## 📋 Project Overview

This project is an academic research questionnaire jointly conducted by Beijing Normal University's School of Journalism and Communication and the University of Zurich's Department of Communication. It collects public opinions on genetically modified foods through an interactive AI conversation system.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- uv package manager

### Installation

**Step 1: Sync the virtual environment**

```bash
uv sync
```

**Step 2: Configure API keys**

Edit the file `.streamlit/secrets.toml` and fill in your API credentials:

```toml
model_api = "your-api-endpoint"
model_key = "your-api-key"
model_name = "your-model-name"
```

> **Note**: The demo version has database submission disabled. You can run the questionnaire locally without configuring the database section.

**Step 3: Run the application**

```bash
streamlit run main.py
```

---

## 📖 How to Use

### For Participants

1. **Read the Informed Consent Form**
   - Click "I Agree to Participate" to continue

2. **Enter Participant Code**
   - You should receive this code from the research team

3. **Complete the Questionnaire**
   - Fill in your personal information
   - Answer questions about AI knowledge and trust in scientists
   - Express your attitudes toward genetically modified foods

4. **Chat with AI**
   - Describe your concerns about genetically modified foods (20-100 characters)
   - Have up to 5 conversation rounds with the AI assistant

5. **Submit Your Response**
   - Complete the post-conversation questions
   - Click "Submit" to finish

### For Researchers

The questionnaire collects the following data:

- Demographic information (age, gender, residence, education, income)
- AI usage and knowledge assessment
- Trust in scientists
- Pre and post attitudes toward genetically modified foods
- AI conversation history
- Attention check questions

---

## 📁 Project Structure

```
GMF-questionnaire/
├── main.py                    # Main application file
├── pyproject.toml             # Project dependencies
├── README.md                  # This file (English)
├── README-CN.md               # Chinese documentation
├── .streamlit/
│   ├── config.toml           # Streamlit configuration
│   └── secrets.toml          # API keys & secrets
└── .venv/                     # Virtual environment
```

---

## 🔧 Configuration

### API Configuration

Edit `.streamlit/secrets.toml`:

```toml
# AI Model Configuration
model_api = "https://api.deepseek.com"
model_key = "sk-your-api-key"
model_name = "deepseek-chat"

# Database Configuration (Optional)
[connections.postgresql]
dialect = "postgresql"
host = "your-database-host"
port = "your-port"
database = "your-database-name"
username = "your-username"
password = "your-password"
```

### Theme Configuration

Edit `.streamlit/config.toml`:

```toml
[theme]
base = "light"
primaryColor = "#1e783b"
textColor = "#000000"
```

---

## 🛠️ Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | >=1.52.0 | Web application framework |
| langchain | >=1.1.0 | AI conversation management |
| langchain-openai | >=1.1.0 | LLM integration |
| sqlalchemy | >=2.0.44 | Database connection |
| pandas | - | Data processing |

---

## ⚠️ Notes

1. **API Key Security**
   - Never commit `secrets.toml` to version control

2. **Database Submission**
   - Currently disabled in demo mode
   - Uncomment the database code in `main.py` to enable

3. **Attention Checks**
   - The questionnaire includes attention check questions
   - Participants must pass these checks for valid responses

---

## 📧 Support

For questions or technical issues, please contact the research team.

---

## 📜 License

This project is for academic research purposes only.

---

**Version**: 0.1.0
**Last Updated**: 2026-03-12
