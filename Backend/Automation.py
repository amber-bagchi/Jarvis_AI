from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import os
import requests
import keyboard
import asyncio

env_vars = dotenv_values(".env")  # Load environment variables
GroqAPIKey = env_vars.get('GroqAPIKey')

# Define CSS Classes for parsing specific elements from HTML Content
classes = ["zCubwf", "hgkElc", "LTKOO sY7ric","Z0LCW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "IZ6rdc", "05uR6d LTK00", "vlzY6d",
            "tw-Data-text tw-text-small tw-ta", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
            "LWkfKe", "VQF4g", "qv3wpe", "kno-rdesc", "SPZz6b" ]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36'

# Initialize Groq API Client
client = Groq(api_key=GroqAPIKey)

# Predefined proffessional responses for user interactions.
professional_responses = [ "Your Satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
                          "I'm at your service for any additional questions or support you may need-don't hesitate to reach out.",]

messages = []

# System messages to provide context to the chatbot.
SystemChatBot  = [
    {"role": "system", "content": f"Hello, I am {os.environ['Username']}, You are a content writer. You have to write content like letters, emails, reports, articles, applications and anything else that you are asked to do."},
]

# Function to perform a google search
def GoogleSearch(Topic):
    search(Topic)
    return True

# Function to generate content using AI and save it to a file
def Content(Topic):
    
    # Nested function to open a file in Notepad
    def OpenNotepad(File):
        default_text_editor = "notepad.exe"
        subprocess.Popen([default_text_editor, File])
        
    # Nested Function to generate content using AI model
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"}) # Add the user prompt to message
        
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream= True,
            stop=None
        )
        
        Answer = ""
        
        # Process streamed response chuncks
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    Topic: str = Topic.replace("Content", "") # Remove 'Content' from the topic
    ContentByAI = ContentWriterAI(Topic)
    
    # Save the generated content to a text file
    with open(rf"Data/{Topic.lower().replace(' ', '')}.txt", "w", encoding='utf-8') as file:
        file.write(ContentByAI)
        file.close()
        
    OpenNotepad(rf"Data/{Topic.lower().replace(' ', '')}.txt")
    return True



def YouTubeSearch(Topic):
    Url4Serach = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Serach)
    return True

# Function to play a video
def PlayYoutube(query):
    playonyt(query)
    return True

# Function to open an app or relevant website
def OpenApp(app, sess=requests.session()):
    
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    
    except:
        # Nested Function to extract links from the HTML content.
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        # Nested Function to perform a google search and retrieve html content
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {'User-Agent': useragent}
            response = sess.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
            return None
        
        html = search_google(app) # Perform the Google search
        
        if html:
            link = extract_links(html)[0] # Extract the first link from the search results
            webopen(link)
        return True
    
    
# Function to close an application
def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False
        
# Function to execute system-level commands.
def System(command):
    
    # Nested Function to mute the system level volume
    def mute():
        keyboard.press_and_release("volume mute")
        
    def unmute():
        keyboard.press_and_release("volume mute")
        
    def volume_up():
        keyboard.press_and_release("volume up")
        
    def volume_down():
        keyboard.press_and_release("volume down")
        
    # Execute the provided command
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
        
    return True

# Async Function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):
    funcs = []
    
    for command in commands:
        
        if command.startswith("open "): # Handel open commands
            
            if "open it" in command: # Handel open it command
                pass
            
            if "open file" in command: # Handel open file command
                pass
            
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) # Schedule app opening
                funcs.append(fun)
                
        elif command.startswith("general "): # Handel general commands
            pass
            
        elif command.startswith("realtime "): # Handel realtime commands
            pass
            
        elif command.startswith("close "): # Handel close commands
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close ")) # Schedule app closing
            funcs.append(fun)
            
        elif command.startswith("play "): # Handel play commands
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play ")) # Schedule video playing
            funcs.append(fun)
            
        elif command.startswith("content "): # Handel content commands
            fun = asyncio.to_thread(Content, command.removeprefix("content ")) # Schedule content generation
            funcs.append(fun)
            
        elif command.startswith("youtube search "): # Handel youtube search commands
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")) # Schedule video playing
            funcs.append(fun)
            
        elif command.startswith("system "): # Handel system commands
            fun = asyncio.to_thread(System, command.removeprefix("system ")) # Schedule system commands
            funcs.append(fun)
            
        else:
            print(f"No Functions Found for: {command}")
            
    results = await asyncio.gather(*funcs) # Execute functions concurrently
    
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result
            
# Asynchronous Function to automate command execution
async def Automation(commands: list[str]):
    
    async for result in TranslateAndExecute(commands):
        pass
    
    return True # Indicate Sucess

