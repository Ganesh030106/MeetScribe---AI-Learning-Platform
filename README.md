# MeetScribe 🎙️ — AI Meeting Analysis Platform

> Upload a meeting video and get instant AI-powered summaries, action items, and sentiment analysis — powered by Google Gemini 2.5 Flash.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Render-4f46e5?style=for-the-badge)](https://meetscribe---ai-learning-platform.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![Gemini](https://img.shields.io/badge/Gemini_2.5-Flash-4285f4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎬 **Video Upload** | Drag & drop or browse to upload meeting recordings (.mp4, .mov, .avi, .webm) |
| 📋 **Smart Summary** | AI generates a concise paragraph summarizing the meeting's purpose, discussions, and outcomes |
| ✅ **Action Items** | Automatically extracts tasks, assigns owners, and identifies deadlines |
| 💬 **Sentiment Analysis** | Analyzes team mood and tone — collaborative, concerned, optimistic, etc. |
| 🔑 **Bring Your Own Key** | Users provide their own Gemini API key — no server secrets needed |
| 🔒 **Privacy First** | API keys are stored only in your browser (localStorage), never on the server |
| 🧾 **Raw JSON Output** | View the complete structured JSON response from Gemini |

---

## 🖥️ Screenshots

### Landing Page
The dark-themed UI with API key input and video upload area:

![MeetScribe UI](https://github.com/user-attachments/assets/meetscribe-ui-placeholder)

---

## 🚀 Live Demo

**[https://meetscribe---ai-learning-platform.onrender.com](https://meetscribe---ai-learning-platform.onrender.com)**

> **Note:** Free tier on Render may take ~30 seconds to wake up on first visit after inactivity.

### How to Use:
1. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Paste your API key and click **Verify**
3. Upload a meeting video
4. Click **✨ Analyze Meeting** and wait for results

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **AI Engine** | Google Gemini 2.5 Flash (Multimodal) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Production Server** | Gunicorn |
| **Hosting** | Render |

---

## 📂 Project Structure

```
MeetScribe---AI-Learning-Platform/
├── app.py                  # Flask backend — routes, Gemini API integration
├── templates/
│   └── index.html          # Frontend UI (dark glassmorphism theme)
├── uploads/                # Temporary video storage (auto-cleaned)
├── requirements.txt        # Python dependencies
├── Procfile                # Production server command
├── render.yaml             # Render deployment config
├── server.js               # Node.js code showcase server
├── views/                  # EJS templates for Node showcase
│   ├── index.ejs
│   └── image.ejs
├── chat.js                 # Gemini chat demo script
├── stream.js               # Gemini streaming demo script
├── gemini-pro-vision.js    # Gemini vision demo script
├── imageGenerate.js        # Gemini image generation demo
├── start.js                # Gemini text generation demo
└── README.md
```

---

## ⚙️ Local Development

### Prerequisites
- Python 3.11+
- A [Gemini API Key](https://aistudio.google.com/apikey) (free)

### Setup

```bash
# Clone the repository
git clone https://github.com/Ganesh030106/MeetScribe---AI-Learning-Platform.git
cd MeetScribe---AI-Learning-Platform

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Open **http://localhost:5000** in your browser, paste your Gemini API key, and start analyzing!

---

## 🌐 Deploy Your Own

### Render (Recommended — Free)

1. Fork this repository
2. Go to [render.com](https://render.com) → **New+ → Web Service**
3. Connect your GitHub repo
4. Configure:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 600`
5. Select **Free** instance → **Create Web Service**

> ⚠️ The `--timeout 600` flag is critical — video processing can take several minutes.

---

## 🔐 Security & Privacy

- **No server-side secrets** — users bring their own Gemini API key
- **Keys stay in the browser** — stored in `localStorage`, sent per-request only
- **Keys are never logged** — the server uses the key for that request and discards it
- **Uploaded videos are auto-deleted** — cleaned from both local storage and Gemini's servers after processing

---

## 🧠 How It Works

```
User uploads video → Flask saves it temporarily
                   → Uploads to Gemini File API
                   → Waits for processing (ACTIVE state)
                   → Sends video + analysis prompt to Gemini 2.5 Flash
                   → Receives structured JSON (summary, actions, sentiment)
                   → Returns results to frontend
                   → Cleans up local + remote files
```

### The AI Prompt
MeetScribe uses a carefully crafted system prompt that instructs Gemini to:
- Analyze spoken words, tone of voice, and visible slides
- Return a **clean JSON object** with `summary`, `action_items`, and `sentiment`
- Extract task owners and deadlines (defaulting to "Unassigned" / "Not specified")

---

## 📜 Additional Scripts

This repo also includes standalone Gemini API learning scripts:

| Script | Description |
|--------|-------------|
| `start.js` | Basic text generation with Gemini |
| `chat.js` | Interactive terminal chatbot |
| `stream.js` | Streaming chat responses |
| `gemini-pro-vision.js` | Image analysis with Gemini Vision |
| `imageGenerate.js` | AI image generation |

Run any script with: `node <script-name>.js` (requires `npm install` and a `.env` file with your key)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Star ⭐ the repo if you find it useful

---

## 📄 License

This project is open source under the [ISC License](LICENSE).

---

<div align="center">

**Built with ❤️ using Google Gemini AI**

[⬆ Back to Top](#meetscribe-️--ai-meeting-analysis-platform)

</div>