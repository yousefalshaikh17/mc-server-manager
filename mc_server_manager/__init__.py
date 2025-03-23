import os
from .server_manager import JavaServerManager
from dotenv import load_dotenv

__all__ = ["JavaServerManager",]

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