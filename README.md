# Jarvis AI - Intelligent Digital Assistant  

## 🔥 Overview
Jarvis AI is a powerful digital assistant designed to perform various tasks, including:
- **Speech Recognition**: Convert spoken words to text.
- **Text-to-Speech**: Convert text into natural-sounding speech.
- **Automation**: Perform system-level tasks like opening/closing applications, controlling volume, and cleaning the recycle bin.
- **Real-Time Search Engine**: Fetch real-time information from the web.
- **Chatbot**: Provide intelligent responses to user queries.
- **Image Generation**: Generate high-quality images using AI models.

## 🚀 Features

🎙 Speech-to-Text: Convert voice commands into text using the SpeechRecognition library.

🔊 Text-to-Speech: Speak responses using gTTS (Google Text-to-Speech).

🌐 Real-Time Search: Fetch live results using web scraping and Google Custom Search API.

🤖 AI Chatbot: Respond intelligently using an AI-based conversational model.

🖼 Image Generation: Generate images based on text prompts using an AI model.

🖥 System Automation:

- Open and close applications.

- Control system volume (mute, unmute, volume up, volume down).

- Clean up the recycle bin.

## 🛠️ Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/Jarvis_AI.git
   cd Jarvis_AI
   ```
2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv jarvis
   source jarvis/bin/activate  # On Windows: jarvis\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up API Keys**
 ```bash
   - GroqAPIKey=your_groq_api_key
   - HuggingFaceAPIKey=your_huggingface_api_key
   - AssistantName=Jarvis
   - Username=User
   ```

## 📂 Project Structure
```
Jarvis_AI/
│── Backend/
│   ├── Automation.py        # Handles system automation (volume control, recycle bin cleanup, etc.)
│   ├── Chatbot.py           # AI chatbot for user queries
│   ├── ImageGeneration.py   # AI-powered image generation
│   ├── Model.py             # Machine learning model for decision-making
│   ├── RealtimeSearchEngine.py  # Fetches real-time web search results
│   ├── SpeechToText.py      # Converts speech to text
│   ├── TextToSpeech.py      # Converts text to speech
│
│── Frontend/
│   ├── GUI.py               # Graphical User Interface
│   ├── Files/               # Stores temporary data files
│
│── Data/                    # Stores logs and generated images
│
│── main.py                  # Entry point for running the AI assistant
│── requirements.txt          # Dependencies
│── .env                      # API keys (not shared in the repo)
│── README.md                 # Documentation
```

## 🚀 Usage
Run the main script to start the AI assistant:
```bash
python main.py
```
### Example Commands:
- **"Increase volume"** → Increases system volume.
- **"Mute the sound"** → Mutes the system.
- **"Clean up the recycle bin"** → Empties the recycle bin.
- **"Search for the latest AI news"** → Fetches real-time news.
- **"Generate an image of a futuristic city"** → Creates an AI-generated image.

## 🤝 Contribution
Contributions are welcome! Feel free to fork the repo and submit pull requests.

## 📜 License
This project is licensed under the MIT License.

---
**Developed with ❤️ by Amber Bagchi**

