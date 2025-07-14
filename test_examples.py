"""
Example usage and test cases for QuickCommand AI Assistant.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai.command_ai import CommandAI
from config.settings import Settings

async def test_command_suggestions():
    """Test the AI command suggestion functionality."""
    
    # Initialize settings and AI
    settings = Settings()
    ai = CommandAI(settings)
    
    # Test cases
    test_cases = [
        "command for remote group policy update",
        "list all running services",
        "check disk space on C drive",
        "install python package for web scraping", 
        "create a new directory and navigate to it",
        "find all text files in current directory",
        "show network adapters",
        "list logged on users"
    ]
    
    print("QuickCommand AI Assistant - Test Cases")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{test_case}'")
        print("-" * 40)
        
        try:
            suggestion = await ai.suggest_command(test_case)
            
            if suggestion:
                print(f"Command: {suggestion['command']}")
                print(f"Description: {suggestion['description']}")
                print(f"Shell: {suggestion['shell']}")
                if suggestion.get('warning'):
                    print(f"Warning: {suggestion['warning']}")
            else:
                print("No suggestion generated")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print(f"\n{'=' * 50}")
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_command_suggestions())
