# ZULU — AI Assistant

> *"At your service."*

ZULU is a JARVIS-inspired AI assistant built in Python. It listens to your voice, responds with speech, answers questions, opens apps, searches the web, and keeps you updated on world events.

---

## Features

- 🎙️ **Voice Recognition** — speak to ZULU using your microphone
- 🔊 **Text-to-Speech** — ZULU talks back
- 🧠 **LLM Chat** — powered by GPT-4o-mini for intelligent conversation
- 📰 **Current Events** — real-time world news via NewsAPI
- 🖥️ **Computer Control** — open applications by name
- 🔍 **Web Search** — search Google from your voice

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ZULU.git
cd ZULU
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> **macOS note:** You may need `brew install portaudio` before `pyaudio` installs.

### 3. Configure API keys
```bash
cp .env.example .env
```
Edit `.env` and add:
- `OPENAI_API_KEY` — from [platform.openai.com](https://platform.openai.com/api-keys)
- `NEWS_API_KEY` — free key from [newsapi.org](https://newsapi.org/register)

### 4. Run ZULU
```bash
python main.py
```

---

## Usage

Say or type your command. ZULU responds to:

| Command | Example |
|---|---|
| News / current events | *"ZULU, what's happening in the world?"* |
| Open an app | *"Open Spotify"* |
| Web search | *"Search for latest AI news"* |
| General chat | *"What's the capital of Japan?"* |
| Exit | *"Goodbye"* |

---

## Project Structure

```
ZULU/
├── main.py              # Entry point
├── zulu/
│   ├── core.py          # Main orchestrator
│   ├── voice.py         # Speech recognition + TTS
│   ├── chat.py          # LLM conversation
│   ├── news.py          # News fetching
│   └── computer.py      # App control + web search
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Roadmap

- [ ] Wake word detection (always-on listening)
- [ ] Calendar and reminders integration
- [ ] Smart home control
- [ ] Custom voice / ElevenLabs TTS
- [ ] GUI dashboard
