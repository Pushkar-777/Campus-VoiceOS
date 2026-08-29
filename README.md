# 🎙️ Campus VoiceOS

## AI-Powered Voice Assistant for Campus Information

Campus VoiceOS is an AI-powered voice assistant designed to help students quickly access important campus information using **voice or text queries**.

Students can simply ask questions about the library, hostel, canteen, placements, medical facilities, Wi-Fi, transport, labs, sports and other campus services.

---

## 🚀 Features

- 🎙️ Voice Input
- 🧠 Speech-to-Text using AssemblyAI
- 🔎 Smart Campus Information Search
- ⌨️ Text-based Queries
- ⚡ Quick Campus Search
- 💡 Suggested Questions
- 🔊 Voice Response
- 🕘 Recent Questions
- 💾 Browser-based Search History
- 🟢 Backend Health Monitoring
- 📊 Campus Categories & Statistics
- 📱 Responsive User Interface

---

## 🏫 Campus Services

Campus VoiceOS currently supports information related to:

- 📚 Library
- 🍽️ Canteen
- 🏠 Hostel
- 💼 Placements
- 🏥 Medical Facilities
- ⚽ Sports
- 💳 Fees
- 📶 Campus Wi-Fi
- 🚌 Transport
- 💻 Computer Labs
- 🎉 Campus Events
- 🚨 Emergency Information
- 🛡️ Campus Security

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- MediaRecorder API
- Web Speech Synthesis API

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### AI / Speech
- AssemblyAI Speech-to-Text API

### Data
- JSON-based Campus Knowledge Base

---

## ⚙️ System Architecture

```text
                Student
                   │
                   ▼
          Voice / Text Query
                   │
          ┌────────┴────────┐
          │                 │
       Voice             Text
          │                 │
          ▼                 │
     AssemblyAI             │
    Speech-to-Text          │
          │                 │
          └────────┬────────┘
                   ▼
            FastAPI Backend
                   │
                   ▼
          Smart Campus Search
                   │
                   ▼
          Campus Knowledge Base
             (JSON Data)
                   │
                   ▼
            Relevant Answer
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
       Text UI          Voice Response
```

---

## 📁 Project Structure

```text
Campus-VoiceOS/
│
├── backend/
│   └── app.py
│
├── frontend/
│   └── index.html
│
├── data/
│   └── campus_data.json
│
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | System health status |
| GET | `/categories` | Available campus categories |
| GET | `/stats` | Campus information statistics |
| POST | `/query` | Search campus information |
| POST | `/transcribe` | Convert audio to text |

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Pushkar-777/Campus-VoiceOS.git
```

```bash
cd Campus-VoiceOS
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install fastapi uvicorn assemblyai python-dotenv python-multipart
```

---

## 🔐 AssemblyAI API Key

Create a `.env` file and add your AssemblyAI API key:

```env
ASSEMBLYAI_API_KEY=your_api_key_here
```

**Never upload your real API key to GitHub.**

The `.gitignore` file already excludes `.env`.

---

## ▶️ Run Backend

From the project root:

```bash
uvicorn backend.app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🌐 Run Frontend

Open another terminal:

```bash
cd frontend
```

Then:

```bash
python -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500
```

---

## 🎤 Example Questions

Try asking:

```text
What are the library timings?
```

```text
Where is the medical center?
```

```text
Where is the placement office?
```

```text
How can I access campus Wi-Fi?
```

```text
Where are the computer labs?
```

```text
What transport facilities are available?
```

```text
What sports facilities are available on campus?
```

---

## 🔊 Voice Interaction

Campus VoiceOS supports a complete voice interaction flow:

```text
Speak
  ↓
AssemblyAI
  ↓
Speech converted to text
  ↓
Campus information search
  ↓
Answer displayed
  ↓
Answer can be spoken aloud
```

---

## 🔒 Security

Sensitive credentials such as API keys are stored using environment variables.

The following files are excluded from Git:

```text
.env
.venv/
__pycache__/
*.pyc
.vscode/
```

---

## 🌟 Future Improvements

- 🤖 Advanced conversational AI
- 🌐 Multilingual voice support
- 📢 Real-time campus announcements
- 📅 Event and timetable integration
- 👨‍🎓 Student authentication
- 🛠️ Admin dashboard
- 🗄️ Database integration
- ☁️ Cloud deployment
- 📍 Campus navigation assistance

---

## 🎯 Project Goal

The goal of Campus VoiceOS is to make campus information **faster, easier and more accessible** by providing students with a simple voice-first interface.

Instead of searching through multiple sources, students can simply **ask Campus VoiceOS**.

---

## 👨‍💻 Developer

### Pushkar Srivastava

GitHub:  
https://github.com/Pushkar-777

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

**Built with Python, FastAPI, JavaScript and AssemblyAI. 🎙️🚀**
