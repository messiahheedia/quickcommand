"""
PowerShell command execution handler.
"""

import subprocess
import sys
from typing import Optional
import colorama
from colorama import Fore, Style


class PowerShellHandler:
    """Handler for executing PowerShell commands."""
    
    def __init__(self):
        """Initialize the PowerShell handler."""
        self.is_available = self._check_powershell_availability()
    
    def _check_powershell_availability(self) -> bool:
        """Check if PowerShell is available on the system."""
        try:
            # Try both pwsh (PowerShell Core) and powershell (Windows PowerShell)
            for cmd in ['powershell', 'pwsh']:  # Try Windows PowerShell first
                try:
                    result = subprocess.run(
                        [cmd, '-Command', 'Write-Host "test"'], 
                        capture_output=True, 
                        text=True, 
                        timeout=10,  # Increased timeout
                        shell=False
                    )
                    if result.returncode == 0:
                        self.ps_command = cmd
                        print(f"{Fore.GREEN}PowerShell detected: {cmd}{Style.RESET_ALL}")
                        return True
                except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
                    print(f"{Fore.YELLOW}PowerShell {cmd} not available: {e}{Style.RESET_ALL}")
                    continue
            print(f"{Fore.RED}No PowerShell executable found{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}Error checking PowerShell availability: {e}{Style.RESET_ALL}")
            return False
    
    def execute(self, command: str) -> None:
        """
        Execute a PowerShell command.
        
        Args:
            command: The PowerShell command to execute
        """
        if not self.is_available:
            print(f"{Fore.RED}PowerShell is not available on this system.{Style.RESET_ALL}")
            return
        
        try:
            print(f"{Fore.CYAN}Executing in PowerShell ({self.ps_command}):{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}> {command}{Style.RESET_ALL}\n")
            
            # Execute the command using a simpler approach
            result = subprocess.run(
                [self.ps_command, '-Command', command],
                capture_output=True,
                text=True,
                timeout=30,
                shell=False
            )
            
            # Print output
            if result.stdout:
                print(result.stdout.strip())
            
            # Handle errors
            if result.returncode != 0:
                print(f"\n{Fore.RED}Command failed with exit code {result.returncode}:{Style.RESET_ALL}")
                if result.stderr:
                    print(f"{Fore.RED}{result.stderr.strip()}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}Command completed successfully.{Style.RESET_ALL}")
                
        except subprocess.TimeoutExpired:
            print(f"{Fore.RED}Command timed out.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error executing PowerShell command: {str(e)}{Style.RESET_ALL}")
    
    def validate_command(self, command: str) -> tuple[bool, Optional[str]]:
        """
        Validate a PowerShell command without executing it.
        
        Args:
            command: The PowerShell command to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.is_available:
            return False, "PowerShell is not available"
        
        try:
            # Use PowerShell's built-in syntax checking
            result = subprocess.run(
                [self.ps_command, '-Command', f'[ScriptBlock]::Create("{command}")'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return True, None
            else:
                return False, result.stderr.strip()
                
        except Exception as e:
            return False, str(e)
    
    def get_shell_info(self) -> dict:
        """Get information about the PowerShell environment."""
        if not self.is_available:
            return {"available": False}
        
        try:
            # Get PowerShell version
            result = subprocess.run(
                [self.ps_command, '-Command', '$PSVersionTable.PSVersion.ToString()'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            version = result.stdout.strip() if result.returncode == 0 else "Unknown"
            
            return {
                "available": True,
                "command": self.ps_command,
                "version": version,
                "type": "PowerShell Core" if self.ps_command == "pwsh" else "Windows PowerShell"
            }
            
        except Exception:
            return {
                "available": True,
                "command": self.ps_command,
                "version": "Unknown",
                "type": "Unknown"
            }
