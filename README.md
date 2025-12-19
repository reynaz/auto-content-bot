# 🤖 Auto-Content-Bot

AI-powered content automation system that integrates Gmail, OpenAI GPT-4, WordPress, and social media platforms.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)

## 🌟 Features

- **📧 Email Monitoring**: Gmail API integration for task extraction
- **🧠 AI Content Generation**: GPT-4 powered content creation
  - Blog posts
  - Case studies
  - Social media posts
  - Product descriptions
- **📝 WordPress Publishing**: REST API integration for drafts/posts
- **📱 Social Media**: LinkedIn, Twitter/X, Facebook posting
- **🌐 Web Dashboard**: Modern UI for workflow management
- **🔄 Hybrid Mode**: Works with real APIs or mock data

## 📁 Project Structure

```
auto-content-bot/
├── main.py              # CLI pipeline entry point
├── dashboard.py         # Flask web dashboard
├── config.py            # Configuration management
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
├── services/
│   ├── ai_engine.py     # OpenAI GPT-4 integration
│   ├── gmail_listener.py # Gmail API + SMTP
│   ├── wp_publisher.py  # WordPress REST API
│   └── social_manager.py # Social media APIs
└── templates/
    └── dashboard.html   # Dashboard UI
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd auto-content-bot
pip install -r requirements.txt
```

### 2. Configuration (Optional)

Copy the environment template and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials. Without credentials, the system runs in demo mode with mock data.

### 3. Run CLI Pipeline

```bash
# Run with mock data (demo mode)
python main.py --demo

# Run with real APIs (requires configuration)
python main.py
```

### 4. Run Web Dashboard

```bash
python dashboard.py
```

Open http://localhost:5000 in your browser.

## 🔧 API Configuration

### OpenAI

```env
OPENAI_API_KEY=sk-proj-your-key-here
```

### WordPress

1. Go to Users → Profile → Application Passwords
2. Create a new application password

```env
WP_URL=https://yoursite.com/wp-json/wp/v2
WP_USER=your-username
WP_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

### Gmail

1. Enable Gmail API in Google Cloud Console
2. Download `credentials.json`
3. First run will prompt for OAuth

```env
GMAIL_CREDENTIALS_PATH=credentials.json
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Social Media

```env
# LinkedIn
LINKEDIN_ACCESS_TOKEN=your-access-token

# Twitter/X
TWITTER_API_KEY=your-api-key
TWITTER_API_SECRET=your-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-access-token-secret
```

## 📊 Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Gmail     │────▶│  AI Engine  │────▶│  WordPress  │
│   Inbox     │     │   (GPT-4)   │     │    Draft    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Social    │
                    │   Media     │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Email     │
                    │   Report    │
                    └─────────────┘
```

## 🎮 Demo Mode

Set `DEMO_MODE=true` in `.env` or don't configure API keys to run with mock data. Perfect for:

- Testing the pipeline
- Demonstrations
- Development without API costs

## 📸 Dashboard Features

- **Integration Status**: Real-time API connection status
- **Quick Actions**: One-click pipeline execution
- **Content Generator**: Create content on-demand
- **Preview & Publish**: Review before publishing
- **Execution Logs**: Live activity monitoring

## 🛠️ Development

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest

# Run dashboard in debug mode
FLASK_DEBUG=1 python dashboard.py
```

## 📄 License

MIT License - Feel free to use and modify.

---

Built with ❤️ for content automation
