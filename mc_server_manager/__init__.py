import os

from dotenv import load_dotenv

load_dotenv()

def get_mcrcon_path():
    # Check for environment variable path
    env_config_path = os.getenv('MCRCON_PATH')
    if env_config_path:
        return env_config_path

def load_config():
    config = {
        "mcrcon_path": None
    }

    path = get_mcrcon_path()
    if path:
        config['mcrcon_path'] = path
    
    return config

config = load_config()

def get_config():
    return config

__all__ = ["JavaServerManager","get_config"]

# Load after to stop circular import
from .server_manager import JavaServerManager