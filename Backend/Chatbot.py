from groq import Groq 
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env") #load enviroment variables

Username  = env_vars.get('Username')
AssistantName = env_vars.get('AssistantName')
GroqAPIKey = env_vars.get('GroqAPIKey')

client = Groq(api_key=GroqAPIKey)

message  = []

System  = """"""

SystemChatbot =  [
    {"role": "system", "content": System}
]

try:
    with open(r"Data\ChatLog.json", "r") as f:
        message = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
        
        
def RealTimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")