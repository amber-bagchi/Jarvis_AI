from AppOpener import close, open as appopen, give_appnames
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
import re
import ctypes
import os
import shutil
from send2trash import send2trash

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


def OpenApp(app):
    try:
        # Try opening the app locally
        from AppOpener import open as appopen
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        print(f"Failed to open '{app}' locally. Searching online...")

        def open_first_google_result(query):
            """ Uses Google's 'I'm Feeling Lucky' to open the first result directly and extracts the real URL. """
            google_search_url = f"https://www.google.com/search?q={query}+site+official&btnI=1"

            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(google_search_url, headers=headers, allow_redirects=False)  # Don't auto-follow redirects

            if response.status_code in [301, 302]:  # Google redirects
                redirected_url = response.headers.get("Location", "")

                # Extract the actual URL from Google's redirect URL
                match = re.search(r"q=(https?://[^\&]*)", redirected_url)
                if match:
                    final_url = match.group(1)
                    print(f"Redirected URL Found: {final_url}")
                    webbrowser.open(final_url)  # Open extracted URL
                    return True
                else:
                    print("Failed to extract final URL.")

            print("Failed to retrieve search results.")
            return False

        # Search and open the first result
        return open_first_google_result(app)
    
    
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

# Function to list all files and folders in a given directory
def list_files_and_folders(path):
    """List all files and folders in the specified directory"""
    if not os.path.exists(path):
        return f"❌ The folder '{path}' does not exist."

    items = os.listdir(path)
    return f"📂 Files and folders in {path}:\n" + "\n".join(items) if items else f"🚀 The folder '{path}' is empty."

#  Function to rename a file or folder
def rename_item(old_path, new_path):
    """Rename a file or folder"""
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return f"Renamed '{old_path}' to '{new_path}'."
    return f"Item '{old_path}' not found."

#  Function to move a file or folder
def move_item(src, dest):
    """Move a file or folder to a new location"""
    if os.path.exists(src):
        shutil.move(src, dest)
        return f" Moved '{src}' to '{dest}'."
    return f" '{src}' not found."

#  Function to delete a file or folder (moves to Recycle Bin)
def delete_item(path):
    """Delete a file or folder (sends to Recycle Bin)"""
    if os.path.exists(path):
        send2trash(path)  # Move to Recycle Bin
        return f" Moved '{path}' to Recycle Bin."
    return f" '{path}' not found."
   
# Function to empty the Recycle Bin
def empty_recycle_bin():
    """Empties the Windows Recycle Bin"""
    try:
        result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1)
        if result == 0:
            return "Recycle Bin has been cleaned successfully."
        else:
            return "Failed to clean the Recycle Bin."
    except Exception as e:
        return f"Error cleaning Recycle Bin: {str(e)}"

# Function to process system cleanup commands
def SystemAutomation(command):
    
    if "clean up recycle bin" in command:
        return empty_recycle_bin()
    return " Command not recognized."

     
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
            
        elif command.startswith("google search "): # Handel google search commands
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")) # Schedule google search
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

