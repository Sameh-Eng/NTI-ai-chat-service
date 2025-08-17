
"""
AI Chat Service using Google Gemini
A simple REST API for conversational AI interactions with built-in client and web interface
"""

import os
import uvicorn
import asyncio
import requests
import threading
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Union
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

class MessageRequest(BaseModel):
    """Request model for chat messages"""
    message: str = Field(..., min_length=1, description="User's message to the AI")
    background_info: Union[str, None] = Field(None, description="Additional context for the conversation")

class MessageResponse(BaseModel):
    """Response model for AI replies"""
    reply: str = Field(..., description="AI generated response")

class GeminiChatService:
    """Service class for handling Gemini AI interactions"""
    
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
        
        self.template = ChatPromptTemplate.from_template(
            "You are a helpful AI assistant. "
            "{background_context}"
            "\n\nUser inquiry: {user_message}"
        )
        
        self.processing_chain = self.template | self.llm | StrOutputParser()
    
    async def generate_response(self, user_msg: str, context: str = "") -> str:
        """Generate AI response for user message"""
        try:
            payload = {
                "background_context": f"Context: {context}" if context else "",
                "user_message": user_msg
            }
            
            result = self.processing_chain.invoke(payload)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")

class ChatClient:
    """Python client for the chat API"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def send_message(self, message: str, context: str = None) -> str:
        """Send a message to the chat API"""
        url = f"{self.base_url}/conversation"
        payload = {"message": message}
        if context:
            payload["background_info"] = context
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()["reply"]
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
    
    def interactive_chat(self):
        """Start an interactive chat session"""
        print("🤖 AI Chat Client Started!")
        print("Type 'quit' to exit, 'clear' to reset context\n")
        
        context = ""
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'clear':
                    context = ""
                    print("🧹 Context cleared!")
                    continue
                elif not user_input:
                    continue
                
                print("🤖 AI: ", end="", flush=True)
                response = self.send_message(user_input, context)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break


def create_app() -> FastAPI:
    """Application factory"""
    application = FastAPI(
        title="AI Chat Service",
        description="RESTful API for conversational AI using Google Gemini",
        version="1.0.0"
    )
    
    chat_service = GeminiChatService()
    
    @application.get("/", response_class=HTMLResponse)
    async def chat_interface():
        """Simple web chat interface"""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI Chat Interface</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .chat-container {
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    overflow: hidden;
                }
                .chat-header {
                    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    padding: 20px;
                    text-align: center;
                }
                .chat-messages {
                    height: 400px;
                    overflow-y: auto;
                    padding: 20px;
                    background: #f8f9fa;
                }
                .message {
                    margin: 10px 0;
                    padding: 12px 16px;
                    border-radius: 18px;
                    max-width: 80%;
                    word-wrap: break-word;
                }
                .user-message {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    margin-left: auto;
                }
                .ai-message {
                    background: #e9ecef;
                    color: #333;
                    margin-right: auto;
                }
                .input-container {
                    display: flex;
                    padding: 20px;
                    gap: 10px;
                    background: white;
                }
                .message-input {
                    flex: 1;
                    padding: 12px 16px;
                    border: 2px solid #e9ecef;
                    border-radius: 25px;
                    outline: none;
                    font-size: 16px;
                }
                .message-input:focus {
                    border-color: #4facfe;
                }
                .send-button {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 25px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: transform 0.2s;
                }
                .send-button:hover {
                    transform: translateY(-1px);
                }
                .send-button:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
                }
                .loading {
                    text-align: center;
                    color: #666;
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            <div class="chat-container">
                <div class="chat-header">
                    <h1>🤖 Sameh AI Chat Assistant</h1>
                    <p>Powered by Google Gemini - Sameh Reda</p>
                </div>
                <div class="chat-messages" id="chatMessages">
                    <div class="message ai-message">
                        👋 Hello! I'm your AI assistant. How can I help you today?
                    </div>
                </div>
                <div class="input-container">
                    <input 
                        type="text" 
                        id="messageInput" 
                        class="message-input" 
                        placeholder="Type your message here..."
                        onkeypress="handleKeyPress(event)"
                    >
                    <button onclick="sendMessage()" id="sendButton" class="send-button">Send</button>
                </div>
            </div>

            <script>
                const chatMessages = document.getElementById('chatMessages');
                const messageInput = document.getElementById('messageInput');
                const sendButton = document.getElementById('sendButton');

                function addMessage(message, isUser) {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
                    messageDiv.textContent = message;
                    chatMessages.appendChild(messageDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }

                function showLoading() {
                    const loadingDiv = document.createElement('div');
                    loadingDiv.className = 'loading';
                    loadingDiv.id = 'loading';
                    loadingDiv.textContent = '🤔 Sameh-AI is thinking...';
                    chatMessages.appendChild(loadingDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }

                function hideLoading() {
                    const loading = document.getElementById('loading');
                    if (loading) loading.remove();
                }

                async function sendMessage() {
                    const message = messageInput.value.trim();
                    if (!message) return;

                    // Disable input
                    messageInput.disabled = true;
                    sendButton.disabled = true;

                    // Add user message
                    addMessage(message, true);
                    messageInput.value = '';

                    // Show loading
                    showLoading();

                    try {
                        const response = await fetch('/conversation', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ message: message })
                        });

                        const data = await response.json();
                        
                        hideLoading();
                        if (response.ok) {
                            addMessage(data.reply, false);
                        } else {
                            addMessage('Sorry, there was an error processing your message.', false);
                        }
                    } catch (error) {
                        hideLoading();
                        addMessage('Connection error. Please try again.', false);
                    } finally {
                        // Re-enable input
                        messageInput.disabled = false;
                        sendButton.disabled = false;
                        messageInput.focus();
                    }
                }

                function handleKeyPress(event) {
                    if (event.key === 'Enter') {
                        sendMessage();
                    }
                }

                // Focus input on load
                messageInput.focus();
            </script>
        </body>
        </html>
        """
    
    @application.post("/conversation", response_model=MessageResponse)
    async def handle_conversation(req: MessageRequest):
        """Endpoint for processing chat conversations"""
        response_text = await chat_service.generate_response(
            user_msg=req.message,
            context=req.background_info or ""
        )
        
        return MessageResponse(reply=response_text)
    
    @application.get("/api-info")
    async def api_info():
        """API information endpoint"""
        return {
            "message": "AI Chat Service API",
            "version": "1.0.0",
            "endpoints": {
                "chat": "/conversation",
                "health": "/health",
                "docs": "/docs",
                "web_interface": "/"
            }
        }
    
    @application.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "service": "AI Chat Service"}
    
    return application


