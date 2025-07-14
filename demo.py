"""
Demonstration script showing QuickCommand capabilities.
Run this to see examples without needing OpenAI API.
"""

import asyncio
import sys
from pathlib import Path
import colorama
from colorama import Fore, Style

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import Settings
from shells.powershell_handler import PowerShellHandler
from shells.python_handler import PythonHandler

# Initialize colorama
colorama.init(autoreset=True)

def print_banner():
    """Print demonstration banner."""
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                QuickCommand AI Assistant Demo                   ║")
    print("║                  Showing Fallback Capabilities                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

def demonstrate_command_mapping():
    """Show how natural language maps to commands."""
    
    examples = [
        {
            "query": "command for remote group policy update",
            "command": "gpupdate /force",
            "description": "Force Group Policy update on local machine",
            "shell": "PowerShell"
        },
        {
            "query": "list all running services", 
            "command": "Get-Service | Where-Object {$_.Status -eq 'Running'}",
            "description": "List all services with 'Running' status",
            "shell": "PowerShell"
        },
        {
            "query": "check disk space on C drive",
            "command": "Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID,Size,FreeSpace",
            "description": "Display disk space information for all drives",
            "shell": "PowerShell"
        },
        {
            "query": "install python package for web scraping",
            "command": "pip install requests beautifulsoup4",
            "description": "Install popular web scraping packages",
            "shell": "Python"
        },
        {
            "query": "create a new directory and navigate to it",
            "command": "mkdir new_project; cd new_project",
            "description": "Create directory and change to it",
            "shell": "PowerShell"
        }
    ]
    
    print(f"{Fore.GREEN}Natural Language → Command Examples:{Style.RESET_ALL}")
    print("=" * 70)
    
    for i, example in enumerate(examples, 1):
        print(f"\n{Fore.YELLOW}{i}. User says:{Style.RESET_ALL} \"{example['query']}\"")
        print(f"   {Fore.CYAN}QuickCommand suggests:{Style.RESET_ALL} {example['command']}")
        print(f"   {Fore.MAGENTA}Shell:{Style.RESET_ALL} {example['shell']}")
        print(f"   {Fore.WHITE}Description:{Style.RESET_ALL} {example['description']}")

def show_shell_info():
    """Display information about available shells."""
    print(f"\n{Fore.GREEN}Available Shell Handlers:{Style.RESET_ALL}")
    print("=" * 40)
    
    # PowerShell info
    ps_handler = PowerShellHandler()
    ps_info = ps_handler.get_shell_info()
    
    print(f"\n{Fore.CYAN}PowerShell:{Style.RESET_ALL}")
    print(f"  Available: {Fore.GREEN if ps_info['available'] else Fore.RED}{ps_info['available']}{Style.RESET_ALL}")
    if ps_info['available']:
        print(f"  Version: {ps_info.get('version', 'Unknown')}")
        print(f"  Type: {ps_info.get('type', 'Unknown')}")
        print(f"  Command: {ps_info.get('command', 'Unknown')}")
    
    # Python info  
    py_handler = PythonHandler()
    py_info = py_handler.get_shell_info()
    
    print(f"\n{Fore.CYAN}Python:{Style.RESET_ALL}")
    print(f"  Available: {Fore.GREEN}{py_info['available']}{Style.RESET_ALL}")
    print(f"  Version: {py_info['version']}")
    print(f"  Platform: {py_info['platform']}")
    print(f"  Implementation: {py_info['implementation']}")
    print(f"  Executable: {py_info['executable']}")

def show_configuration():
    """Display current configuration."""
    settings = Settings()
    
    print(f"\n{Fore.GREEN}Current Configuration:{Style.RESET_ALL}")
    print("=" * 30)
    
    config = settings.to_dict()
    for key, value in config.items():
        color = Fore.GREEN if value not in [None, False] else Fore.RED
        print(f"  {key}: {color}{value}{Style.RESET_ALL}")

def show_usage_instructions():
    """Show how to use the application."""
    print(f"\n{Fore.GREEN}How to Use QuickCommand:{Style.RESET_ALL}")
    print("=" * 35)
    
    steps = [
        "Run setup.bat to install dependencies",
        "Copy .env.example to .env", 
        "Add your OpenAI API key to .env file",
        "Run: python quickcommand.py",
        "Type natural language commands and get AI suggestions",
        "Review suggested commands before execution",
        "Type 'exit' to quit the application"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"  {Fore.CYAN}{i}.{Style.RESET_ALL} {step}")
    
    print(f"\n{Fore.YELLOW}Example Session:{Style.RESET_ALL}")
    print("  ❯ command for remote group policy update")
    print("  Thinking...")
    print("  Suggested command: gpupdate /force")
    print("  Execute this command? (y/n/copy): y")
    print("  Executing command...")
    print("  Microsoft Windows [Version...]")

def main():
    """Run the demonstration."""
    print_banner()
    
    print(f"{Fore.YELLOW}This demo shows QuickCommand capabilities without requiring OpenAI API.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}The actual application uses AI for much more intelligent suggestions!{Style.RESET_ALL}\n")
    
    demonstrate_command_mapping()
    show_shell_info() 
    show_configuration()
    show_usage_instructions()
    
    print(f"\n{Fore.GREEN}Ready to try the real application? Run: python quickcommand.py{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
