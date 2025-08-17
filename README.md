# 🤖 AI Chat Service

A modern AI chatbot service powered by Google Gemini with multiple interfaces including web UI, terminal chat, and REST API.

## ✨ Features

- 🌐 **Beautiful Web Interface** - Modern, responsive chat UI
- 💻 **Terminal Chat** - Interactive command-line interface  
- 🔌 **REST API** - Easy integration with other applications
- 🐍 **Python Client** - Built-in Python client for API calls
- 📚 **Auto Documentation** - FastAPI automatic API docs
- 🎯 **Multiple Run Modes** - Choose how you want to interact

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Eng-Sameh/NTI-ai-chat-service.git
   cd ai-chat-service
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   ```
   
   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

4. **Run the application**
   ```bash
   python chatbot.py
   ```

## 🎯 Usage Options

When you run the application, you'll see a menu:

```
🚀 AI Chat Service
Choose an option:
1. Start server only
2. Start server + test with Python client  
3. Start server + interactive chat
4. Test API client (server must be running)
```

### Option 1: Web Interface
- Choose option 1
- Visit `http://127.0.0.1:8000` for the web chat interface
- Visit `http://127.0.0.1:8000/docs` for API documentation

### Option 2: API Testing
- Automatically tests the API with sample messages
- Great for development and debugging

### Option 3: Terminal Chat
- Interactive chat directly in your terminal
- Type messages and get instant AI responses
- Commands: `quit` to exit, `clear` to reset context

### Option 4: Client Only
- Connect to an already running server
- Useful for testing or multiple client connections

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web chat interface |
| `/conversation` | POST | Send message to AI |
| `/health` | GET | Health check |
| `/docs` | GET | API documentation |
| `/api-info` | GET | API information |

### Example API Usage

**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/conversation" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, how are you?"}'
```

**Python:**
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/conversation",
    json={"message": "What is AI?"}
)
print(response.json()["reply"])
```

**JavaScript:**
```javascript
fetch('http://127.0.0.1:8000/conversation', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: 'Hello!'})
})
.then(response => response.json())
.then(data => console.log(data.reply));
```

## 🏗️ Project Structure

```
ai-chat-service/
├── chatbot.py          # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## 🛠️ Development

### Running in Development Mode
```bash
# Option 1: Use the built-in menu
python chatbot.py

# Option 2: Direct server start
uvicorn chatbot:app --reload --host 127.0.0.1 --port 8000
```

### Testing the API
The application includes built-in testing functionality. Choose option 2 from the menu to automatically test all endpoints.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes |

### Customization

You can customize the AI behavior by modifying the prompt template in the `GeminiChatService` class:

```python
self.template = ChatPromptTemplate.from_template(
    "You are a helpful AI assistant. "
    "{background_context}"
    "\n\nUser inquiry: {user_message}"
)
```

## 🚨 Troubleshooting

### Common Issues

**"GOOGLE_API_KEY environment variable is required"**
- Make sure you've created a `.env` file with your API key
- Verify the API key is valid and active

**"Connection error"**
- Ensure the server is running
- Check if port 8000 is available
- Verify your internet connection

**"Module not found"**
- Install all dependencies: `pip install -r requirements.txt`
- Activate your virtual environment if using one

## 📞 Support

If you have questions or need help:
- Check the [API documentation](http://127.0.0.1:8000/docs) when server is running
- Open an [issue](https://github.com/YOUR_USERNAME/ai-chat-service/issues)
- Review the troubleshooting section above

## 🌟 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Google Gemini](https://ai.google.dev/) for the AI model
- [LangChain](https://langchain.com/) for AI integration
- [Uvicorn](https://www.uvicorn.org/) for the ASGI server