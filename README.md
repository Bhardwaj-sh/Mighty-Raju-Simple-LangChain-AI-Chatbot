# ⚡ MightyRaju AI Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Orchestration-orange.svg)](https://www.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI%20Engine-8E75C4.svg)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent, superhero-themed conversational AI web application built with **Streamlit**, **LangChain**, and the **Google Gemini API**, featuring persistent chat history powered by **SQLite**. Designed with a modern, glassmorphic UI and character identity inspired by *Mighty Raju*.

---

## 📖 1. Project Overview

**MightyRaju AI Chatbot** is a production-ready conversational AI assistant crafted to deliver lightning-fast responses, contextual multi-turn dialogue, and structured knowledge organization.

Designed to showcase practical full-stack AI development, this project combines:
- A custom glassmorphic front-end built natively with Streamlit and tailored CSS tokens.
- LangChain orchestration leveraging Google Gemini's high-speed Flash-Lite model for responsive streaming responses.
- A zero-configuration local SQLite persistence layer for session recall, conversation management, project categorization, and full-text keyword search.

---

## ✨ 2. Key Features

- **⚡ Character Persona & Identity**: Distinct superhero-themed persona embodying Mighty Raju's sharp, fearless, and respectful tone with transparent custom character assets.
- **🎨 Glassmorphic Superhero Design**: Polished design system featuring coral gradients, custom cards, sleek typography (`Plus Jakarta Sans`), and animated hero banners.
- **💬 Token-by-Token Streaming**: Live, low-latency streaming responses with dynamic typing indicators and clean error boundaries.
- **🧠 Multi-Turn Conversational Memory**: Full conversation context maintained across interaction turns using LangChain message representations (`SystemMessage`, `HumanMessage`, `AIMessage`).
- **💾 Local SQLite Persistence**: Automatic database initialization on first run with complete storage for chats, messages, and projects.
- **📁 Projects & Folders**: Categorize, organize, and filter conversations by custom project folders.
- **🔖 Bookmark & Saved Chats**: One-click conversation bookmarking for quick reference to important answers.
- **🔍 Full-Text Conversation Search**: Live keyword search across both chat titles and message contents.
- **🕒 Dynamic Recent Chats**: Automated title generation from user prompts, timestamp tracking, and single-click chat switching.
- **🔒 Enterprise-Grade Privacy & Security**: Zero client credentials in code; keys are dynamically loaded via `.env` or Streamlit Secrets, with automated database exclusion from Git.

---

## 🛠️ 3. Technologies Used

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | [Streamlit](https://streamlit.io/) (v1.35+) | Interactive web UI, reactive session state, and streaming widgets |
| **AI Orchestration** | [LangChain](https://www.langchain.com/) | Prompt structuring, message schema, and model streaming pipeline |
| **Foundation Model** | [Google Gemini](https://aistudio.google.com/) | High-speed generative AI processing (`gemini-3.5-flash-lite`) |
| **Storage & Persistence** | SQLite3 | Embedded SQL database for conversations, messages, and project metadata |
| **Environment & Config** | `python-dotenv` & `st.secrets` | Secure, dual-mode credential and environment variable management |
| **Language Runtime** | Python 3.10+ | Core application logic and async I/O handling |

---

## 📂 4. Project Folder Structure

```text
MightyRaju-AI-Chatbot/
│
├── assets/                                 # Static UI media & branding
│   ├── mighty_raju_transparent.png         # Main welcome hero character mascot
│   └── mighty_raju_avatar_transparent.png  # Circular branding logo & assistant avatar
│
├── .env.example                            # Template for environment variables (safe for Git)
├── .gitignore                              # Comprehensive ignore rules (.venv, .env, *.db, cache)
├── app.py                                  # Core Streamlit application, UI layout, & LangChain pipeline
├── database.py                             # SQLite data access layer (CRUD operations & indexes)
├── requirements.txt                        # Clean, minimal production dependencies
└── README.md                               # Project documentation
```

---

## ⚙️ 5. Installation Instructions

Follow these step-by-step instructions to set up and run the MightyRaju AI Chatbot on your local system.

### Prerequisites

- **Python**: Version 3.10 or higher installed ([Download Python](https://www.python.org/downloads/))
- **Git**: Installed on your operating system ([Download Git](https://git-scm.com/))
- **Google Gemini API Key**: Free API key from [Google AI Studio](https://aistudio.google.com/)

### Clone the Repository

```bash
git clone https://github.com/Bhardwaj-sh/MightyRaju-AI-Chatbot.git
cd MightyRaju-AI-Chatbot
```

---

## 🐍 6. Virtual Environment Setup

Isolate project dependencies by creating a dedicated virtual environment:

### On Windows (Command Prompt or PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*(If running PowerShell and script execution is disabled, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### On macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 📦 7. Dependency Installation

With the virtual environment activated, install the required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔑 8. Gemini API Key Configuration

1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/).
2. Create a `.env` file in the project root directory by copying `.env.example`:

```bash
# On Windows PowerShell:
Copy-Item .env.example .env

# On macOS/Linux:
cp .env.example .env
```

3. Open `.env` in your text editor and insert your API key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

> **Security Note:** The `.env` file is strictly ignored by `.gitignore` and will never be tracked or committed to GitHub.

---

## 🚀 9. Running the Streamlit Application

Start the local Streamlit development server:

```bash
streamlit run app.py
```

The application will launch automatically in your default browser at:
```text
http://localhost:8501
```

To run with auto-reload enabled during development:
```bash
streamlit run app.py --server.runOnSave true
```

---

## 📸 10. Screenshots

| Main Welcome Screen | Multi-Turn Live Chat |
| :---: | :---: |
| ![Welcome Hero Screen](https://via.placeholder.com/600x380/BA0001/FFFFFF?text=Mighty+Raju+Welcome+Screen) | ![Live Streaming Chat](https://via.placeholder.com/600x380/1E293B/FFFFFF?text=Live+Streaming+Conversation) |

| Project & Chat Management | Sidebar Navigation |
| :---: | :---: |
| ![Project Organization](https://via.placeholder.com/600x380/7F1D1D/FFFFFF?text=Projects+%26+Saved+Chats) | ![Sidebar Navigation](https://via.placeholder.com/600x380/334155/FFFFFF?text=Sidebar+Recent+Chats) |

*(Note: Replace placeholder images with actual screenshots from your running deployment).*

---

## 🔮 11. Future Improvements

- [ ] **Voice Input & Speech-to-Text (STT)**: Integration with Web Speech API for voice interactions.
- [ ] **Multimodal Vision Support**: Support image uploads and document analysis using Gemini Vision capabilities.
- [ ] **Export & Share Conversations**: Download chat logs in Markdown, PDF, or JSON format.
- [ ] **User Authentication**: Support multi-user accounts via OAuth2 / Streamlit-Authenticator.
- [ ] **Vector Database Search (RAG)**: Retrieval-Augmented Generation on custom uploaded PDFs and documents using ChromaDB or FAISS.

---

## 🛡️ 12. Security & Compliance

- **No Hardcoded Keys**: API keys are accessed through environment variables or secure platform secret managers.
- **Private Data Protection**: Local SQLite database files (`*.db`) containing user conversation records are excluded from source control.
- **Error Sanitization**: API errors caught at runtime automatically mask sensitive key strings before displaying error notices.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
