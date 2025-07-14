"""
AI-powered command generation using OpenAI and Google Gemini APIs.
"""

import json
import asyncio
from typing import Dict, Optional, Any
import openai
from openai import AsyncOpenAI

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from .prompts import SYSTEM_PROMPT, get_user_prompt
from config.settings import Settings


class CommandAI:
    """AI service for generating command suggestions using multiple providers."""
    
    def __init__(self, settings: Settings):
        """Initialize the AI service with settings."""
        self.settings = settings
        self.openai_client = None
        self.gemini_model = None
        
        # Initialize based on provider
        if self.settings.ai_provider == 'openai' and self.settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        elif self.settings.ai_provider == 'gemini' and self.settings.gemini_api_key and GEMINI_AVAILABLE:
            genai.configure(api_key=self.settings.gemini_api_key)
            # Use the correct model name for Gemini
            model_name = self.settings.ai_model if self.settings.ai_model.startswith('gemini') else 'gemini-pro'
            self.gemini_model = genai.GenerativeModel(model_name)
    
    async def suggest_command(self, user_request: str) -> Optional[Dict[str, Any]]:
        """
        Generate a command suggestion based on user's natural language request.
        
        Args:
            user_request: Natural language description of what the user wants to do
            
        Returns:
            Dictionary containing command, description, shell type, and optional warning
        """
        if self.settings.ai_provider == 'fallback':
            return self._get_fallback_suggestion(user_request)
        elif self.settings.ai_provider == 'openai' and self.openai_client:
            return await self._suggest_with_openai(user_request)
        elif self.settings.ai_provider == 'gemini' and self.gemini_model:
            return await self._suggest_with_gemini(user_request)
        else:
            return self._get_fallback_suggestion(user_request)
    
    async def _suggest_with_openai(self, user_request: str) -> Optional[Dict[str, Any]]:
        """Generate suggestion using OpenAI."""
        try:
            system_prompt = SYSTEM_PROMPT
            user_prompt = get_user_prompt(user_request, self.settings.default_shell)
            
            response = await self.openai_client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=500,
                timeout=30  # Add timeout
            )
            
            content = response.choices[0].message.content.strip()
            return self._parse_ai_response(content)
            
        except Exception as e:
            error_msg = str(e)
            print(f"OpenAI API Error: {error_msg}")
            
            # Check for specific error types and provide helpful messages
            if "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                print(f"💡 Your OpenAI API quota is exceeded. Check your billing at https://platform.openai.com/account/billing")
                print(f"   Falling back to enhanced pattern matching...")
            elif "invalid" in error_msg.lower() and "api" in error_msg.lower():
                print(f"🔑 API key issue. Please check your OpenAI API key in .env file")
            elif "timeout" in error_msg.lower():
                print(f"⏱️  Request timed out. Please try again.")
            
            return self._get_fallback_suggestion(user_request)
    
    async def _suggest_with_gemini(self, user_request: str) -> Optional[Dict[str, Any]]:
        """Generate suggestion using Google Gemini."""
        try:
            # Combine system prompt and user prompt for Gemini
            full_prompt = f"{SYSTEM_PROMPT}\n\n{get_user_prompt(user_request, self.settings.default_shell)}"
            
            # Generate content with Gemini
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                full_prompt
            )
            
            content = response.text.strip()
            return self._parse_ai_response(content)
            
        except Exception as e:
            print(f"Gemini API Error: {str(e)}")
            return self._get_fallback_suggestion(user_request)
    
    def _parse_ai_response(self, content: str) -> Optional[Dict[str, Any]]:
        """Parse AI response content."""
        # Try to parse as JSON first
        try:
            result = json.loads(content)
            return self._validate_suggestion(result)
        except json.JSONDecodeError:
            # If not JSON, try to extract command from text
            return self._parse_text_response(content)
    
    def _validate_suggestion(self, suggestion: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Validate and sanitize the AI suggestion."""
        if not isinstance(suggestion, dict) or 'command' not in suggestion:
            return None
        
        # Ensure required fields
        result = {
            'command': suggestion.get('command', '').strip(),
            'description': suggestion.get('description', ''),
            'shell': suggestion.get('shell', self.settings.default_shell),
            'warning': suggestion.get('warning', '')
        }
        
        # Basic safety checks
        dangerous_commands = ['rm -rf /', 'del /f /s /q', 'format', 'fdisk']
        command_lower = result['command'].lower()
        
        for dangerous in dangerous_commands:
            if dangerous in command_lower:
                result['warning'] = "⚠️ This command could be destructive. Please review carefully!"
        
        return result if result['command'] else None
    
    def _parse_text_response(self, content: str) -> Optional[Dict[str, Any]]:
        """Parse a text response that's not in JSON format."""
        lines = content.split('\n')
        command = ""
        description = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('Command:') or line.startswith('command:'):
                command = line.split(':', 1)[1].strip()
            elif line.startswith('Description:') or line.startswith('description:'):
                description = line.split(':', 1)[1].strip()
            elif not command and line and not line.startswith('#'):
                # If no explicit command marker, treat first non-comment line as command
                command = line
        
        if command:
            return {
                'command': command,
                'description': description,
                'shell': self.settings.default_shell,
                'warning': ''
            }
        
        return None
    
    def _get_fallback_suggestion(self, user_request: str) -> Optional[Dict[str, Any]]:
        """Provide intelligent fallback suggestions when AI is not available."""
        user_lower = user_request.lower()
        
        # Enhanced pattern matching with more intelligence
        suggestions = {
            # Group Policy
            ('group policy', 'gpo', 'policy update'): {
                'command': 'gpupdate /force',
                'description': 'Force Group Policy update on local machine',
                'shell': 'powershell'
            },
            ('remote group policy', 'remote gpo'): {
                'command': 'Invoke-GPUpdate -Computer "ComputerName" -Force',
                'description': 'Force Group Policy update on remote computer',
                'shell': 'powershell'
            },
            
            # Services
            ('running services', 'active services', 'list services'): {
                'command': 'Get-Service | Where-Object {$_.Status -eq "Running"} | Sort-Object Name',
                'description': 'List all running services sorted by name',
                'shell': 'powershell'
            },
            ('stopped services', 'inactive services'): {
                'command': 'Get-Service | Where-Object {$_.Status -eq "Stopped"} | Sort-Object Name',
                'description': 'List all stopped services',
                'shell': 'powershell'
            },
            ('start service', 'enable service'): {
                'command': 'Start-Service -Name "ServiceName"',
                'description': 'Start a specific service (replace ServiceName)',
                'shell': 'powershell'
            },
            ('stop service', 'disable service'): {
                'command': 'Stop-Service -Name "ServiceName"',
                'description': 'Stop a specific service (replace ServiceName)',
                'shell': 'powershell'
            },
            
            # Disk and Storage
            ('disk space', 'storage', 'free space', 'drive space'): {
                'command': 'Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID,@{Name="Size(GB)";Expression={[math]::Round($_.Size/1GB,2)}},@{Name="FreeSpace(GB)";Expression={[math]::Round($_.FreeSpace/1GB,2)}},@{Name="PercentFree";Expression={[math]::Round(($_.FreeSpace/$_.Size)*100,2)}}',
                'description': 'Show disk space with sizes in GB and percentage free',
                'shell': 'powershell'
            },
            ('c drive', 'c: drive', 'system drive'): {
                'command': 'Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID=\'C:\'" | Select-Object Size,FreeSpace',
                'description': 'Check C: drive space specifically',
                'shell': 'powershell'
            },
            
            # Processes
            ('running processes', 'process list', 'task list'): {
                'command': 'Get-Process | Sort-Object CPU -Descending | Select-Object -First 20 Name,CPU,WorkingSet,Id',
                'description': 'List top 20 processes by CPU usage',
                'shell': 'powershell'
            },
            ('kill process', 'stop process', 'end process'): {
                'command': 'Stop-Process -Name "ProcessName" -Force',
                'description': 'Kill a process by name (replace ProcessName)',
                'shell': 'powershell'
            },
            
            # Network
            ('network', 'ip config', 'network adapter', 'network interface'): {
                'command': 'Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | Select-Object Name,InterfaceDescription,LinkSpeed',
                'description': 'List active network adapters',
                'shell': 'powershell'
            },
            ('ip address', 'ip info'): {
                'command': 'Get-NetIPAddress | Where-Object {$_.AddressFamily -eq "IPv4" -and $_.IPAddress -ne "127.0.0.1"}',
                'description': 'Show IPv4 addresses (excluding localhost)',
                'shell': 'powershell'
            },
            ('ping', 'test connection'): {
                'command': 'Test-NetConnection -ComputerName "hostname" -Port 80',
                'description': 'Test network connectivity (replace hostname)',
                'shell': 'powershell'
            },
            
            # System Information
            ('system info', 'computer info', 'system details'): {
                'command': 'Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,TotalPhysicalMemory,CsProcessors',
                'description': 'Display basic system information',
                'shell': 'powershell'
            },
            ('uptime', 'system uptime'): {
                'command': '(Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime',
                'description': 'Show system uptime',
                'shell': 'powershell'
            },
            
            # Event Logs
            ('event log', 'system events', 'error log'): {
                'command': 'Get-EventLog -LogName System -Newest 20 | Where-Object {$_.EntryType -eq "Error"}',
                'description': 'Show latest 20 system errors',
                'shell': 'powershell'
            },
            ('application log', 'app events'): {
                'command': 'Get-EventLog -LogName Application -Newest 20',
                'description': 'Show latest 20 application events',
                'shell': 'powershell'
            },
            
            # File Operations
            ('create directory', 'new folder', 'mkdir', 'make directory'): {
                'command': 'New-Item -ItemType Directory -Name "NewFolder"',
                'description': 'Create a new directory (replace NewFolder with desired name)',
                'shell': 'powershell'
            },
            ('list files', 'directory listing', 'ls', 'dir'): {
                'command': 'Get-ChildItem | Sort-Object Name',
                'description': 'List files and folders in current directory',
                'shell': 'powershell'
            },
            ('find files', 'search files'): {
                'command': 'Get-ChildItem -Path . -Recurse -Filter "*.txt" | Select-Object Name,FullName,Length',
                'description': 'Find all .txt files recursively (change *.txt for other types)',
                'shell': 'powershell'
            },
            ('copy files', 'copy'): {
                'command': 'Copy-Item -Path "source" -Destination "destination" -Recurse',
                'description': 'Copy files/folders recursively',
                'shell': 'powershell'
            },
            
            # Python Package Management
            ('install package', 'pip install', 'python package'): {
                'command': 'pip install requests',
                'description': 'Install a Python package (replace requests with package name)',
                'shell': 'python'
            },
            ('list packages', 'pip list', 'installed packages'): {
                'command': 'pip list',
                'description': 'List all installed Python packages',
                'shell': 'python'
            },
            ('web scraping', 'scrape web'): {
                'command': 'pip install requests beautifulsoup4 lxml',
                'description': 'Install popular web scraping packages',
                'shell': 'python'
            },
            ('data analysis', 'data science'): {
                'command': 'pip install pandas numpy matplotlib seaborn',
                'description': 'Install data analysis packages',
                'shell': 'python'
            },
            
            # Windows Features
            ('windows features', 'optional features'): {
                'command': 'Get-WindowsOptionalFeature -Online | Where-Object {$_.State -eq "Enabled"}',
                'description': 'List enabled Windows optional features',
                'shell': 'powershell'
            },
            ('installed programs', 'software list'): {
                'command': 'Get-WmiObject -Class Win32_Product | Select-Object Name,Version | Sort-Object Name',
                'description': 'List installed programs',
                'shell': 'powershell'
            }
        }
        
        # Smart matching - find best match
        best_match = None
        best_score = 0
        
        for patterns, suggestion in suggestions.items():
            score = 0
            for pattern in patterns:
                if pattern in user_lower:
                    score += len(pattern)  # Longer matches get higher scores
            
            if score > best_score:
                best_score = score
                best_match = suggestion
        
        if best_match:
            return {
                'command': best_match['command'],
                'description': best_match['description'],
                'shell': best_match['shell'],
                'warning': 'Enhanced fallback suggestion - AI service not available'
            }
        
        # If no pattern matches, provide a helpful suggestion
        return {
            'command': f'# No specific pattern found for: "{user_request}"',
            'description': 'Try commands like "list services", "disk space", "system info", or "network adapters"',
            'shell': 'powershell',
            'warning': 'No matching pattern found - try being more specific'
        }
