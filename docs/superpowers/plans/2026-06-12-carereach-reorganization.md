# CareReach Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the Tantrostav Hackathon prototype into a clean, deployable telemedicine project named CareReach with proper uv packaging, src/ layout, fixed bugs, updated dependencies, Apache 2.0 license, and Streamlit Cloud deployment config.

**Architecture:** Single Streamlit app (`app.py` at root) with utility modules under `src/` (db, hospital, auth) and page modules under `src/pages/`. All state via `st.session_state`, SQLite for persistence, Gemini 1.5 Flash for AI, Google Maps for hospital search.

**Tech Stack:** Python 3.12+, Streamlit >=1.40, google-generativeai >=0.8, googlemaps >=4.10, geopy >=2.4, bcrypt >=4.1, pandas >=2.0, streamlit-js-eval >=0.1.7, python-dotenv >=1.0, uv

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Create | `pyproject.toml` | uv project config, all deps |
| Create | `.gitignore` | ignore .venv, .env, users.db, data/, __pycache__ |
| Create | `LICENSE` | Apache 2.0 full text |
| Create | `.env.example` | template showing all required/optional secrets |
| Create | `app.py` | Streamlit entrypoint — init DB, routing, sidebar |
| Create | `src/__init__.py` | empty, makes src a package |
| Create | `src/db.py` | SQLite: init_db, auth, history, appointments |
| Create | `src/hospital.py` | Google Maps hospital search + optional email |
| Create | `src/auth.py` | login/signup Streamlit UI |
| Create | `src/pages/__init__.py` | empty |
| Create | `src/pages/chatbot.py` | Gemini symptom checker page |
| Create | `src/pages/appointment.py` | hospital finder + booking page |
| Create | `src/pages/history.py` | health history page |
| Update | `README.md` | full project docs |
| Keep | `.streamlit/config.toml` | already correct |
| Delete | `app_fin.py`, `common_utils.py`, `hospital_utils.py` | replaced |
| Delete | `requirements.txt`, `*.ps1`, `extensions.txt`, `*.code-workspace`, `*.zip` | replaced by uv |
| Delete | `trash/`, `data/Tantrostav/` | dead code |

---

## Task 1: Git init + uv project scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`

- [ ] **Step 1: Init git repo**

```powershell
cd "V:\Code\ProjectCode\Tantrostav Hackathon"
git init
git config user.email "krishnalsh2004@gmail.com"
git config user.name "CareReach"
```

- [ ] **Step 2: Install uv if not present, init project**

```powershell
# Check if uv is available
uv --version
# If not: winget install astral-sh.uv
# Init without creating a new directory (we're already in the project dir)
uv init --no-workspace
```

- [ ] **Step 3: Write pyproject.toml**

Delete the auto-generated `pyproject.toml` if any and write:

```toml
[project]
name = "carereach"
version = "0.1.0"
description = "AI-powered telemedicine platform for remote consultations"
readme = "README.md"
license = { text = "Apache-2.0" }
requires-python = ">=3.12"
dependencies = [
    "streamlit>=1.40",
    "google-generativeai>=0.8",
    "geopy>=2.4",
    "googlemaps>=4.10",
    "bcrypt>=4.1",
    "python-dotenv>=1.0",
    "streamlit-js-eval>=0.1.7",
    "pandas>=2.0",
]
```

- [ ] **Step 4: Write .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
*.egg-info/

# Secrets & local state
.env
users.db
data/

# Streamlit
.streamlit/secrets.toml

# OS
.DS_Store
Thumbs.db

# Editors
.vscode/
*.code-workspace

