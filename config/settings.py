"""
Application settings and configuration management.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Application settings configuration."""
    
    # AI Configuration
    ai_provider: str = "gemini"  # openai or gemini
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    ai_model: str = "gemini-pro"
    openai_model: str = "gpt-3.5-turbo"
    
    # Shell Configuration
    default_shell: str = "powershell"
    
    # Safety Configuration
    require_confirmation: bool = True
    enable_dangerous_commands: bool = False
    
    # Output Configuration
    use_colors: bool = True
    verbose_output: bool = False
    
    def __post_init__(self):
        """Initialize settings from environment variables."""
        # AI Settings
        self.ai_provider = os.getenv('AI_PROVIDER', self.ai_provider).lower()
        self.openai_api_key = os.getenv('OPENAI_API_KEY', self.openai_api_key)
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', self.gemini_api_key)
        self.openai_model = os.getenv('OPENAI_MODEL', self.openai_model)
        
        # Set AI model based on provider and explicit configuration
        ai_model_env = os.getenv('AI_MODEL')
        if ai_model_env:
            self.ai_model = ai_model_env
        elif self.ai_provider == 'gemini':
            self.ai_model = 'gemini-pro'
        elif self.ai_provider == 'openai':
            self.ai_model = 'gpt-3.5-turbo'
        
        # Shell Settings
        self.default_shell = os.getenv('DEFAULT_SHELL', self.default_shell).lower()
        
        # Safety Settings
        self.require_confirmation = os.getenv('REQUIRE_CONFIRMATION', 'true').lower() == 'true'
        self.enable_dangerous_commands = os.getenv('ENABLE_DANGEROUS_COMMANDS', 'false').lower() == 'true'
        
        # Output Settings
        self.use_colors = os.getenv('USE_COLORS', 'true').lower() == 'true'
        self.verbose_output = os.getenv('VERBOSE_OUTPUT', 'false').lower() == 'true'
        
        # Validate settings
        self._validate()
    
    def _validate(self):
        """Validate configuration settings."""
        # Validate AI provider
        valid_providers = ['openai', 'gemini', 'ollama', 'fallback']
        if self.ai_provider not in valid_providers:
            print(f"Warning: Invalid AI provider '{self.ai_provider}'. Using 'fallback' as default.")
            self.ai_provider = 'fallback'
        
        # Validate shell
        valid_shells = ['powershell', 'python']
        if self.default_shell not in valid_shells:
            print(f"Warning: Invalid shell '{self.default_shell}'. Using 'powershell' as default.")
            self.default_shell = 'powershell'
        
        # Validate AI models based on provider
        if self.ai_provider == 'openai':
            valid_models = [
                'gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo-preview', 
                'gpt-3.5-turbo-16k', 'gpt-4-32k'
            ]
            if self.ai_model not in valid_models:
                print(f"Warning: Unrecognized OpenAI model '{self.ai_model}'. This may not work as expected.")
        elif self.ai_provider == 'gemini':
            valid_models = ['gemini-pro', 'gemini-pro-vision']
            if self.ai_model not in valid_models:
                print(f"Warning: Unrecognized Gemini model '{self.ai_model}'. This may not work as expected.")
    
    def to_dict(self) -> dict:
        """Convert settings to dictionary."""
        return {
            'ai_provider': self.ai_provider,
            'openai_api_key': '***' if self.openai_api_key else None,
            'gemini_api_key': '***' if self.gemini_api_key else None,
            'ai_model': self.ai_model,
            'openai_model': self.openai_model,
            'default_shell': self.default_shell,
            'require_confirmation': self.require_confirmation,
            'enable_dangerous_commands': self.enable_dangerous_commands,
            'use_colors': self.use_colors,
            'verbose_output': self.verbose_output
        }
    
    @classmethod
    def from_file(cls, config_path: str) -> 'Settings':
        """Load settings from a configuration file."""
        # This could be extended to load from YAML/JSON config files
        # For now, we rely on environment variables and defaults
        return cls()
    
    def save_to_file(self, config_path: str) -> bool:
        """Save current settings to a configuration file."""
        try:
            import yaml
            with open(config_path, 'w') as f:
                yaml.dump(self.to_dict(), f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
