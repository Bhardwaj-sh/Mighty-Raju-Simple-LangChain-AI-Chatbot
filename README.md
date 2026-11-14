# ⚡ Mighty Raju – Premium AI Chatbot

A modern, glassmorphic AI chatbot web application powered by **Streamlit**, **LangChain**, and **Google Gemini API**.

---

## 🌟 Features

- **⚡ Mighty Raju Identity**: Official branding, transparent character mascot with gentle idle breathing and blinking animations.
- **🎨 Glassmorphic UI/UX**: Soft pastel gradient aesthetics with frosted glass card styling inspired by modern AI apps.
- **💬 Real-Time Streaming**: Live token-by-token streaming with typing indicators and distinct message bubble styling.
- **🧠 Multi-Turn Conversation Memory**: Preserves context across multiple interaction turns using LangChain.
- **🔍 Full Search**: Search across all previous conversation titles and message content.
- **🔖 Saved Chats (Bookmarks)**: 1-click bookmarking of important conversations.
- **📁 Projects & Folders**: Organize and categorize conversations into custom projects.
- **🕒 Dynamic Recent Chats**: Auto-generated conversation titles and quick switching.
- **💾 Local SQLite Persistence**: Seamless local storage for conversations, messages, and projects without third-party database dependencies.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Orchestration**: [LangChain](https://www.langchain.com/) (`langchain`, `langchain-core`, `langchain-google-genai`)
- **AI Model**: Google Gemini (`gemini-3.5-flash`)
- **Database**: SQLite
- **Environment**: Python 3.10+ & `python-dotenv`

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Bhardwaj-sh/Mighty-Raju-Simple-LangChain-AI-Chatbot.git
cd Mighty-Raju-Simple-LangChain-AI-Chatbot
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your Google Gemini API key to `.env`:
```dotenv
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Launch the Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```text
├── assets/
│   ├── mighty_raju.jpg
│   ├── mighty_raju_transparent.png
│   ├── mighty_raju_avatar.png
│   └── mighty_raju_avatar_transparent.png
├── .env.example
├── .gitignore
├── app.py
├── database.py
├── requirements.txt
└── README.md
```

---

## 🛡️ License
MIT License