# Project artifacts
trash/
*.zip
```

- [ ] **Step 5: Install dependencies with uv**

```powershell
uv sync
```

Expected: uv creates `.venv/` and `uv.lock`, installs all packages.

- [ ] **Step 6: Commit**

```powershell
git add pyproject.toml .gitignore
git commit -m "chore: init uv project with Python 3.12 and all dependencies"
```

---

## Task 2: License + secrets template

**Files:**
- Create: `LICENSE`
- Create: `.env.example`

- [ ] **Step 1: Write LICENSE (Apache 2.0)**

```
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.

   "License" shall mean the terms and conditions for use, reproduction,
   and distribution as defined by Sections 1 through 9 of this document.

   "Licensor" shall mean the copyright owner or entity authorized by
   the copyright owner that is granting the License.

   "Legal Entity" shall mean the union of the acting entity and all
   other entities that control, are controlled by, or are under common
   control with that entity. For the purposes of this definition,
   "control" means (i) the power, direct or indirect, to cause the
   direction or management of such entity, whether by contract or
   otherwise, or (ii) ownership of fifty percent (50%) or more of the
   outstanding shares, or (iii) beneficial ownership of such entity.

   "You" (or "Your") shall mean an individual or Legal Entity
   exercising permissions granted by this License.

   "Source" form shall mean the preferred form for making modifications,
   including but not limited to software source code, documentation
   source, and configuration files.

   "Object" form shall mean any form resulting from mechanical
   transformation or translation of a Source form, including but
   not limited to compiled object code, generated documentation,
   and conversions to other media types.

   "Work" shall mean the work of authorship made available under
   the License, as indicated by a copyright notice that is included in
   or attached to the work (an example is provided in the Appendix below).

   "Derivative Works" shall mean any work, whether in Source or Object
   form, that is based on (or derived from) the Work and for which the
   editorial revisions, annotations, elaborations, or other modifications
   represent, as a whole, an original work of authorship. For the purposes
   of this License, Derivative Works shall not include works that remain
   separable from, or merely link (or bind by name) to the interfaces of,
   the Work and Derivative Works thereof.

   "Contribution" shall mean, as submitted to the Licensor for inclusion
   in the Work by the copyright owner or by an individual or Legal Entity
   authorized to submit on behalf of the copyright owner. For the purposes
   of this definition, "submit" means any form of electronic, verbal, or
   written communication sent to the Licensor or its representatives,
   including but not limited to communication on electronic mailing lists,
   source code control systems, and issue tracking systems that are managed
   by, or on behalf of, the Licensor for the purpose of communicating and
   discussing the Work, but excluding communication that is conspicuously
   marked or designated in writing by the copyright owner as "Not a
   Contribution."

   "Contributor" shall mean Licensor and any Legal Entity on behalf of
   whom a Contribution has been received by the Licensor and included
   within the Work.

2. Grant of Copyright License. Subject to the terms and conditions of
   this License, each Contributor hereby grants to You a perpetual,
   worldwide, non-exclusive, no-charge, royalty-free, irrevocable
   copyright license to reproduce, prepare Derivative Works of,
   publicly display, publicly perform, sublicense, and distribute the
   Work and such Derivative Works in Source or Object form.

3. Grant of Patent License. Subject to the terms and conditions of
   this License, each Contributor hereby grants to You a perpetual,
   worldwide, non-exclusive, no-charge, royalty-free, irrevocable
   (except as stated in this section) patent license to make, have made,
   use, offer to sell, sell, import, and otherwise transfer the Work,
   where such license applies only to those patent claims licensable
   by such Contributor that are necessarily infringed by their
   Contribution(s) alone or by the combination of their Contribution(s)
   with the Work to which such Contribution(s) was submitted. If You
   institute patent litigation against any entity (including a cross-claim
   or counterclaim in a lawsuit) alleging that the Work or any
   Contribution embodied within the Work constitutes direct or contributory
   patent infringement, then any patent licenses granted to You under
   this License for that Work shall terminate as of the date such
   litigation is filed.

4. Redistribution. You may reproduce and distribute copies of the
   Work or Derivative Works thereof in any medium, with or without
   modifications, and in Source or Object form, provided that You
   meet the following conditions:

   (a) You must give any other recipients of the Work or Derivative
       Works a copy of this License; and

   (b) You must cause any modified files to carry prominent notices
       stating that You changed the files; and

   (c) You must retain, in the Source form of any Derivative Works
       that You distribute, all copyright, patent, trademark, and
       attribution notices from the Source form of the Work,
       excluding those notices that do not pertain to any part of
       the Derivative Works; and

   (d) If the Work includes a "NOTICE" text file as the end of this
       LICENSE file, You must include a readable copy of the
       attribution notices contained within such NOTICE file, in
       at least one of the following places: within a NOTICE text
       file distributed as part of the Derivative Works; within
       the Source form or documentation, if provided along with the
       Derivative Works; or, within a display generated by the
       Derivative Works, if and wherever such third-party notices
       normally appear. The contents of the NOTICE file are for
       informational purposes only and do not modify the License.

