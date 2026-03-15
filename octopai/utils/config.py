import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Project configuration class"""
    
    # Cloudflare API configuration (optional)
    CLOUDFLARE_API_KEY = os.getenv('CLOUDFLARE_API_KEY', '')
    CLOUDFLARE_ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID', '')
    
    # OpenRouter API configuration (required)
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
    
    # Model configuration - Octopai uses latest proprietary models
    OCTOPAI_MODEL_PROVIDER = os.getenv('OCTOPAI_MODEL_PROVIDER', 'openrouter')
    OCTOPAI_MODEL = os.getenv('OCTOPAI_MODEL', 'openai/gpt-5.4')
    OCTOPAI_CLAUDE_MODEL = os.getenv('OCTOPAI_CLAUDE_MODEL', 'anthropic/claude-4.6')
    
    # Project configuration
    SKILLS_DIR = os.getenv('SKILLS_DIR', './skills')
    TEMP_DIR = os.getenv('TEMP_DIR', './temp')
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', './output')
    
    # Verbose mode
    OCTOPAI_VERBOSE = os.getenv('OCTOPAI_VERBOSE', '0').lower() in ('1', 'true', 'yes')
    
    # API endpoints
    @classmethod
    def get_cloudflare_markdown_api(cls):
        """Get Cloudflare Markdown API URL"""
        if cls.CLOUDFLARE_ACCOUNT_ID:
            return f"https://api.cloudflare.com/client/v4/accounts/{cls.CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/markdown/from-html"
        return None
    
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    @classmethod
    def validate(cls):
        """
        Validate if configuration is complete
        
        Raises:
            ValueError: If required configurations are missing
        """
        missing = []
        
        # OpenRouter API key is required
        if not cls.OPENROUTER_API_KEY:
            missing.append('OPENROUTER_API_KEY')
        
        if missing:
            raise ValueError(
                f"Missing required configurations: {', '.join(missing)}\n"
                f"Please copy .env.example to .env and fill in the values."
            )
        
        return True
    
    @classmethod
    def has_cloudflare(cls):
        """Check if Cloudflare configuration is available"""
        return bool(cls.CLOUDFLARE_API_KEY and cls.CLOUDFLARE_ACCOUNT_ID)
    
    @classmethod
    def get_info(cls):
        """Get configuration info summary"""
        return {
            'model_provider': cls.OCTOPAI_MODEL_PROVIDER,
            'model': cls.OCTOPAI_MODEL,
            'has_cloudflare': cls.has_cloudflare(),
            'skills_dir': cls.SKILLS_DIR,
            'verbose': cls.OCTOPAI_VERBOSE
        }
