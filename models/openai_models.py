import requests
import json
import os
from utils.get_keys import load_config

config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'config.yaml') # Path to config file 
# the path is formated to be compatible with all operating systems
load_config(config_path)

class OpenAIModel:
    def __init__(self, model, system_prompt, temperature):
        self.model_endpoint = 'https://api.openai.com/v1/chat/completions'
        self.temperature = temperature
        self.model = model
        self.system_prompt = system_prompt
        load_config(config_path)
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }


    def generate_text(self, prompt):

        payload = {
                    "model": self.model,#"gpt-3.5-turbo",
                    "response_format": {"type": "json_object"}, # response format is used to specify the type of response we want from the model
                    "messages": [
                        {
                            "role": "system", # the role is used to specify the role of the message, either system or user
                            "content": self.system_prompt # the system prompt is used to provide context to the model
                        },
                        {
                            "role": "user", # the role is used to specify the role of the message, either system or user
                            "content": prompt # the user prompt is the input to the model
                        }
                    ],
                    "stream": False, # the stream parameter is used to specify if the response should be streamed or not
                    
                    "temperature": self.temperature,
                }
        
        response_dict = requests.post(self.model_endpoint, headers=self.headers, data=json.dumps(payload))
        response_json = response_dict.json()
        response = json.loads(response_json['choices'][0]['message']['content'])

        print(F"\n\nResponse from OpenAI model: {response}")

        return response 