# 🏆 Digital Debate Judge

A modern **Flask + SQLite web application** for organizing and judging debates.  
Built with a clean **glassmorphism UI** (Bootstrap + custom CSS) and features for participant registration, scoring by judges, and live results.

---

## ✨ Features
- 📝 **Register Participants** with their name and debate topic.  
- 🎤 **Judge Panel** where judges can assign scores (0–100).  
- 📊 **Results Leaderboard** with participants ranked by score.  
- 🗑️ **Delete Participants** when needed.  
- 🌈 **Modern UI** with animated gradients, glassmorphism cards, and responsive design.  

---

## 📂 Project Structure
```bash
digital-debate-judge/
│
├── app.py # Main Flask app
├── debate.db # SQLite database (auto-created)
├── templates/ # HTML templates
│ ├── home.html
│ ├── register.html
│ ├── judge_panel.html
│ └── results.html
└── static/ # (Optional) for images, css, js if needed
```
## 🌐 Usage

Home Page (/) → Navigate between panels.

Register Page (/register) → Add participants.

Judge Panel (/judge) → Select a participant and assign a score.

Results Page (/results) → View leaderboard, delete participants.

## 🛠️ Tech Stack

Backend: Python, Flask

Database: SQLite

Frontend: HTML, Bootstrap 5, CSS (glassmorphism), Typed.js

## 🔒 Security Notes

Currently, delete actions are done via GET. For production, convert them to POST requests with CSRF protection.

Input validation is basic; consider stricter checks for production use.
