# CareReach — Reorganization & Productionization Design

**Date:** 2026-06-12  
**License:** Apache 2.0  
**Python:** >=3.12  
**Package manager:** uv

---

## Goal

Transform the Tantrostav Hackathon prototype into a clean, deployable project named **CareReach**. No new features — only reorganization, bug fixes, dependency updates, and proper project setup.

---

## Directory Structure

```
(root — dir will be renamed to CareReach)
├── app.py                  ← Streamlit entrypoint (routing + sidebar)
├── src/
│   ├── auth.py             ← login/signup UI + bcrypt password hashing
│   ├── db.py               ← all SQLite logic (users, history, appointments)
│   ├── hospital.py         ← Google Maps Places API + geopy geocoding
│   └── pages/
│       ├── chatbot.py      ← Gemini symptom checker page
│       ├── appointment.py  ← hospital finder + booking page
│       └── history.py      ← health history page
├── .streamlit/
│   └── config.toml         ← dark theme, monospace font (unchanged)
├── .env                    ← local secrets (gitignored)
├── .env.example            ← committed template listing all required keys
├── .gitignore
├── LICENSE                 ← Apache 2.0
├── README.md
└── pyproject.toml          ← uv project config, all deps pinned here
```

**Deleted from old project:** `trash/`, `data/Tantrostav/`, `app_fin.py`, `common_utils.py`, `hospital_utils.py`, `requirements.txt`, `install_requirements.ps1`, `install_extensions.ps1`, `extensions.txt`, `*.code-workspace`, `*.zip`

---

## Dependencies (pyproject.toml)

| Package | Old | New | Reason |
|---|---|---|---|
| `streamlit` | 1.29.0 | >=1.40 | bug fixes, current API |
| `google-generativeai` | 0.3.1 | >=0.8 | `gemini-pro` deprecated |
| `joblib` | 1.3.2 | removed | replaced by session_state |
| `geopy` | unpinned | >=2.4 | explicit pin |
| `googlemaps` | unpinned | >=4.10 | explicit pin |
| `bcrypt` | — | >=4.1 | replace SHA-256 |
| `python-dotenv` | missing | >=1.0 | was used but not listed |
| `streamlit-js-eval` | missing | >=0.1.7 | was used but not listed |
| `pandas` | missing | >=2.0 | was used but not listed |

---

## Bug Fixes

| Bug | Fix |
|---|---|
| `gemini-pro` model deprecated | → `gemini-1.5-flash` |
| `st.reload()` doesn't exist | → `st.rerun()` |
| SHA-256 no salt | → bcrypt |
| `save_appointment` never called | → call it on confirm |
| Email silently required | → only send if `SENDER_EMAIL` is set |
| Typo "Analaysis" in history | → "Analysis" |
| `joblib` file persistence (ephemeral on Cloud) | → `st.session_state` only |
| Missing deps in requirements.txt | → all listed in pyproject.toml |

---

## Secrets Required

Users must set these — locally in `.env`, on Streamlit Cloud in app secrets:

```
GOOGLE_AI_API_KEY       # required — Gemini API key
GOOGLE_MAPS_API_KEY     # required — Google Maps Places API key
SENDER_EMAIL            # optional — Gmail address for appointment emails
SENDER_PASSWORD         # optional — Gmail app password
```

---

## Deployment (Streamlit Community Cloud)

- Push repo to GitHub
- Connect on share.streamlit.io, set main file to `app.py`
- Add `GOOGLE_AI_API_KEY` and `GOOGLE_MAPS_API_KEY` to app secrets
- Done

---

## Git Strategy

Commit after each logical unit:
1. `chore: init uv project, pyproject.toml, gitignore, license`
2. `refactor: add src layout, db.py, hospital.py, auth.py`
3. `refactor: add pages (chatbot, appointment, history)`
4. `refactor: wire app.py entrypoint`
5. `fix: update Gemini model, bcrypt auth, st.rerun, appointment save`
6. `docs: update README`
