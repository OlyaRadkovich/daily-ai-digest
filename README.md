# 🚀 Daily AI News Digest for QA & SDET

A fully automated Python bot that fetches critical technical news regarding **Applied AI in QA and Software Development** and delivers a concise digest to a private **Google Chat** space every weekday.


## ✨ Features

* **Intelligent Curation:** Uses Perplexity's `sonar-reasoning` (or `sonar-pro`) model to search the web for the latest updates.
* **Targeted Content:**
    * **Test Automation:** Playwright, Selenium, AI Agents, Self-healing tests.
    * **Manual QA:** AI for test case generation, visual regression, bug reporting.
    * **SDET Tools:** Cursor, GitHub Copilot, Local LLMs for coding tests.
    * **Strategic Context:** AI Regulation, Security, and industry shifts.
* **Google Chat Formatting:** Automatically cleans up Markdown links and removes citations for a clean chat experience.
* **Scheduled Automation:** Runs automatically **Monday through Friday at 07:00 UTC**.
* **Zero-Maintenance:** Deployed via GitHub Actions with no need for a dedicated server.

## 🛠 Tech Stack

* **Core:** Python 3.12
* **HTTP Client:** `httpx`
* **Configuration:** `pydantic-settings`
* **Logging:** `loguru`
* **CI/CD:** GitHub Actions
* **AI Provider:** OpenRouter API (Accessing Perplexity models)

## 📂 Project Structure

```text
daily-ai-digest/
├── .github/workflows/
│   └── daily_run.yml    # Cron schedule configuration (Mon-Fri)
├── src/
│   ├── __init__.py
│   ├── client_ai.py     # Prompt engineering & OpenRouter API client
│   ├── config.py        # Environment variables & Pydantic settings
│   ├── publisher.py     # Google Chat formatting & webhook delivery
│   └── main.py          # Entry point
├── .env.example         # Template for environment variables
├── .gitignore
├── README.md
└── requirements.txt

```

## 🚀 Setup & Usage

### 1. Prerequisites

* Python 3.12+
* An [OpenRouter](https://openrouter.ai/) API Key (with credits).
* A **Google Chat** Space with an Incoming Webhook URL.

### 2. Local Installation

Clone the repository and install dependencies.

### 3. Configuration

Create a `.env` file in the root directory:

```ini
OPENROUTER_API_KEY=your-key-here
GOOGLE_CHAT_WEBHOOK_URL=[https://chat.googleapis.com....]

```

### 4. Running Locally

```bash
python -m src.main

```

## 🤖 GitHub Actions Deployment

To make the bot run automatically:

1. Push your code to a GitHub repository.
2. Go to **Settings** -> **Secrets and variables** -> **Actions**.
3. Add the following **Repository Secrets**:
* `OPENROUTER_API_KEY`
* `GOOGLE_CHAT_WEBHOOK_URL`


4. The workflow is defined in `.github/workflows/daily_run.yml` and will trigger automatically at 09:00 UTC on weekdays.

You can also trigger it manually via the **Actions** tab -> **Run workflow**.

## ⚙️ Customization

* **Change the Prompt:** Edit `src/client_ai.py` to adjust the topics or persona.
* **Change the Model:** Edit `src/config.py`. Recommended models:
* `perplexity/sonar-reasoning` (Best quality, slower)
* `perplexity/sonar-pro` (Good balance)


* **Change Schedule:** Edit the cron expression in `.github/workflows/daily_run.yml`.