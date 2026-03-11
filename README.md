# 🤖 Fully Featured Chatbot

> 🌍 A multilingual, voice-enabled PDF chatbot — query your documents in **English** or **Kiswahili** with real-time, streamed AI responses.

---

## ✨ Features

| | Feature | Description |
|---|---------|-------------|
| 📄 | **PDF Q&A** | Upload and query any PDF document using natural language |
| 🌍 | **Multilingual** | Full support for English and Kiswahili |
| 🎙️ | **Voice Input** | Speak your queries in English via the microphone |
| 🔊 | **Text-to-Speech** | Hear responses read aloud |
| ⚡ | **Real-time Streaming** | Token-by-token WebSocket responses for low latency |
| 🧠 | **RAG Architecture** | Answers are grounded in your document, not hallucinated |
| 💬 | **Feedback System** | Built-in feedback page to rate responses |

---

## 🗂️ Project Structure

```
📦 fully_featured_chatbot/
├── 📁 src/
│   ├── 📁 english_governance_chatbot/   # 🇬🇧 English PDF Q&A module
│   ├── 📁 kiswahili/                    # 🇰🇪 Kiswahili language module
│   ├── 🐍 __init__.py
│   ├── 🌐 index.html                    # Main English chat interface
│   ├── 🌐 kiswahili.html                # Kiswahili chat interface
│   ├── 🌐 feedback.html                 # User feedback page
│   ├── 🐍 query_llm.py                  # RAG pipeline & LLM query logic
│   ├── 🐍 speech_recognition.py         # 🎙️ Speech-to-text processing
│   └── 🐍 text_to_speech.py             # 🔊 Text-to-speech output
├── 🐍 llm_response_websocket.py         # ⚡ WebSocket server — LLM responses
├── 🐍 speech_recognition_websocket.py   # 🎙️ WebSocket server — speech input
├── 📄 requirements.txt
└── 📖 README.md
```

---

## 🚀 Getting Started

### 🧰 Prerequisites

- 🐍 Python 3.8+
- 📦 pip

### ⚙️ Installation

**1️⃣ Clone the repository**
```bash
git clone https://github.com/Musagen12/fully_featured_chatbot.git
cd fully_featured_chatbot
```

**2️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

### ▶️ Running the App

🧠 Start the LLM response WebSocket server:
```bash
python llm_response_websocket.py
```

🎙️ Start the speech recognition WebSocket server:
```bash
python speech_recognition_websocket.py
```

🌐 Then open `src/index.html` (English) or `src/kiswahili.html` (Kiswahili) in your browser.

---

## 💬 Usage

| Step | Action |
|------|--------|
| 1️⃣ | 📤 Upload a PDF document through the interface |
| 2️⃣ | 🌍 Choose your language — **English** or **Kiswahili** |
| 3️⃣ | ⌨️ Type your question **or** 🎙️ use voice input (English only) |
| 4️⃣ | ⚡ Receive a streamed, document-grounded response |
| 5️⃣ | 🔊 Optionally listen to the response read aloud |

---

## 🌐 Supported Languages

| 🌍 Language | ⌨️ Text Input | 🎙️ Voice Input | 🔊 Text-to-Speech |
|------------|:------------:|:--------------:|:-----------------:|
| 🇬🇧 English   | ✅ | ✅ | ✅ |
| 🇰🇪 Kiswahili | ✅ | ❌ | ✅ |

---

## 🏗️ How It Works

The chatbot uses a **Retrieval-Augmented Generation (RAG)** pipeline — it retrieves the most relevant chunks from your PDF before asking the LLM to generate an answer, keeping responses accurate and grounded.

