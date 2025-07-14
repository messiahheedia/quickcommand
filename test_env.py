#!/usr/bin/env python3
"""
Quick test to check environment variable loading.
"""

import os
from dotenv import load_dotenv

print("Testing environment variable loading...")
print(f"Current working directory: {os.getcwd()}")

# Load .env file
load_dotenv()

print("\nEnvironment variables after loading .env:")
print(f"AI_PROVIDER: {os.getenv('AI_PROVIDER')}")
print(f"AI_MODEL: {os.getenv('AI_MODEL')}")
print(f"GEMINI_API_KEY: {'***' if os.getenv('GEMINI_API_KEY') else 'None'}")
print(f"DEFAULT_SHELL: {os.getenv('DEFAULT_SHELL')}")

# Test settings
from config.settings import Settings
settings = Settings()

print(f"\nSettings after initialization:")
print(f"ai_provider: {settings.ai_provider}")
print(f"ai_model: {settings.ai_model}")
print(f"gemini_api_key: {'***' if settings.gemini_api_key else 'None'}")
print(f"default_shell: {settings.default_shell}")
