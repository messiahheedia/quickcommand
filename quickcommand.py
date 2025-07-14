#!/usr/bin/env python3
"""
QuickCommand AI Assistant
An AI-powered command assistant for PowerShell and Python environments.
"""

import sys
import os
import random
from pathlib import Path
from typing import Optional
import click
import colorama
from colorama import Fore, Style
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai.command_ai import CommandAI
from shells.powershell_handler import PowerShellHandler
from shells.python_handler import PythonHandler
from config.settings import Settings

# Initialize colorama for colored output
colorama.init(autoreset=True)

class QuickCommand:
    """Main application class for the AI command assistant."""
    
    def __init__(self):
        """Initialize the QuickCommand assistant."""
        load_dotenv()
        self.settings = Settings()
        self.ai = CommandAI(self.settings)
        self.powershell = PowerShellHandler()
        self.python_handler = PythonHandler()
        
    def print_banner(self):
        """Print the application banner."""
        print(f"{Fore.CYAN}{Style.BRIGHT}")
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║                    QuickCommand AI Assistant                     ║")
        print("║              Natural Language → Smart Commands                  ║")
        print("║                        Created by Siah                          ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print(f"{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type your command description and I'll suggest the right command!")
        print(f"{Fore.YELLOW}Type 'exit' or 'quit' to leave, 'help' for assistance.{Style.RESET_ALL}\n")
    
    def get_all_recommendations(self):
        """Get the full list of available recommendations with function and actual command."""
        return [
            ("Remote Group Policy Update", "gpupdate /force", "System Administration"),
            ("Check All Drive Space", "Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID,Size,FreeSpace", "System Monitoring"),
            ("List Running Services", "Get-Service | Where-Object {$_.Status -eq 'Running'}", "Process Management"),
            ("Show Top CPU Processes", "Get-Process | Sort-Object CPU -Descending | Select-Object -First 10", "Performance Monitoring"),
            ("Install Web Scraping Package", "pip install requests beautifulsoup4", "Development"),
            ("Find Large Files (1GB+)", "Get-ChildItem -Recurse | Where-Object {$_.Length -gt 1GB}", "File Management"),
            ("Show Network Connections", "netstat -an", "Network Diagnostics"),
            ("Backup Registry Key", "reg export HKLM\\SOFTWARE\\backup.reg", "System Backup"),
            ("Restart Print Spooler", "Restart-Service Spooler", "Service Management"),
            ("Show System Uptime", "Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object LastBootUpTime", "System Information"),
            ("List Installed Programs", "Get-WmiObject -Class Win32_Product | Select-Object Name,Version", "Software Management"),
            ("Check Memory Usage", "Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10", "Performance Monitoring"),
            ("Windows Defender Scan", "Start-MpScan -ScanType QuickScan", "Security"),
            ("Create Daily Task", "schtasks /create /tn 'DailyTask' /tr 'notepad.exe' /sc daily", "Task Automation"),
            ("Export System Event Logs", "Get-EventLog -LogName System -Newest 100 | Export-Csv events.csv", "System Diagnostics"),
            ("Check Firewall Status", "Get-NetFirewallProfile", "Security"),
            ("Compress to ZIP", "Compress-Archive -Path C:\\temp\\* -DestinationPath archive.zip", "File Management"),
            ("Show Network Adapters", "Get-NetAdapter", "Network Diagnostics"),
            ("List User Accounts", "Get-LocalUser", "User Management"),
            ("Clear Temp Files", "Remove-Item -Path $env:TEMP\\* -Recurse -Force", "System Cleanup"),
            ("Check Drive Health", "Get-PhysicalDisk | Get-StorageReliabilityCounter", "System Diagnostics"),
            ("Show Environment Variables", "Get-ChildItem Env:", "System Configuration"),
            ("Kill Process by Name", "Stop-Process -Name 'notepad' -Force", "Process Management"),
            ("Create New User", "New-LocalUser -Name 'NewUser' -Password (ConvertTo-SecureString 'Password123' -AsPlainText -Force)", "User Management")
        ]
    
    def show_recommendations(self):
        """Show 8 random command recommendations on startup."""
        all_recommendations = self.get_all_recommendations()
        selected = random.sample(all_recommendations, 8)
        
        print(f"{Fore.GREEN}{Style.BRIGHT}💡 Recommended Commands{Style.RESET_ALL}")
        print("─" * 80)
        
        recommendations_dict = {}
        for i, (function, command, category) in enumerate(selected, 1):
            print(f"{Fore.MAGENTA}[{i}]{Style.RESET_ALL} {Fore.CYAN}{function}{Style.RESET_ALL}")
            print(f"    Command: {Fore.WHITE}{command}{Style.RESET_ALL}")
            print(f"    Category: {Fore.YELLOW}{category}{Style.RESET_ALL}")
            print()
            recommendations_dict[str(i)] = command
        
        print(f"{Fore.YELLOW}💡 Type the number (1-8) to execute a command, or enter your own description!{Style.RESET_ALL}\n")
        
        return recommendations_dict
    
    def print_help(self):
        """Print help information."""
        print(f"{Fore.GREEN}QuickCommand AI Assistant Help{Style.RESET_ALL}")
        print("─" * 50)
        print("Examples of natural language commands:")
        print(f"  • {Fore.CYAN}'command for remote group policy update'{Style.RESET_ALL}")
        print(f"  • {Fore.CYAN}'list all running services'{Style.RESET_ALL}")
        print(f"  • {Fore.CYAN}'install python package for web scraping'{Style.RESET_ALL}")
        print(f"  • {Fore.CYAN}'create a new directory and navigate to it'{Style.RESET_ALL}")
        print(f"  • {Fore.CYAN}'check disk space on C drive'{Style.RESET_ALL}")
        print()
        print("Commands:")
        print(f"  • {Fore.MAGENTA}help{Style.RESET_ALL} - Show this help message")
        print(f"  • {Fore.MAGENTA}recommendations{Style.RESET_ALL} - Show new command recommendations")
        print(f"  • {Fore.MAGENTA}exit/quit{Style.RESET_ALL} - Exit the assistant")
        print(f"  • {Fore.MAGENTA}settings{Style.RESET_ALL} - Show current settings")
        print()
    
    def show_settings(self):
        """Display current settings."""
        print(f"{Fore.GREEN}Current Settings:{Style.RESET_ALL}")
        print(f"  AI Provider: {Fore.CYAN}{self.settings.ai_provider.upper()}{Style.RESET_ALL}")
        print(f"  AI Model: {Fore.CYAN}{self.settings.ai_model}{Style.RESET_ALL}")
        print(f"  Default Shell: {Fore.CYAN}{self.settings.default_shell}{Style.RESET_ALL}")
        
        if self.settings.ai_provider == 'openai':
            api_configured = 'Yes' if self.settings.openai_api_key else 'No'
            print(f"  OpenAI API Key: {Fore.CYAN}{api_configured}{Style.RESET_ALL}")
        elif self.settings.ai_provider == 'gemini':
            api_configured = 'Yes' if self.settings.gemini_api_key else 'No'
            print(f"  Gemini API Key: {Fore.CYAN}{api_configured}{Style.RESET_ALL}")
        else:
            api_configured = 'Unknown'
        
        # Show PowerShell availability
        ps_available = 'Yes' if self.powershell.is_available else 'No'
        print(f"  PowerShell Available: {Fore.CYAN}{ps_available}{Style.RESET_ALL}")
        
        print()
    
    async def process_command(self, user_input: str) -> Optional[str]:
        """Process user input and generate command suggestion."""
        try:
            # Get AI suggestion
            print(f"{Fore.YELLOW}Thinking...{Style.RESET_ALL}")
            suggestion = await self.ai.suggest_command(user_input)
            
            if not suggestion:
                print(f"{Fore.RED}Sorry, I couldn't generate a command for that request.{Style.RESET_ALL}")
                return None
            
            # Display suggestion
            print(f"\n{Fore.GREEN}Command Suggestion:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{suggestion.get('command', 'No command generated')}{Style.RESET_ALL}")
            
            if suggestion.get('description'):
                print(f"\n{Fore.GREEN}Description:{Style.RESET_ALL}")
                print(f"{suggestion['description']}")
            
            if suggestion.get('warning'):
                print(f"\n{Fore.RED}⚠️  Warning:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{suggestion['warning']}{Style.RESET_ALL}")
            
            # Ask for confirmation
            while True:
                try:
                    choice = input(f"\n{Fore.YELLOW}Execute this command? (y/n/copy): {Style.RESET_ALL}").strip().lower()
                    
                    if choice in ['y', 'yes']:
                        return suggestion.get('command')
                    elif choice in ['n', 'no']:
                        print(f"{Fore.YELLOW}Command cancelled.{Style.RESET_ALL}")
                        return None
                    elif choice == 'copy':
                        try:
                            import pyperclip
                            pyperclip.copy(suggestion.get('command', ''))
                            print(f"{Fore.GREEN}Command copied to clipboard!{Style.RESET_ALL}")
                        except ImportError:
                            print(f"{Fore.YELLOW}Clipboard functionality not available. Install pyperclip: pip install pyperclip{Style.RESET_ALL}")
                        return None
                    else:
                        print(f"{Fore.RED}Please enter 'y' (yes), 'n' (no), or 'copy'.{Style.RESET_ALL}")
                except (EOFError, KeyboardInterrupt):
                    print(f"\n{Fore.YELLOW}Command cancelled.{Style.RESET_ALL}")
                    return None
        
        except Exception as e:
            print(f"{Fore.RED}Error processing command: {str(e)}{Style.RESET_ALL}")
            return None
    
    def execute_command(self, command: str):
        """Execute the approved command."""
        try:
            if self.settings.default_shell == "powershell":
                self.powershell.execute(command)
            elif self.settings.default_shell == "python":
                self.python_handler.execute(command)
            else:
                # Default to PowerShell on Windows
                self.powershell.execute(command)
        except Exception as e:
            print(f"{Fore.RED}Error executing command: {str(e)}{Style.RESET_ALL}")
    
    async def run_interactive(self):
        """Run the interactive command loop."""
        self.print_banner()
        
        # Show random recommendations on startup
        recommendations = self.show_recommendations()
        
        # Check if API key is configured
        api_key_configured = False
        if self.settings.ai_provider == 'openai' and self.settings.openai_api_key:
            api_key_configured = True
        elif self.settings.ai_provider == 'gemini' and self.settings.gemini_api_key:
            api_key_configured = True
            
        if not api_key_configured:
            provider_name = self.settings.ai_provider.upper()
            if self.settings.ai_provider == 'openai':
                key_name = "OPENAI_API_KEY"
            elif self.settings.ai_provider == 'gemini':
                key_name = "GEMINI_API_KEY"
            else:
                key_name = "API_KEY"
                
            print(f"{Fore.RED}⚠️  {provider_name} API key not configured!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please add to .env file: {key_name}=your_api_key_here{Style.RESET_ALL}\n")
        
        while True:
            try:
                # Get user input
                user_input = input(f"{Fore.BLUE}❯ {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit']:
                    print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                    break
                elif user_input.lower() == 'help':
                    self.print_help()
                    continue
                elif user_input.lower() == 'settings':
                    self.show_settings()
                    continue
                elif user_input.lower() == 'recommendations':
                    recommendations = self.show_recommendations()
                    continue
                
                # Check if input is a recommendation number
                if user_input in recommendations:
                    command = recommendations[user_input]
                    print(f"{Fore.CYAN}Selected command: {command}{Style.RESET_ALL}")
                    
                    # Show command details
                    print(f"{Fore.GREEN}Command:{Style.RESET_ALL} {Fore.WHITE}{command}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Description:{Style.RESET_ALL} Direct execution of recommended command")
                    
                    # Ask for execution confirmation
                    while True:
                        try:
                            choice = input(f"\n{Fore.YELLOW}Execute this command? (y/n/copy): {Style.RESET_ALL}").strip().lower()
                            
                            if choice in ['y', 'yes']:
                                print(f"{Fore.GREEN}Executing command...{Style.RESET_ALL}")
                                self.execute_command(command)
                                break
                            elif choice in ['n', 'no']:
                                print(f"{Fore.YELLOW}Command cancelled.{Style.RESET_ALL}")
                                break
                            elif choice == 'copy':
                                try:
                                    import pyperclip
                                    pyperclip.copy(command)
                                    print(f"{Fore.GREEN}Command copied to clipboard!{Style.RESET_ALL}")
                                except ImportError:
                                    print(f"{Fore.YELLOW}Clipboard functionality not available. Install pyperclip: pip install pyperclip{Style.RESET_ALL}")
                                break
                            else:
                                print(f"{Fore.RED}Please enter 'y' (yes), 'n' (no), or 'copy'.{Style.RESET_ALL}")
                        except (EOFError, KeyboardInterrupt):
                            print(f"\n{Fore.YELLOW}Command cancelled.{Style.RESET_ALL}")
                            break
                    
                    print()  # Add spacing
                    continue
                
                # Process the command
                command_to_execute = await self.process_command(user_input)
                
                if command_to_execute:
                    print(f"{Fore.GREEN}Executing command...{Style.RESET_ALL}")
                    self.execute_command(command_to_execute)
                
                print()  # Add spacing between interactions
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' or 'quit' to leave gracefully.{Style.RESET_ALL}")
            except EOFError:
                print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                break

@click.command()
@click.option('--shell', default='powershell', help='Default shell (powershell/python)')
@click.option('--model', default='gpt-3.5-turbo', help='AI model to use')
def main(shell: str, model: str):
    """QuickCommand AI Assistant - Natural language to smart commands."""
    try:
        import asyncio
        
        # Update settings based on CLI args
        os.environ['DEFAULT_SHELL'] = shell
        os.environ['AI_MODEL'] = model
        
        app = QuickCommand()
        asyncio.run(app.run_interactive())
        
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