5. Submission of Contributions. Unless You explicitly state otherwise,
   any Contribution intentionally submitted for inclusion in the Work
   by You to the Licensor shall be under the terms and conditions of
   this License, without any additional terms or conditions.

6. Trademarks. This License does not grant permission to use the trade
   names, trademarks, service marks, or product names of the Licensor,
   except as required for reasonable and customary use in describing the
   origin of the Work and reproducing the content of the NOTICE file.

7. Disclaimer of Warranty. Unless required by applicable law or
   agreed to in writing, Licensor provides the Work (and each
   Contributor provides its Contributions) on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
   implied, including, without limitation, any warranties or conditions
   of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
   PARTICULAR PURPOSE. You are solely responsible for determining the
   appropriateness of using or reproducing the Work and assume any
   risks associated with Your exercise of permissions under this License.

8. Limitation of Liability. In no event and under no legal theory,
   whether in tort (including negligence), contract, or otherwise,
   unless required by applicable law (such as deliberate and grossly
   negligent acts) or agreed to in writing, shall any Contributor be
   liable to You for damages, including any direct, indirect, special,
   incidental, or exemplary damages of any character arising as a
   result of this License or out of the use or inability to use the
   Work (including but not limited to damages for loss of goodwill,
   work stoppage, computer failure or malfunction, or all other
   commercial damages or losses), even if such Contributor has been
   advised of the possibility of such damages.

9. Accepting Warranty or Additional Liability. While redistributing
   the Work or Derivative Works thereof, You may choose to offer,
   and charge a fee for, acceptance of support, warranty, indemnity,
   or other liability obligations and/or rights consistent with this
   License. However, in accepting such obligations, You may offer only
   conditions that are consistent with this License and for which you
   can accept full responsibility, and indemnify each Contributor for
   any liability incurred by, or claims asserted against, such
   Contributor by reason of your accepting any such warranty or
   additional liability.

END OF TERMS AND CONDITIONS

Copyright 2026 CareReach Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

- [ ] **Step 2: Write .env.example**

```env
# ── Required ──────────────────────────────────────────────────────────────────
# Google Gemini API key — get from https://aistudio.google.com/
GOOGLE_AI_API_KEY=your_gemini_api_key_here

# Google Maps Platform API key — enable Places API at https://console.cloud.google.com/
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# ── Optional (appointment confirmation emails) ─────────────────────────────────
# Gmail address to send from (requires 2FA + App Password, NOT your regular password)
SENDER_EMAIL=your_gmail@gmail.com

# Gmail App Password — generate at https://myaccount.google.com/apppasswords
SENDER_PASSWORD=your_gmail_app_password
```

- [ ] **Step 3: Commit**

```powershell
git add LICENSE .env.example
git commit -m "chore: add Apache 2.0 license and secrets template"
```

---

## Task 3: src/db.py — all database logic

**Files:**
- Create: `src/__init__.py`
- Create: `src/db.py`

- [ ] **Step 1: Create src/ package**

Create empty `src/__init__.py`.

- [ ] **Step 2: Write src/db.py**

```python
import sqlite3
from datetime import datetime

import bcrypt

DB_PATH = "users.db"


def get_conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT DEFAULT 'Patient'
            );
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                symptoms TEXT,
                analysis TEXT,
                timestamp TEXT
            );
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                specialist TEXT,
                date TEXT,
                time TEXT,
                hospital TEXT
            );
        """)


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def authenticate_user(username: str, password: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT password FROM users WHERE username = ?", (username,)
        ).fetchone()
    return bool(row) and _verify(password, row[0])


def add_user(username: str, password: str) -> bool:
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, _hash(password)),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def save_history(username: str, symptoms: str, analysis: str) -> None:
    status = "Analysis Completed" if analysis.strip() else "Analysis Not Completed"
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO history (username, symptoms, analysis, timestamp) VALUES (?, ?, ?, ?)",
            (username, symptoms, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )


def fetch_history(username: str) -> list[tuple]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT symptoms, analysis, timestamp FROM history "
            "WHERE username = ? ORDER BY timestamp DESC",
            (username,),
        ).fetchall()


def save_appointment(
    username: str, specialist: str, date: str, time: str, hospital: str
) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO appointments (username, specialist, date, time, hospital) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, specialist, date, time, hospital),
        )
```

