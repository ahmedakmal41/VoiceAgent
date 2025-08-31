# 🤖 Azure Speech GPT Voice Bot - Streamlit Version

This is a Streamlit implementation of the Azure Speech GPT Voice Bot that provides voice-to-voice conversation with AI.

## Features

- 🎤 **Voice Recording**: Record your voice directly in the browser
- 🗣️ **Speech-to-Text**: Convert your speech to text using Azure Speech Services
- 🤖 **AI Conversation**: Get intelligent responses from Azure OpenAI GPT-4
- 🔊 **Text-to-Speech**: Hear AI responses spoken back to you
- 💬 **Conversation History**: View your recent conversations
- 🎨 **Modern UI**: Clean, responsive interface with status indicators

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

1. Copy the `.streamlit/secrets.toml` file
2. Replace the placeholder values with your actual API keys:
   - `AZURE_SPEECH_KEY`: Your Azure Speech Services subscription key
   - `AZURE_SPEECH_REGION`: Your Azure Speech Services region (e.g., "eastus")
   - `OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
   - `OPENAI_API_KEY`: Your Azure OpenAI API key

### 3. Run the Application

```bash
streamlit run streamlit_app.py
```

## Azure Services Setup

### Azure Speech Services
1. Create an Azure Speech Services resource in the Azure portal
2. Get your subscription key and region
3. Add them to your secrets.toml file

### Azure OpenAI
1. Create an Azure OpenAI resource
2. Deploy a GPT-4 model
3. Get your endpoint URL and API key
4. Add them to your secrets.toml file

## Usage

1. **Start the App**: Run `streamlit run streamlit_app.py`
2. **Record Voice**: Click the microphone button to record your voice
3. **Wait for Processing**: The app will convert your speech to text, send it to GPT-4, and convert the response back to speech
4. **Listen to Response**: The AI's response will be played automatically
5. **Continue Conversation**: Record more audio to continue the conversation

## Security Notes

- API keys are stored securely in Streamlit secrets
- Never commit your actual API keys to version control
- The secrets.toml file contains placeholder values only

## Deployment Options

### Local Development
- Run locally using `streamlit run streamlit_app.py`

### Streamlit Cloud
1. Push your code to GitHub (without secrets.toml)
2. Deploy on Streamlit Cloud
3. Add your API keys in the Streamlit Cloud secrets management

### Other Platforms
- Can be deployed on any platform that supports Python and Streamlit
- Make sure to configure environment variables for API keys

## Troubleshooting

### Common Issues

1. **Microphone not working**: Ensure your browser has microphone permissions
2. **API errors**: Check that your API keys are correct and have proper permissions
3. **Audio playback issues**: Ensure your browser supports audio playback
4. **Speech recognition errors**: Speak clearly and ensure you're in a quiet environment

### Error Messages

- "Missing Azure Speech configuration": Check your AZURE_SPEECH_KEY and AZURE_SPEECH_REGION
- "Missing OpenAI configuration": Check your OPENAI_ENDPOINT and OPENAI_API_KEY
- "Speech recognition canceled": Usually indicates audio input issues

## Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Speech Processing**: Azure Cognitive Services Speech SDK
- **AI Processing**: Azure OpenAI GPT-4
- **Audio Handling**: audio-recorder-streamlit component

### Dependencies
- `streamlit`: Web application framework
- `azure-cognitiveservices-speech`: Azure Speech Services SDK
- `openai`: OpenAI API client (compatible with Azure OpenAI)
- `audio-recorder-streamlit`: Audio recording component
- `requests`: HTTP client for API calls

## Original Implementation

This Streamlit version is based on the original HTML/JavaScript implementation that used:
- Azure Speech SDK for browser
- Direct fetch API calls to Azure OpenAI
- Embedded JavaScript for audio handling

The Streamlit version provides the same functionality with improved security and deployment options.
