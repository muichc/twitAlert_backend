import os
import yaml

def process_yaml():
    cwd = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(cwd, 'config.yaml')
    with open(config_file) as file:
        return yaml.safe_load(file)

def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]