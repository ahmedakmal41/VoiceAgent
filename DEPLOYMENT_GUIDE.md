# 🚀 Quick Deployment Guide

## Prerequisites

Before deploying, make sure you have:

1. **Azure Speech Services** subscription and API key
2. **OpenAI API** access and endpoint
3. **Git** installed and configured
4. **Python 3.8+** installed

## 🎯 Option 1: Streamlit Cloud (Easiest)

### Step 1: Prepare Your Code
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Add your GitHub remote
git remote add origin <your-github-repo-url>
git push origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and branch
5. Set the path to `streamlit_app.py`
6. Add your secrets in the dashboard:
   - `AZURE_SPEECH_KEY`
   - `AZURE_SPEECH_REGION`
   - `OPENAI_ENDPOINT`
   - `OPENAI_API_KEY`
7. Click "Deploy!"

## 🎯 Option 2: Heroku

### Step 1: Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set AZURE_SPEECH_KEY=your_key
heroku config:set AZURE_SPEECH_REGION=your_region
heroku config:set OPENAI_ENDPOINT=your_endpoint
heroku config:set OPENAI_API_KEY=your_key

# Deploy
git push heroku main
```

## 🎯 Option 3: Docker

### Step 1: Build and Run
```bash
# Build image
docker build -t voicebot .

# Run container
docker run -p 8501:8501 voicebot
```

### Step 2: Use Docker Compose
```bash
# Start with docker-compose
docker-compose up

# Or run in background
docker-compose up -d
```

## 🎯 Option 4: Automated Deployment

### Run the deployment script
```bash
python deploy.py
```

This script will:
- Check prerequisites
- Set up Git repository
- Create secrets template
- Guide you through deployment options

## 🔐 Setting Up Secrets

### For Local Development
Create `.streamlit/secrets.toml`:
```toml
AZURE_SPEECH_KEY = "your_azure_speech_key"
AZURE_SPEECH_REGION = "your_azure_region"
OPENAI_ENDPOINT = "your_openai_endpoint"
OPENAI_API_KEY = "your_openai_api_key"
```

### For Production
- **Streamlit Cloud**: Use the dashboard
- **Heroku**: Use `heroku config:set`
- **Docker**: Use environment variables or `.env` file

## 🌐 Access Your App

After deployment, your app will be available at:
- **Streamlit Cloud**: `https://your-app-name.streamlit.app`
- **Heroku**: `https://your-app-name.herokuapp.com`
- **Docker**: `http://localhost:8501`

## 🐛 Troubleshooting

### Common Issues

1. **Microphone not working**
   - Ensure HTTPS in production
   - Check browser permissions

2. **API errors**
   - Verify API keys are correct
   - Check service quotas and limits

3. **Deployment failures**
   - Ensure all dependencies are in `requirements.txt`
   - Check platform-specific requirements

### Getting Help

- Check the logs in your deployment platform
- Verify environment variables are set correctly
- Test locally first with `streamlit run streamlit_app.py`

## 📊 Monitoring

- **Streamlit Cloud**: Built-in monitoring dashboard
- **Heroku**: Use `heroku logs --tail`
- **Docker**: Use `docker logs <container_id>`

## 🔄 Updates

To update your deployed app:
```bash
git add .
git commit -m "Update message"
git push origin main
```

The deployment platform will automatically detect changes and redeploy.

## 💰 Cost Considerations

- **Streamlit Cloud**: Free tier available
- **Heroku**: Free tier discontinued, paid plans start at $7/month
- **Azure Speech Services**: Pay-per-use, first 500K characters free monthly
- **OpenAI**: Pay-per-use, varies by model

## 🎉 Success!

Once deployed, your voice bot will be accessible worldwide! Users can:
- Speak naturally to interact with the bot
- Get intelligent responses from GPT
- Hear responses in natural voice
- Use continuous conversation mode

Remember to monitor usage and costs, especially for Azure Speech Services and OpenAI APIs.
