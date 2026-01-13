# 🤖 Auto-Content-Bot

**AI-powered content automation system demo** - Built to demonstrate my ability to design and implement API integrations for content automation workflows.

> ⚠️ **Note:** This is a **demonstration project** built in one day to showcase my technical skills and enthusiasm. It uses mock functions to simulate API behavior. Given the opportunity, I am fully capable of implementing the real integrations.

---

## 🎯 Purpose

This project demonstrates my understanding of building an AI-powered content automation pipeline that:
- Monitors email for content requests
- Generates content using AI
- Publishes to CMS and social media platforms
- Sends automated reports

---

## � Demo vs Production Implementation

| Component | Current (Demo) | Production Ready |
|-----------|----------------|------------------|
| **Gmail API** | ✅ Mock email data returned | Real OAuth2 + Gmail API integration code is written, needs credentials |
| **OpenAI GPT-4** | ✅ Mock content responses | Real OpenAI SDK integration code is written, needs API key |
| **WordPress API** | ✅ Mock post creation | Real REST API integration code is written, needs site credentials |
| **LinkedIn API** | ✅ Mock posting simulation | Real OAuth2 integration code is written, needs access token |
| **Twitter API** | ✅ Mock tweet simulation | Real Tweepy integration code is written, needs API keys |
| **Email (SMTP)** | ✅ Mock sending | Real SMTP integration code is written, needs app password |

**Key Point:** The actual API integration code exists in the codebase. Switching from demo to production only requires adding real credentials to the `.env` file and setting `DEMO_MODE=false`.

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI demo
python main.py --demo

# Run web dashboard
python dashboard.py
# Open http://localhost:5000
```

---

## 📁 Project Structure

```
auto-content-bot/
├── main.py              # CLI pipeline entry point
├── dashboard.py         # Flask web dashboard
├── config.py            # Configuration management
├── services/
│   ├── ai_engine.py     # OpenAI integration (mock/real)
│   ├── gmail_listener.py # Gmail API integration (mock/real)
│   ├── wp_publisher.py  # WordPress REST API (mock/real)
│   └── social_manager.py # Social media APIs (mock/real)
└── templates/
    └── dashboard.html   # Dashboard UI
```

---

## � Architecture

```
Email Inbox → AI Content Generation → WordPress Draft
                    ↓
              Social Media Posts
                    ↓
              Email Report
```

---

## 💡 What I Learned / Demonstrated

- RESTful API design and consumption
- OAuth2 authentication flows
- Python async patterns and service architecture
- Flask web application development
- Environment-based configuration management
- Clean code separation (services, config, UI)

---

## � Next Steps (Production)

With real API credentials, this system can:
1. Actually monitor Gmail inbox for task emails
2. Generate real content using GPT-4
3. Create real WordPress posts/drafts
4. Post to actual LinkedIn/Twitter accounts
5. Send real email reports via SMTP

---

## 📝 About This Project

**Built in:** ~1 day  
**Purpose:** Internship application demo  
**Status:** Fully functional demo with mock data  

I built this project to demonstrate my enthusiasm and capability to work on AI-powered automation systems. I am eager to learn and implement the full production version with real integrations.

---

*Built with Python, Flask, and enthusiasm* 🚀
<<<<<<< HEAD


