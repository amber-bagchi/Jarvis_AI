from groq import Groq 
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")  # Load environment variables

Username = env_vars.get('Username')
AssistantName = env_vars.get('AssistantName')
GroqAPIKey = env_vars.get('GroqAPIKey')

client = Groq(api_key=GroqAPIKey)

# Define System Prompt
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatbot = [{"role": "system", "content": System}]

# Load previous messages or create an empty chat log if not exists
try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except (FileNotFoundError, ValueError):
    messages = []

def RealTimeInformation():
    """Returns real-time date and time information."""
    current_date_time = datetime.datetime.now()
    return f"""Please use this real-time information if needed:
Day: {current_date_time.strftime('%A')}
Date: {current_date_time.strftime('%d')}
Month: {current_date_time.strftime('%B')}
Year: {current_date_time.strftime('%Y')}
Time: {current_date_time.strftime('%H:%M:%S')}
"""

def AnswerModifier(Answer):
    """Cleans up the chatbot's response for better readability."""
    return "\n".join([line for line in Answer.split("\n") if line.strip()])

def ChatBot(Query):
    """Handles user queries and maintains chat history."""
    global messages  # Ensure we modify the global chat history

    try:
        # Append new user query to chat history
        messages.append({"role": "user", "content": Query})

        # Make a request to the Groq API
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatbot + [{"role": "system", "content": RealTimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        # Process response
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        # Append chatbot response to chat history
        messages.append({"role": "assistant", "content": Answer})

        # Save updated chat history to file
        with open("Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"Error: {e}")
        return "I encountered an error, please try again."

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))