- [ ] **Step 3: Commit**

```powershell
git add src/__init__.py src/db.py
git commit -m "refactor: add src/db.py with bcrypt auth and SQLite helpers"
```

---

## Task 4: src/hospital.py — Maps + optional email

**Files:**
- Create: `src/hospital.py`

- [ ] **Step 1: Write src/hospital.py**

```python
import os
import smtplib

import googlemaps
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from requests.exceptions import RequestException

load_dotenv()

_MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
_SENDER_EMAIL = os.getenv("SENDER_EMAIL")
_SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

gmaps = googlemaps.Client(key=_MAPS_KEY)
_geo = Nominatim(user_agent="carereach_locator")

_SPECIALTY_KEYWORDS: dict[str, list[str]] = {
    "General Physician": ["general physician", "general checkup", "consult"],
    "neurologist": ["neurologist", "neuro", "brain", "nerve"],
    "dermatologist": ["dermatologist", "skin", "derma"],
    "cardiologist": ["cardiologist", "cardio", "heart"],
    "orthopedist": ["orthopedist", "orthopedic", "bone", "joint"],
    "pediatrician": ["pediatrician", "child", "pediatrics"],
    "gynecologist": ["gynecologist", "gyno", "obgyn"],
    "psychiatrist": ["psychiatrist", "mental health", "psych"],
    "dentist": ["dentist", "dental", "oral"],
    "oncologist": ["oncologist", "cancer"],
    "endocrinologist": ["endocrinologist", "hormone", "gland"],
    "ophthalmologist": ["ophthalmologist", "eye", "vision"],
    "urologist": ["urologist", "urinary", "kidney"],
    "gastroenterologist": ["gastroenterologist", "gastro", "stomach"],
    "pulmonologist": ["pulmonologist", "lung", "respiratory"],
    "ent": ["ENT", "ear nose throat", "otolaryngologist"],
    "rheumatologist": ["rheumatologist", "arthritis", "autoimmune"],
    "radiologist": ["radiologist", "imaging", "radiology"],
    "nephrologist": ["nephrologist", "renal"],
    "allergist": ["allergist", "immunologist", "allergy"],
    "surgeon": ["surgeon", "surgery"],
}


def get_hospitals(
    location: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    specialization: str = "hospital",
) -> dict:
    try:
        keywords = _SPECIALTY_KEYWORDS.get(specialization, ["hospital"])

        if location:
            try:
                geo = _geo.geocode(location)
                if not geo:
                    return {"error": "Invalid location — could not geocode."}
                lat, lng = geo.latitude, geo.longitude
            except RequestException as exc:
                return {"error": f"Geocoding failed: {exc}"}
        elif latitude is not None and longitude is not None:
            lat, lng = latitude, longitude
        else:
            return {"error": "Provide either a location name or GPS coordinates."}

        seen: set[str] = set()
        hospitals: list[dict] = []
        for keyword in keywords:
            for place in gmaps.places_nearby(
                location=(lat, lng), radius=5000, type="hospital", keyword=keyword
            ).get("results", []):
                name = place["name"]
                if name not in seen:
                    seen.add(name)
                    hospitals.append({
                        "name": name,
                        "address": place.get("vicinity", ""),
                        "rating": place.get("rating", "N/A"),
                        "reviews": place.get("user_ratings_total", 0),
                    })

        return {"hospitals": hospitals}
    except Exception as exc:
        return {"error": str(exc)}


def send_confirmation_email(
    to_email: str, user_name: str, hospital: str, slot: str
) -> None:
    if not _SENDER_EMAIL or not _SENDER_PASSWORD:
        return
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(_SENDER_EMAIL, _SENDER_PASSWORD)
            server.sendmail(
                _SENDER_EMAIL,
                to_email,
                (
                    f"Subject: Appointment Confirmation — CareReach\n\n"
                    f"Hi {user_name},\n\n"
                    f"Your appointment at {hospital} is confirmed for {slot}.\n\n"
                    f"Thank you for using CareReach."
                ),
            )
    except Exception:
        pass  # email is optional; never surface this to the user
```

- [ ] **Step 2: Commit**

