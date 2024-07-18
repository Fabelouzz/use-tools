import os
import yaml 

def load_config(file_path): # Load config file
    with open(file_path, 'r') as file: # Open file
        config = yaml.safe_load(file) # Load file
        for key, value in config.items(): # Iterate over config items
            os.environ[key] = value # Set environment variable