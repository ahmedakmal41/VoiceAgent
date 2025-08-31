# 🤖 Azure Support Voice Bot

A conversational AI voice bot built with Streamlit that integrates Azure Speech Services for speech recognition and text-to-speech, along with OpenAI GPT for intelligent responses.

## ✨ Features

- 🎤 **Voice Input**: Record audio or use direct microphone input
- 🗣️ **Speech Recognition**: Convert speech to text using Azure Speech Services
- 🤖 **AI Responses**: Get intelligent responses from OpenAI GPT
- 🔊 **Text-to-Speech**: Hear the bot's responses in natural voice
- 🔄 **Continuous Mode**: Automatic listening and response cycles
- 💬 **Conversation History**: Track your chat history
- 🎨 **Modern UI**: Beautiful, responsive Streamlit interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Azure Speech Services subscription
- OpenAI API access
- Microphone access

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AzureSupportBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.streamlit/secrets.toml` file:
   ```toml
   AZURE_SPEECH_KEY = "your_azure_speech_key"
   AZURE_SPEECH_REGION = "your_azure_region"
   OPENAI_ENDPOINT = "your_openai_endpoint"
   OPENAI_API_KEY = "your_openai_api_key"
   ```

4. **Run locally**
   ```bash
   streamlit run streamlit_app.py
   ```

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Add your secrets in the Streamlit Cloud dashboard
   - Deploy!

### Option 2: Heroku

1. **Create Procfile**
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create runtime.txt**
   ```
   python-3.9.18
   ```

3. **Deploy to Heroku**
   ```bash
   heroku create your-app-name
   heroku config:set AZURE_SPEECH_KEY=your_key
   heroku config:set AZURE_SPEECH_REGION=your_region
   heroku config:set OPENAI_ENDPOINT=your_endpoint
   heroku config:set OPENAI_API_KEY=your_key
   git push heroku main
   ```

### Option 3: Railway

1. **Create railway.json**
   ```json
   {
     "build": {
       "builder": "nixpacks"
     },
     "deploy": {
       "startCommand": "streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0"
     }
   }
   ```

2. **Deploy on Railway**
   - Connect your GitHub repository
   - Add environment variables
   - Deploy automatically

### Option 4: Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run**
   ```bash
   docker build -t voicebot .
   docker run -p 8501:8501 voicebot
   ```

## 🔧 Configuration

### Azure Speech Services
- Get your subscription key from [Azure Portal](https://portal.azure.com)
- Set your region (e.g., `eastus`, `westeurope`)

### OpenAI
- Get your API key from [OpenAI Platform](https://platform.openai.com)
- Set your endpoint (e.g., `https://your-resource.openai.azure.com/openai/deployments/your-deployment/chat/completions?api-version=2023-05-15`)

## 📱 Usage

1. **Start the app** - Navigate to your deployed URL
2. **Enable microphone** - Allow browser access to your microphone
3. **Choose mode**:
   - **Continuous Mode**: Automatic listening and response cycles
   - **Single Mode**: Click to record each message
4. **Speak naturally** - The bot will process your speech and respond
5. **Listen to responses** - Hear the AI's spoken replies

## 🛠️ Customization

- **Voice**: Change `speech_synthesis_voice_name` in `text_to_speech()`
- **Language**: Modify `speech_recognition_language` in speech config
- **AI Behavior**: Update the system prompt in `get_gpt_response()`
- **UI**: Customize CSS styles in the `st.markdown()` section

## 🔒 Security Notes

- Never commit your API keys to version control
- Use environment variables or Streamlit secrets
- Consider implementing rate limiting for production use
- Monitor API usage and costs

## 📊 Monitoring

- Check Streamlit Cloud logs for errors
- Monitor Azure Speech Services usage
- Track OpenAI API consumption
- Set up alerts for high usage

## 🐛 Troubleshooting

### Common Issues

1. **Microphone not working**
   - Check browser permissions
   - Ensure HTTPS in production (required for microphone access)

2. **Azure Speech errors**
   - Verify subscription key and region
   - Check Azure service status

3. **OpenAI errors**
   - Verify API key and endpoint
   - Check rate limits and quotas

4. **Deployment issues**
   - Ensure all dependencies are in `requirements.txt`
   - Check port configuration for your hosting platform

## 📈 Scaling

- **Streamlit Cloud**: Automatically scales with traffic
- **Heroku**: Upgrade dynos for more resources
- **Railway**: Automatic scaling based on usage
- **Docker**: Deploy to Kubernetes for enterprise scaling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) for the amazing web app framework
- [Azure Speech Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/) for speech capabilities
- [OpenAI](https://openai.com) for AI language models
- [audio-recorder-streamlit](https://github.com/Joooohan/audio-recorder-streamlit) for audio recording component