app = create_app()

def start_server():
    """Start the development server"""
    uvicorn.run(
        "chatbot:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

def run_server_in_background():
    """Run the FastAPI server in a separate thread"""
    uvicorn.run(
        "chatbot:app",
        host="127.0.0.1",
        port=8000,
        log_level="error"  
    )

def test_api_client():
    """Test the API with Python client"""
    print("🧪 Testing API Client...")
    client = ChatClient()
    
    
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    
    test_messages = [
        "Hello! How are you today?",
        "What's 2 + 2?",
        "Tell me a fun fact about space"
    ]
    
    for msg in test_messages:
        print(f"\n📤 Sending: {msg}")
        response = client.send_message(msg)
        print(f"📥 Response: {response}")
    
    print("\n✅ API test completed!")

def main():
    """Main function with options"""
    print("🚀 AI Chat Service")
    print("Choose an option:")
    print("1. Start server only")
    print("2. Start server + test with Python client")
    print("3. Start server + interactive chat")
    print("4. Test API client (server must be running)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        print("🌐 Starting server at http://127.0.0.1:8000")
        print("💡 Visit http://127.0.0.1:8000 for web interface")
        print("📚 Visit http://127.0.0.1:8000/docs for API docs")
        start_server()
        
    elif choice == "2":
        print("🌐 Starting server and testing...")
        server_thread = threading.Thread(target=run_server_in_background, daemon=True)
        server_thread.start()
        test_api_client()
        input("\nPress Enter to exit...")
        
    elif choice == "3":
        print("🌐 Starting server...")
        server_thread = threading.Thread(target=run_server_in_background, daemon=True)
        server_thread.start()
        time.sleep(3)  
        
        print("💬 Starting interactive chat...")
        client = ChatClient()
        client.interactive_chat()
        
    elif choice == "4":
        client = ChatClient()
        client.interactive_chat()
        
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()