```powershell
git add src/hospital.py
git commit -m "refactor: add src/hospital.py with Maps search and optional email"
```

---

## Task 5: src/auth.py — login/signup UI

**Files:**
- Create: `src/auth.py`

- [ ] **Step 1: Write src/auth.py**

```python
import streamlit as st

from src.db import authenticate_user, add_user


def show_login() -> None:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password.")


def show_signup() -> None:
    st.title("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if not username or not password:
            st.warning("Please fill out all fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        elif add_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Username already exists. Please choose another.")
```

- [ ] **Step 2: Commit**

```powershell
git add src/auth.py
git commit -m "refactor: add src/auth.py with login and signup UI"
```

---

## Task 6: src/pages/ — chatbot, appointment, history

**Files:**
- Create: `src/pages/__init__.py`
- Create: `src/pages/chatbot.py`
- Create: `src/pages/appointment.py`
- Create: `src/pages/history.py`

- [ ] **Step 1: Create src/pages/__init__.py** (empty file)

- [ ] **Step 2: Write src/pages/chatbot.py**

```python
import os
import time

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

from src.db import save_history

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_AI_API_KEY"])

_MODEL = "gemini-1.5-flash"
_AI_AVATAR = "✨"


def show(username: str) -> None:
    st.subheader("Symptom Checker 🩺")
    st.caption("Describe your symptoms and get an AI-powered analysis. Not a substitute for professional medical advice.")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "gemini_history" not in st.session_state:
        st.session_state.gemini_history = []

    model = genai.GenerativeModel(_MODEL)
    chat = model.start_chat(history=st.session_state.gemini_history)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=msg.get("avatar")):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Describe your symptoms…"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = chat.send_message(prompt, stream=True)

        with st.chat_message("ai", avatar=_AI_AVATAR):
            placeholder = st.empty()
            full = ""
            for chunk in response:
                for word in chunk.text.split(" "):
                    full += word + " "
                    time.sleep(0.04)
                    placeholder.write(full + "▌")
            placeholder.write(full.strip())

        st.session_state.messages.append(
            {"role": "ai", "content": full.strip(), "avatar": _AI_AVATAR}
        )
        st.session_state.gemini_history = chat.history
        save_history(username, symptoms=prompt, analysis=full)
```

- [ ] **Step 3: Write src/pages/appointment.py**

```python
import streamlit as st
import pandas as pd
from streamlit_js_eval import streamlit_js_eval

from src.db import save_appointment
from src.hospital import get_hospitals, send_confirmation_email

_SPECIALTIES = [
    "General Physician", "neurologist", "dermatologist", "cardiologist",
    "orthopedist", "pediatrician", "gynecologist", "psychiatrist", "dentist",
    "oncologist", "endocrinologist", "ophthalmologist", "urologist",
    "gastroenterologist", "pulmonologist", "ent", "rheumatologist",
    "radiologist", "nephrologist", "allergist", "surgeon",
]


def _table(hospitals: list[dict], show_all: bool) -> None:
    rows = hospitals if show_all else hospitals[:5]
    for i, h in enumerate(rows, 1):
        h["#"] = i
        if isinstance(h.get("rating"), float):
            h["rating"] = f"{h['rating']:.1f}"
    st.table(pd.DataFrame(rows).set_index("#"))


def _confirm(hospitals: list[dict], specialist: str, date, appt_time, username: str) -> None:
    names = [h["name"] for h in hospitals]
    hospital = st.selectbox("Select a Hospital 🏥", names)
    if st.button("Confirm Appointment ✅"):
        save_appointment(username, specialist, str(date), str(appt_time), hospital)
        send_confirmation_email(
            to_email="",  # no email collected from user in this flow
            user_name=username,
            hospital=hospital,
            slot=f"{date} {appt_time}",
        )
        st.success(
            f"Appointment booked with **{specialist}** on **{date}** at **{appt_time}** "
            f"at **{hospital}**."
        )


def show(username: str) -> None:
    st.subheader("Book Appointment 📅")

    specialist = st.selectbox("Specialist 🩺", _SPECIALTIES)
    date = st.date_input("Date 📅")
    appt_time = st.time_input("Time ⏰")
    show_all = st.checkbox("Show all hospitals (default: top 5)")

    mode = st.radio("Location", ["Enter Place Name", "Use Current Location"])

    if mode == "Enter Place Name":
        place = st.text_input("Place or city name")
        if st.button("Find Hospitals"):
            if not place:
                st.warning("Please enter a place name.")
                return
            with st.spinner("Searching nearby hospitals…"):
                result = get_hospitals(location=place, specialization=specialist)
            if "error" in result:
                st.warning(result["error"])
            elif not result.get("hospitals"):
                st.warning("No hospitals found for that location and specialty.")
            else:
                _table(result["hospitals"], show_all)
                _confirm(result["hospitals"], specialist, date, appt_time, username)

    else:
        coords = streamlit_js_eval(
            js_expressions="navigator.geolocation.getCurrentPosition((pos) => pos.coords)",
            want_output=True,
        )
        if coords:
            st.success(f"Location: {coords['latitude']:.4f}, {coords['longitude']:.4f}")
            st.map([{"lat": coords["latitude"], "lon": coords["longitude"]}])
            with st.spinner("Searching nearby hospitals…"):
                result = get_hospitals(
                    latitude=coords["latitude"],
                    longitude=coords["longitude"],
                    specialization=specialist,
                )
            if "error" in result:
                st.warning(result["error"])
            elif not result.get("hospitals"):
                st.warning("No hospitals found nearby.")
            else:
                _table(result["hospitals"], show_all)
                _confirm(result["hospitals"], specialist, date, appt_time, username)
        else:
            st.info("Allow location access in your browser, then this page will reload.")
```

