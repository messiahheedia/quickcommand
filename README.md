# QuickCommand AI Assistant

> *"Say what you want, get the exact command - but you're always in control."*

**Created by Siah** 

An AI-powered command assistant that translates natural language into precise PowerShell and Python commands. Perfect for developers, system administrators, and anyone who wants intelligent command suggestions without the risk of auto-execution.

## 🎯 What is QuickCommand?

QuickCommand bridges the gap between what you want to do and the exact command syntax you need. Simply describe your task in plain English, and get precise, ready-to-execute commands - but **you're always in control** of when and if they run.

### Example Translations
```
You say: "command for remote group policy update"
You get: gpupdate /force

You say: "list all running services" 
You get: Get-Service | Where-Object {$_.Status -eq "Running"}

You say: "check disk space"
You get: Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID,Size,FreeSpace
```

## ✨ Key Features

- 🧠 **AI-Powered Translation** - Natural language to precise commands
- 👀 **Preview Before Execute** - See exactly what will run
- 🔒 **Safety First** - Never auto-executes, you're in control
- ⚡ **Multi-Shell Support** - PowerShell and Python environments
- 🎨 **Rich Interface** - Colorful, intuitive terminal UI
- 📋 **Smart Recommendations** - 24+ built-in command suggestions
- 🔄 **Fallback System** - Works even without AI API
- ⚙️ **Highly Configurable** - Environment-based settings

## 🚀 Quick Start

### Option 1: Automated Setup (Windows)
```batch
# Clone and run setup
git clone https://github.com/messiahheedia/quickcommand.git
cd quickcommand
setup.bat
```

### Option 2: Manual Setup
```bash
# 1. Clone the repository
git clone https://github.com/messiahheedia/quickcommand.git
cd quickcommand

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API (optional but recommended)
cp .env.example .env
# Edit .env and add your OpenAI API key

# 4. Run QuickCommand
python quickcommand.py
```

## 📋 Requirements

- **Python 3.7+** (tested on 3.13.3)
- **PowerShell** (Windows PowerShell or PowerShell Core)
- **OpenAI API Key** (optional - fallback mode available)

## 🔧 Configuration

### Environment Variables (.env file)
```env
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here  # Alternative AI provider
DEFAULT_SHELL=powershell
LOG_LEVEL=INFO
```

### Supported AI Providers
- **OpenAI GPT-3.5/4** (primary)
- **Google Gemini** (fallback)
- **Pattern Matching** (offline fallback)

## 🎮 How to Use

1. **Launch QuickCommand**
   ```bash
   python quickcommand.py
   ```

2. **Describe what you want**
   ```
   > "list all files in downloads folder"
   ```

3. **Review the suggestion**
   ```
   AI Suggestion:
   Command: Get-ChildItem "$env:USERPROFILE\Downloads"
   Description: Lists all files and folders in the Downloads directory
   Warning: None
   ```

4. **Choose your action**
   - `[E]xecute` - Run the command
   - `[C]opy` - Copy to clipboard  
   - `[S]kip` - Try a different request
   - `[Q]uit` - Exit application

## 🏗️ Project Structure

```
QuickCommand/
├── quickcommand.py              # 🚀 Main application
├── ai/                          # 🧠 AI integration
│   ├── command_ai.py           # OpenAI/Gemini API handler  
│   └── prompts.py              # AI prompt templates
├── shells/                      # 🔧 Shell handlers
│   ├── powershell_handler.py   # PowerShell execution
│   └── python_handler.py       # Python execution  
├── config/                      # ⚙️ Configuration
│   ├── settings.py             # App settings
│   └── command_patterns.yaml   # Fallback patterns
├── setup.bat                    # 📦 Automated setup
├── start.bat                    # 🎬 Quick launcher
└── requirements.txt             # 📋 Dependencies
```

## 🛡️ Safety & Security

- **No Auto-Execution** - Commands are never run without explicit user approval
- **Input Sanitization** - All inputs are validated and sanitized
- **Preview Mode** - See exactly what will execute before running
- **Secure Configuration** - API keys managed via environment variables
- **Audit Trail** - All commands and outputs are visible

## 🔧 Advanced Usage

### Batch Mode
```bash
python quickcommand.py --batch "list running services, check disk space, get system info"
```

### Custom Patterns
Edit `config/command_patterns.yaml` to add your own command mappings:
```yaml
patterns:
  - query: "restart iis"
    command: "iisreset"
    description: "Restart Internet Information Services"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for the powerful GPT API
- **Google** for Gemini AI integration
- **Microsoft** for PowerShell and Windows Terminal
- **Python Community** for excellent libraries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/messiahheedia/quickcommand/issues)
- **Creator**: Siah (Messiah Heedia)
- **Repository**: https://github.com/messiahheedia/quickcommand

---

**Created with ❤️ by Siah** | *Making command-line accessible to everyone*