"""
Python command execution handler.
"""

import subprocess
import sys
import tempfile
import os
from typing import Optional
import colorama
from colorama import Fore, Style


class PythonHandler:
    """Handler for executing Python commands and scripts."""
    
    def __init__(self):
        """Initialize the Python handler."""
        # Try different Python commands available on Windows
        python_commands = [sys.executable, 'py', 'python', 'python3']
        self.python_executable = sys.executable
        
        # Check which Python command works
        for cmd in python_commands:
            try:
                result = subprocess.run([cmd, '--version'], capture_output=True, timeout=5)
                if result.returncode == 0:
                    self.python_executable = cmd
                    break
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        self.is_available = True  # Always available since we're running in Python
    
    def execute(self, command: str) -> None:
        """
        Execute a Python command or script.
        
        Args:
            command: The Python command/script to execute
        """
        try:
            print(f"{Fore.CYAN}Executing in Python:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}> {command}{Style.RESET_ALL}\n")
            
            # Check if it's a single line command or multi-line script
            if '\n' in command or command.strip().startswith('import ') or 'def ' in command:
                self._execute_script(command)
            else:
                self._execute_single_command(command)
                
        except Exception as e:
            print(f"{Fore.RED}Error executing Python command: {str(e)}{Style.RESET_ALL}")
    
    def _execute_single_command(self, command: str) -> None:
        """Execute a single Python command."""
        try:
            # For single commands, use python -c
            process = subprocess.Popen(
                [self.python_executable, '-c', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Stream output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            # Get any remaining output and errors
            stdout, stderr = process.communicate()
            
            # Print any remaining output
            if stdout:
                print(stdout.strip())
            
            # Handle errors
            if process.returncode != 0:
                print(f"\n{Fore.RED}Command failed with exit code {process.returncode}:{Style.RESET_ALL}")
                if stderr:
                    print(f"{Fore.RED}{stderr.strip()}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}Command completed successfully.{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Error executing single Python command: {str(e)}{Style.RESET_ALL}")
    
    def _execute_script(self, script: str) -> None:
        """Execute a multi-line Python script."""
        try:
            # Create a temporary file for the script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
                tmp_file.write(script)
                tmp_file_path = tmp_file.name
            
            try:
                # Execute the temporary script
                process = subprocess.Popen(
                    [self.python_executable, tmp_file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Stream output in real-time
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
                
                # Get any remaining output and errors
                stdout, stderr = process.communicate()
                
                # Print any remaining output
                if stdout:
                    print(stdout.strip())
                
                # Handle errors
                if process.returncode != 0:
                    print(f"\n{Fore.RED}Script failed with exit code {process.returncode}:{Style.RESET_ALL}")
                    if stderr:
                        print(f"{Fore.RED}{stderr.strip()}{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.GREEN}Script completed successfully.{Style.RESET_ALL}")
                    
            finally:
                # Clean up temporary file
                try:
                    os.unlink(tmp_file_path)
                except OSError:
                    pass
                    
        except Exception as e:
            print(f"{Fore.RED}Error executing Python script: {str(e)}{Style.RESET_ALL}")
    
    def validate_command(self, command: str) -> tuple[bool, Optional[str]]:
        """
        Validate Python code without executing it.
        
        Args:
            command: The Python code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Try to compile the code
            compile(command, '<string>', 'exec')
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
        except Exception as e:
            return False, f"Compilation error: {str(e)}"
    
    def get_shell_info(self) -> dict:
        """Get information about the Python environment."""
        return {
            "available": True,
            "executable": self.python_executable,
            "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": sys.platform,
            "implementation": sys.implementation.name
        }
    
    def install_package(self, package_name: str) -> bool:
        """
        Install a Python package using pip.
        
        Args:
            package_name: Name of the package to install
            
        Returns:
            True if installation was successful, False otherwise
        """
        try:
            print(f"{Fore.CYAN}Installing Python package: {package_name}{Style.RESET_ALL}")
            
            process = subprocess.run(
                [self.python_executable, '-m', 'pip', 'install', package_name],
                capture_output=True,
                text=True
            )
            
            if process.returncode == 0:
                print(f"{Fore.GREEN}Package '{package_name}' installed successfully.{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}Failed to install package '{package_name}':{Style.RESET_ALL}")
                print(f"{Fore.RED}{process.stderr.strip()}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}Error installing package: {str(e)}{Style.RESET_ALL}")
            return False