- [ ] **Step 4: Write src/pages/history.py**

```python
import streamlit as st

from src.db import fetch_history


def show(username: str) -> None:
    st.subheader("Health History 📋")
    records = fetch_history(username)

    if not records:
        st.info("No history yet. Use the Symptom Checker to get started.")
        return

    for symptoms, analysis, timestamp in records:
        with st.container(border=True):
            st.write(f"**Symptoms:** {symptoms}")
            st.write(f"**Status:** {analysis}")
            st.caption(f"🕐 {timestamp}")
```

- [ ] **Step 5: Commit**

```powershell
git add src/pages/
git commit -m "refactor: add src/pages (chatbot, appointment, history)"
```

---

## Task 7: app.py — Streamlit entrypoint

**Files:**
- Create: `app.py`

- [ ] **Step 1: Write app.py**

```python
import streamlit as st

from src.db import init_db
from src.auth import show_login, show_signup
from src.pages import chatbot, appointment, history

_SIDEBAR_MD = """
## CareReach 🏥

AI-powered telemedicine for remote consultations.

---
- 🩺 **Symptom Checker** — describe symptoms, get analysis
- 📅 **Book Appointment** — find hospitals near you
- 📋 **Health History** — review past consultations

---
*Not a substitute for professional medical advice.*
"""


def main() -> None:
    st.set_page_config(
        page_title="CareReach",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_db()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None

    st.sidebar.markdown(_SIDEBAR_MD)

    if st.session_state.logged_in:
        st.sidebar.write(f"👤 **{st.session_state.username}**")
        page = st.sidebar.selectbox(
            "Navigate",
            ["Symptom Checker", "Book Appointment", "Health History"],
        )
        if st.sidebar.button("Logout", use_container_width=True):
            for key in ("logged_in", "username", "messages", "gemini_history"):
                st.session_state.pop(key, None)
            st.rerun()

        st.title(f"Welcome back, {st.session_state.username}! 👋")

        if page == "Symptom Checker":
            chatbot.show(st.session_state.username)
        elif page == "Book Appointment":
            appointment.show(st.session_state.username)
        elif page == "Health History":
            history.show(st.session_state.username)
    else:
        page = st.sidebar.radio("Account", ["Login", "Sign Up"])
        if page == "Login":
            show_login()
        else:
            show_signup()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```powershell
git add app.py
git commit -m "refactor: add app.py entrypoint with routing and sidebar"
```

---

## Task 8: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Write README.md**

```markdown
# CareReach

