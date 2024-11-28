# backend/config_loader.py
import yaml
import os
import logging
import pprint
from dotenv import load_dotenv

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    logging.debug(f"Config path: {config_path}")
    
    with open(config_path, "r") as file:
        # Load the config.yaml file
        config = yaml.safe_load(file)
        
        # Get the project root directory. This needed to resolve any variables in the config file that contain 'PATH' realtive to
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # Resolve any variable in the config file that contains 'PATH' to fully qualified paths
        # This implies that all variables in the config file that contain paths need to have the word PATH in the name
        for key, value in config.items():
            if 'PATH' in key and isinstance(value, str):
                config[key] = os.path.abspath(os.path.join(project_root, value))

        # API Keys and other sensitive information should not be stored in the config.yaml file but in the .env file
        # Code below loads those sensitive variables specifically from the .env file and adds to the config object
        load_dotenv()
        for key, value in os.environ.items():
            config[key] = value
       
    logging.debug(f"Config content: {pprint.pformat(config)}")
    return config

if __name__ == "__main__":
    config = load_config()
    

