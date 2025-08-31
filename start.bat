@echo off
echo 🤖 Starting Azure Support Voice Bot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 🔍 Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if secrets file exists
if not exist ".streamlit\secrets.toml" (
    echo ⚠️  No secrets file found!
    echo Please create .streamlit\secrets.toml with your API keys
    echo.
    echo Example:
    echo AZURE_SPEECH_KEY = "your_key_here"
    echo AZURE_SPEECH_REGION = "your_region_here"
    echo OPENAI_ENDPOINT = "your_endpoint_here"
    echo OPENAI_API_KEY = "your_key_here"
    echo.
    pause
    exit /b 1
)

echo ✅ All checks passed!
echo 🚀 Starting Streamlit app...
echo 🌐 Your app will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo.

REM Start the Streamlit app
streamlit run streamlit_app.py

pause