AI-powered telemedicine platform for remote healthcare consultations.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red)](https://streamlit.io)

## Features

| Feature | Description |
|---|---|
| **Symptom Checker** | Chat with Google Gemini 1.5 Flash about your symptoms |
| **Hospital Finder** | Search nearby hospitals by specialist type via Google Maps |
| **Appointment Booking** | Pick a date, time, specialist, and hospital |
| **Health History** | Review all past symptom conversations |
| **Auth** | Secure signup/login with bcrypt-hashed passwords |

## Setup

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — `winget install astral-sh.uv` or `pip install uv`
- [Google Gemini API key](https://aistudio.google.com/) (free tier available)
- [Google Maps Platform API key](https://console.cloud.google.com/) — enable **Places API**

### Install

```bash
git clone <repo-url>
cd CareReach
uv sync
```

### Configure

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```env
GOOGLE_AI_API_KEY=your_gemini_api_key
GOOGLE_MAPS_API_KEY=your_maps_api_key
# Optional — only needed for appointment confirmation emails:
SENDER_EMAIL=your_gmail@gmail.com
SENDER_PASSWORD=your_gmail_app_password
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
GOOGLE_AI_API_KEY = "your_gemini_api_key"
GOOGLE_MAPS_API_KEY = "your_maps_api_key"
```

5. Click **Deploy** — done.

## Project Structure

```
.
├── app.py                  # Streamlit entrypoint
├── src/
│   ├── auth.py             # Login/signup UI
│   ├── db.py               # SQLite helpers (users, history, appointments)
│   ├── hospital.py         # Google Maps hospital search + optional email
│   └── pages/
│       ├── chatbot.py      # Gemini symptom checker
│       ├── appointment.py  # Hospital finder + booking
│       └── history.py      # Health history viewer
├── .streamlit/
│   └── config.toml         # Dark theme
├── .env.example            # Secrets template
├── pyproject.toml          # uv project config
└── uv.lock                 # Locked dependencies
```

## Secrets Reference

| Key | Required | Description |
|---|---|---|
| `GOOGLE_AI_API_KEY` | Yes | Gemini API key from Google AI Studio |
| `GOOGLE_MAPS_API_KEY` | Yes | Google Maps Platform key with Places API enabled |
| `SENDER_EMAIL` | No | Gmail address for appointment confirmation emails |
| `SENDER_PASSWORD` | No | Gmail App Password (not your regular password) |

## License

Apache 2.0 — see [LICENSE](LICENSE).
```

- [ ] **Step 2: Commit**

```powershell
git add README.md
git commit -m "docs: rewrite README for CareReach with setup and deploy instructions"
```

---

## Task 9: Delete old files + final commit

**Files:**
- Delete: `app_fin.py`, `common_utils.py`, `hospital_utils.py`
- Delete: `requirements.txt`, `install_requirements.ps1`, `install_extensions.ps1`, `extensions.txt`
- Delete: `Tantrostav.code-workspace`, `Tantrostav Hackathon.zip`
- Delete: `trash/` directory
- Delete: `data/Tantrostav/` directory

- [ ] **Step 1: Delete replaced source files**

```powershell
Remove-Item "app_fin.py", "common_utils.py", "hospital_utils.py"
Remove-Item "requirements.txt", "install_requirements.ps1", "install_extensions.ps1", "extensions.txt"
Remove-Item "Tantrostav.code-workspace"
if (Test-Path "Tantrostav Hackathon.zip") { Remove-Item "Tantrostav Hackathon.zip" }
```

- [ ] **Step 2: Delete old directories**

```powershell
Remove-Item -Recurse -Force "trash"
Remove-Item -Recurse -Force "data\Tantrostav"
```

- [ ] **Step 3: Verify app starts**

```powershell
uv run streamlit run app.py --server.headless true &
Start-Sleep 5
# Should print: "You can now view your Streamlit app in your browser."
# Ctrl+C to stop
```

- [ ] **Step 4: Final commit**

```powershell
git add -A
git commit -m "chore: remove all legacy hackathon files, project is now CareReach"
```

---

## Secrets Summary (add these to Streamlit Cloud)

| Secret | Where to get it |
|---|---|
| `GOOGLE_AI_API_KEY` | https://aistudio.google.com/ → Get API key |
| `GOOGLE_MAPS_API_KEY` | https://console.cloud.google.com/ → APIs & Services → Enable Places API → Credentials |
| `SENDER_EMAIL` *(optional)* | Your Gmail address |
| `SENDER_PASSWORD` *(optional)* | https://myaccount.google.com/apppasswords |
