# CareReach

AI-powered telemedicine platform for remote healthcare consultations.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red)](https://streamlit.io)

## Features

| Feature | Description |
|---|---|
| **Symptom Checker** | Chat with Google Gemini 1.5 Flash about your symptoms and get instant analysis |
| **Hospital Finder** | Search nearby hospitals by specialist type using Google Maps Places API |
| **Appointment Booking** | Select a date, time, specialist, and hospital — saved to your account |
| **Health History** | Review all past symptom conversations |
| **Secure Auth** | Signup and login with bcrypt-hashed passwords stored in SQLite |

## Setup

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — `winget install astral-sh.uv` (Windows) or `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux)
- [Google Gemini API key](https://aistudio.google.com/) — free tier available
- [Google Maps Platform API key](https://console.cloud.google.com/) — enable the **Places API**

### Install

```bash
git clone <repo-url>
cd CareReach
uv sync
```

### Configure

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

```env
# Backend secret — only the Maps key is needed here
GOOGLE_MAPS_API_KEY=your_maps_api_key

# Optional — enables appointment confirmation emails:
SENDER_EMAIL=your_gmail@gmail.com
SENDER_PASSWORD=your_gmail_app_password

# Note: Gemini API key is NOT set here — each user enters their own in the app UI.
```

### Run

```bash
uv run streamlit run app.py
```

Open `http://localhost:8501`.

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set **Main file path** to `app.py`
4. Under **Advanced settings → Secrets**, add:

```toml
GOOGLE_MAPS_API_KEY = "your_maps_api_key"
```

5. Click **Deploy** — done.

## Project Structure

```
.
├── app.py                  # Streamlit entrypoint — routing and sidebar
├── src/
│   ├── auth.py             # Login and signup UI
│   ├── db.py               # SQLite helpers (users, history, appointments)
│   ├── hospital.py         # Google Maps hospital search + optional email
│   └── pages/
│       ├── chatbot.py      # Gemini 1.5 Flash symptom checker
│       ├── appointment.py  # Hospital finder and booking
│       └── history.py      # Health history viewer
├── .streamlit/
│   └── config.toml         # Dark theme, monospace font
├── .env.example            # Secrets template — copy to .env
├── pyproject.toml          # uv project config and dependencies
└── uv.lock                 # Locked dependency tree
```

## Secrets Reference

### Backend secrets (set by you — in `.env` locally, in Streamlit Cloud app secrets for deployment)

| Key | Required | Where to get it |
|---|---|---|
| `GOOGLE_MAPS_API_KEY` | Yes | [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Enable Places API → Credentials |
| `SENDER_EMAIL` | No | Your Gmail address |
| `SENDER_PASSWORD` | No | [Gmail App Password](https://myaccount.google.com/apppasswords) — requires 2FA enabled |

> **Note on email:** If `SENDER_EMAIL` / `SENDER_PASSWORD` are not set, appointments are still saved to the database — the confirmation email is simply skipped.

### User-provided (entered in the app UI — never stored on the server)

| Key | Required | Where to get it |
|---|---|---|
| Gemini API Key | Yes, per user | [Google AI Studio](https://aistudio.google.com/) → Get API key (free tier available) |

Each user enters their own Gemini API key via the **⚙️ AI Settings** panel in the sidebar after logging in. The app fetches their available models dynamically and lets them choose which one to use. The key lives only in their browser session and is never persisted.

## Tech Stack

- **UI:** [Streamlit](https://streamlit.io/) 1.58+
- **AI:** Google Gemini 1.5 Flash via `google-generativeai`
- **Maps:** Google Maps Places API via `googlemaps` + `geopy`
- **Database:** SQLite (local file `users.db`)
- **Auth:** `bcrypt` password hashing
- **Package manager:** [uv](https://docs.astral.sh/uv/)

## License

Apache 2.0 — see [LICENSE](LICENSE).
