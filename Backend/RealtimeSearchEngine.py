from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")

# Retrieve chatbot credentials from .env file
Username = env_vars.get('Username')
AssistantName = env_vars.get('AssistantName')
GroqAPIKey = env_vars.get('GroqAPIKey')

# Initialize Groq API Client
client = Groq(api_key=GroqAPIKey)

# Define system instructions for the chatbot
System = f"""Hello, I am {Username}. You are {AssistantName}, an advanced AI with real-time search capability.
*** Always provide answers professionally with proper grammar, punctuation, and complete sentences. ***
*** Answer based on provided search data and past user inputs. ***
"""

# Load existing chat history from JSON file (or create an empty one)
try:
    with open(r"Data/ChatLog.json", "r") as f:
        messages = load(f)
except (FileNotFoundError, ValueError):
    messages = []

# Function to perform a Google search and return formatted results
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]"
    return Answer

# Function to clean up AI responses
def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

# Initial chatbot instructions & first interaction
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I assist you today?"}
]

# Function to fetch real-time date & time
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year =  current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use This Real-Time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds,\n"
    return data


# Function to handle user queries with search & memory retention
def RealtimeSearchEngine(prompt):
    global messages  # Ensure chat history persists

    # Load chat history again in case of updates
    try:
        with open(r"Data/ChatLog.json", "r") as f:
            messages = load(f)
    except (FileNotFoundError, ValueError):
        messages = []

    # Append user query to chat log
    messages.append({"role": "user", "content": prompt})

    # Perform Google search for real-time data
    search_results = GoogleSearch(prompt)

    # Construct message list including system prompt, search results, and chat history
    full_messages = SystemChatBot + [{"role": "system", "content": search_results}] + messages

    # Call Groq API for response
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=full_messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None
    )

    # Initialize answer variable
    Answer = ""

    # Process and construct AI response
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # Clean up response
    Answer = Answer.strip().replace("</s>", "")

    # Append chatbot's response to chat history
    messages.append({"role": "assistant", "content": Answer})

    # Save updated chat history to file
    with open(r"Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    return AnswerModifier(Answer)

# Main chatbot loop
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))