```
┌──────────────────────────────────────────────────────────┐
│  🌐 Browser (Frontend)                                   │
│  index.html  /  kiswahili.html  /  feedback.html        │
└──────────────┬──────────────────────┬────────────────────┘
               │ 💬 Text Query        │ 🎙️ Audio Stream
               ▼                      ▼
┌──────────────────────┐  ┌───────────────────────────────┐
│ ⚡ llm_response_     │  │ 🎙️ speech_recognition_        │
│   websocket.py       │  │    websocket.py               │
│  (Port 8765)         │  │   (Port 8766)                 │
└────────┬─────────────┘  └────────────┬──────────────────┘
         │                             │ 📝 Transcribed Text
         │ ◄───────────────────────────┘
         ▼
┌──────────────────────┐
│ 🧠 query_llm.py      │  ← 🔍 Semantic search over PDF chunks
│   (RAG Pipeline)     │  ← 📝 Prompt construction
└────────┬─────────────┘
         │
         ▼
┌────────────────────────────────────────────┐
│ 🇬🇧 english_governance_chatbot/            │
│ 🇰🇪 kiswahili/                             │
│    Language-specific retrieval & prompts   │
└────────────────────────────────────────────┘
```

**🔄 Step-by-step flow:**

| # | Step | Description |
|---|------|-------------|
| 1️⃣ | 📥 **PDF Ingestion** | Documents are chunked, embedded, and stored in a vector index |
| 2️⃣ | 💬 **Query** | User submits a question via text or voice |
| 3️⃣ | 🎙️ **Speech-to-Text** | Audio is transcribed and forwarded as text *(voice path only)* |
| 4️⃣ | 🔍 **Retrieval** | Semantic search finds the most relevant PDF chunks |
| 5️⃣ | 🧠 **Generation** | LLM generates an answer using the retrieved context |
| 6️⃣ | ⚡ **Streaming** | Response is streamed token-by-token back to the browser |
| 7️⃣ | 🔊 **TTS** *(optional)* | `text_to_speech.py` reads the response aloud |

---

## 🔌 API & WebSocket Reference

The app runs **two WebSocket servers** that the frontend connects to simultaneously.

### ⚡ LLM Response WebSocket — `llm_response_websocket.py`

> Handles natural language queries and streams LLM responses token by token.

| 🔧 Property | 📋 Value |
|------------|---------|
| 🔌 Default Port | `8765` |
| 📡 Protocol | `ws://` |
| 🔁 Direction | Bidirectional |

📤 **Client → Server:**
```json
{
  "query": "What are the governance principles outlined in the document?",
  "language": "english"
}
```

📥 **Server → Client** *(streamed token by token):*
```json
{ "token": "The",  "done": false }
{ "token": " key", "done": false }
{ "token": "",     "done": true  }
```
> 💡 When `"done": true`, the stream has ended and the full response has been delivered.

---

### 🎙️ Speech Recognition WebSocket — `speech_recognition_websocket.py`

> Accepts a raw audio stream from the browser microphone and returns a transcript.

| 🔧 Property | 📋 Value |
|------------|---------|
| 🔌 Default Port | `8766` |
| 📡 Protocol | `ws://` |
| 🔁 Direction | Bidirectional |

📤 **Client → Server:** Raw audio bytes (PCM/WAV via browser `MediaRecorder` API)

📥 **Server → Client:**
```json
{
  "transcript": "What are the governance principles outlined in the document?"
}
```
> 💡 The transcript is then forwarded to the LLM WebSocket as a standard text query.

---

## 🛠️ Tech Stack

| 🔧 Technology | 💡 Role |
|--------------|--------|
| 🐍 Python | Backend logic, WebSocket servers, RAG pipeline |
| 🔌 WebSockets | Real-time bidirectional communication |
| 🎙️ Speech Recognition | Audio-to-text for English voice queries |
| 🔊 Text-to-Speech | Converts LLM responses to audio |
| 🧠 LLM | Language model for PDF-grounded answer generation |
| 📄 Vector Store | Semantic retrieval over embedded PDF chunks |
| 🌐 HTML / CSS / JS | Frontend chat interfaces |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. 🍴 Fork the repo
2. 🌿 Create a feature branch (`git checkout -b feature/my-feature`)
3. 💾 Commit your changes (`git commit -m 'Add my feature'`)
4. 📤 Push to the branch (`git push origin feature/my-feature`)
5. 🔃 Open a Pull Request

---

## 📄 License

This project is open source. See the repository for details.

---

## 👤 Author

**Musagen12** — [🐙 GitHub](https://github.com/Musagen12)

---

<p align="center">⭐ If you find this project useful, please consider giving it a star!</p>