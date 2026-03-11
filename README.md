# 🤖 Fully Featured Chatbot

A multilingual, voice-enabled chatbot that lets you query your PDF documents in **English** or **Kiswahili** — with real-time speech recognition and WebSocket-powered responses.

---

## ✨ Features

- 📄 **PDF Q&A** — Upload and query any PDF document using natural language
- 🌍 **Multilingual Support** — Interact in English or Kiswahili
- 🎙️ **Voice Input** — English voice support via speech recognition
- ⚡ **Real-time Streaming** — WebSocket-based LLM responses for low latency
- 🔊 **Speech Recognition WebSocket** — Dedicated socket for audio input processing

---

## 🗂️ Project Structure

```
fully_featured_chatbot/
├── src/
│   ├── english_governance_chatbot/   # English PDF Q&A module
│   ├── kiswahili/                    # Kiswahili language module
│   ├── __init__.py
│   ├── index.html                    # Main chat interface
│   ├── kiswahili.html                # Kiswahili chat interface
│   ├── feedback.html                 # User feedback page
│   ├── query_llm.py                  # LLM query logic
│   ├── speech_recognition.py         # Speech-to-text processing
│   └── text_to_speech.py             # Text-to-speech output
├── llm_response_websocket.py         # WebSocket server for LLM responses
├── speech_recognition_websocket.py   # WebSocket server for speech input
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Musagen12/fully_featured_chatbot.git
   cd fully_featured_chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

Start the LLM response WebSocket server:
```bash
python llm_response_websocket.py
```

Start the speech recognition WebSocket server (for voice input):
```bash
python speech_recognition_websocket.py
```

Then launch the frontend from the `src/` directory according to its own setup instructions.

---

## 💬 Usage

1. Upload a PDF document through the interface
2. Choose your preferred language — **English** or **Kiswahili**
3. Type your question, or use the **voice input** button (English only)
4. Receive a streamed response grounded in the content of your PDF

---

## 🌐 Supported Languages

| Language   | Text Input | Voice Input |
|------------|-----------|-------------|
| English    | ✅        | ✅          |
| Kiswahili  | ✅        | ❌          |

---

## 🏗️ How It Works

The chatbot follows a **Retrieval-Augmented Generation (RAG)** architecture, combining document retrieval with an LLM to produce grounded, accurate answers.

```
┌─────────────────────────────────────────────────────┐
│                    Browser (Frontend)                │
│   index.html / kiswahili.html / feedback.html       │
└────────────┬────────────────────┬───────────────────┘
             │ Text/Query         │ Audio Stream
             ▼                    ▼
┌────────────────────┐  ┌─────────────────────────────┐
│ llm_response_      │  │ speech_recognition_          │
│ websocket.py       │  │ websocket.py                 │
│ (LLM WebSocket)    │  │ (Speech WebSocket)           │
└────────┬───────────┘  └──────────┬──────────────────┘
         │                         │ Transcribed Text
         │ ◄───────────────────────┘
         ▼
┌────────────────────┐
│   query_llm.py     │  ← Retrieves relevant PDF chunks
│   (RAG Pipeline)   │    and constructs LLM prompt
└────────┬───────────┘
         │
         ▼
┌────────────────────────────────────────┐
│  english_governance_chatbot/           │  ← English module
│  kiswahili/                            │  ← Kiswahili module
│  (Language-specific retrieval logic)   │
└────────────────────────────────────────┘
```

**Step-by-step flow:**

1. **PDF Ingestion** — Documents are chunked, embedded, and stored in a vector index at startup
2. **Query** — The user submits a question via text or voice (English only)
3. **Speech-to-Text** *(voice path)* — `speech_recognition_websocket.py` transcribes the audio and forwards the text
4. **Retrieval** — `query_llm.py` performs a semantic search over the PDF vector store to find the most relevant chunks
5. **Generation** — The retrieved context and user query are sent to the LLM, which streams a response back
6. **Response** — The answer is streamed in real time to the browser via the LLM WebSocket; `text_to_speech.py` can optionally read it aloud

---

## 🔌 API & WebSocket Reference

The app exposes two WebSocket servers that the frontend connects to simultaneously.

### LLM Response WebSocket — `llm_response_websocket.py`

Handles natural language queries and streams LLM responses.

| Property | Value |
|----------|-------|
| Default Port | `8765` |
| Protocol | `ws://` |
| Direction | Bidirectional |

**Client → Server message:**
```json
{
  "query": "What are the governance principles outlined in the document?",
  "language": "english"
}
```

**Server → Client message (streamed):**
```json
{ "token": "The",  "done": false }
```
```json
{ "token": "", "done": true }
```

The server streams tokens incrementally so the UI can render responses in real time. When `done` is `true`, the stream is complete.

---

### Speech Recognition WebSocket — `speech_recognition_websocket.py`

Accepts a raw audio stream from the browser and returns a transcribed text string.

| Property | Value |
|----------|-------|
| Default Port | `8766` |
| Protocol | `ws://` |
| Direction | Bidirectional |

**Client → Server:** Raw audio bytes (PCM/WAV stream from the browser's `MediaRecorder` API)

**Server → Client message:**
```json
{
  "transcript": "What are the governance principles outlined in the document?"
}
```

Once received by the frontend, the transcript is forwarded to the LLM WebSocket as a standard text query.

---

## 🛠️ Tech Stack

- **Python** — Backend logic and WebSocket servers
- **WebSockets** — Real-time bidirectional communication
- **Speech Recognition** — Audio-to-text for English voice queries
- **LLM Integration** — Language model for PDF-grounded answers

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is open source. See the repository for details.

---

## 👤 Author

**Musagen12** — [GitHub](https://github.com/Musagen12)