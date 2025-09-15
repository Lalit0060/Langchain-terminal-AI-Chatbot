# 🤖 LangChain Animated Streaming Chatbot

A beautiful, feature-rich conversational AI chatbot built with LangChain, LangGraph, and Rich library for stunning terminal animations.

## ✨ Features

- 🎭 **Beautiful Animations**: Smooth streaming with rich terminal effects
- 🎨 **Markdown Rendering**: Rich markdown support with syntax highlighting
- 🧠 **Conversation Memory**: Persistent chat history across sessions
- ⚡ **Real-time Streaming**: Token-by-token response streaming
- 🎬 **Multiple Animation Modes**: Choose between standard and ultra-smooth async
- 🔒 **Secure API Management**: Environment variable support for API keys

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free from [Google AI Studio](https://aistudio.google.com/))

### Installation

1. **Clone or create the project directory:**
   ```
   mkdir langchain_chatbot
   cd langchain_chatbot
   ```

2. **Create virtual environment:**
   ```
   python -m venv langchain_env
   ```

3. **Activate virtual environment:**
   
   **Windows:**
   ```
   langchain_env\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```
   source langchain_env/bin/activate
   ```

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Configure API key:**
   
   **Option 1: Environment file (Recommended)**
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your Google API key
   
   **Option 2: Runtime input**
   - The app will prompt for API key on first run

6. **Run the chatbot:**
   ```
   python streaming_chatbot.py
   ```

## 🎮 Usage

### Animation Modes

**Standard Animated Chat (Option 1):**
- Beautiful panels and spinners
- Smooth streaming with cursor effects
- Perfect for most users

**Ultra-Smooth Async Chat (Option 2):**
- Advanced async streaming
- Pulsing border effects
- Dynamic animations
- Best performance

### Commands

- Type your messages naturally
- Use `quit`, `exit`, or `bye` to end chat
- Press `Ctrl+C` for graceful interruption

### Markdown Support

The chatbot supports rich markdown formatting:

- **Bold text** with `**text**`
- *Italic text* with `*text*`
- `Inline code` with backticks
- Code blocks with triple backticks
- Lists, headers, and blockquotes
- Tables and horizontal rules

## 🛠️ Technical Details

### Architecture

- **LangChain**: Core LLM framework
- **LangGraph**: State management and memory
- **Rich**: Terminal animations and rendering
- **Google Gemini**: AI model provider

### Key Components

- `streaming_chatbot.py`: Main application
- `requirements.txt`: Python dependencies
- `.env`: Environment configuration
- `README.md`: Documentation

### Memory Management

- Persistent conversation history
- Thread-based session management
- Automatic context preservation
- Memory optimization for long conversations

## 🎨 Customization

### Animation Settings

Modify animation parameters in the code:

```
# Streaming speed
time.sleep(0.05)  # Adjust for faster/slower streaming

# Refresh rate
refresh_per_second=20  # Higher = smoother animations

# Spinner styles
Spinner("dots12", ...)  # Try: "aesthetic", "bouncingBar", "hearts"
```

### Color Themes

Rich supports extensive color customization:

```
# Border colors
border_style="green"  # Try: "blue", "cyan", "magenta", "red"

# Text styles
"[bold cyan]Text[/bold cyan]"  # Combine styles
```

## 🔧 Troubleshooting

### Common Issues

**Import Errors:**
```
pip install --upgrade langchain langgraph langchain-google-genai rich
```

**API Key Issues:**
- Verify key at [Google AI Studio](https://aistudio.google.com/)
- Check API quotas and billing
- Ensure `.env` file is in project root

**Animation Performance:**
- Reduce `refresh_per_second` for slower systems
- Use standard mode instead of async mode
- Close other terminal applications

**Memory Issues:**
- Restart chat session periodically
- Check available system memory
- Reduce conversation history if needed

## 📁 Project Structure

```
langchain_chatbot/
├── langchain_env/          # Virtual environment
├── streaming_chatbot.py    # Main chatbot script
├── requirements.txt        # Dependencies
├── .env                   # API keys (optional)
└── README.md              # Documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section
2. Review [LangChain documentation](https://python.langchain.com/)
3. Visit [Rich documentation](https://rich.readthedocs.io/)
4. Create an issue in the repository

## 🚀 What's Next?

Future enhancements planned:

- [ ] Voice input/output support
- [ ] Custom AI model integration
- [ ] Chat export functionality
- [ ] Plugin system for extensions
- [ ] Web interface option
- [ ] Multi-language support

---

**Enjoy your beautiful AI conversations!** 🤖✨
```

## **How to Create These Files**

**Step 1: Create the files in your project directory**
```cmd
cd langchain_chatbot
```

**Step 2: Create requirements.txt**
```cmd
echo langchain>=0.3.0 > requirements.txt
echo langgraph>=0.2.0 >> requirements.txt
echo langchain-google-genai>=2.0.0 >> requirements.txt
echo rich>=13.0.0 >> requirements.txt
echo python-dotenv>=1.0.0 >> requirements.txt
```

**Step 3: Create .env file**
- Copy the .env content above into a new file named `.env`
- Replace `your_google_gemini_api_key_here` with your actual API key

**Step 4: Create README.md**
- Copy the README.md content above into a new file named `README.md`

**Step 5: Your final structure should be:**
```
langchain_chatbot/
├── langchain_env/          # (Create with: python -m venv langchain_env)
├── streaming_chatbot.py    # (Your main code file)
├── requirements.txt        # ✅ Created
├── .env                   # ✅ Created  
└── README.md              # ✅ Created
```