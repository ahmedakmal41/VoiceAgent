#!/usr/bin/env python3
"""
Deployment script for Azure Support Voice Bot
Automates deployment to various platforms
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    tools = {
        'git': 'Git',
        'python': 'Python',
        'pip': 'Pip',
        'streamlit': 'Streamlit'
    }
    
    missing_tools = []
    
    for tool, name in tools.items():
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
            print(f"✅ {name} is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {name} is not installed")
            missing_tools.append(name)
    
    if missing_tools:
        print(f"\n⚠️  Please install: {', '.join(missing_tools)}")
        return False
    
    return True

def setup_git():
    """Initialize git repository if not already done"""
    if not Path('.git').exists():
        print("🔧 Setting up Git repository...")
        run_command('git init', 'Git initialization')
        run_command('git add .', 'Adding files to Git')
        run_command('git commit -m "Initial commit"', 'Initial commit')
    else:
        print("✅ Git repository already exists")

def deploy_streamlit_cloud():
    """Deploy to Streamlit Cloud"""
    print("\n🚀 Deploying to Streamlit Cloud...")
    
    # Check if remote exists
    result = subprocess.run('git remote -v', shell=True, capture_output=True, text=True)
    
    if 'origin' not in result.stdout:
        print("⚠️  No remote origin found. Please add your GitHub repository:")
        print("   git remote add origin <your-github-repo-url>")
        return False
    
    # Push to GitHub
    print("📤 Pushing to GitHub...")
    if run_command('git push origin main', 'Push to GitHub'):
        print("\n✅ Code pushed to GitHub successfully!")
        print("\n📋 Next steps for Streamlit Cloud:")
        print("1. Go to https://share.streamlit.io")
        print("2. Connect your GitHub account")
        print("3. Select this repository")
        print("4. Add your secrets in the dashboard:")
        print("   - AZURE_SPEECH_KEY")
        print("   - AZURE_SPEECH_REGION")
        print("   - OPENAI_ENDPOINT")
        print("   - OPENAI_API_KEY")
        print("5. Deploy!")
        return True
    
    return False

def deploy_heroku():
    """Deploy to Heroku"""
    print("\n🚀 Deploying to Heroku...")
    
    # Check if Heroku CLI is installed
    try:
        subprocess.run(['heroku', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Heroku CLI is not installed")
        print("Please install from: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Create Heroku app
    app_name = input("Enter your Heroku app name (or press Enter for auto-generated): ").strip()
    
    if not app_name:
        result = run_command('heroku create', 'Creating Heroku app')
        if result:
            app_name = result.strip().split('/')[-1].split('.')[0]
    else:
        run_command(f'heroku create {app_name}', 'Creating Heroku app')
    
    # Set environment variables
    print("🔐 Setting environment variables...")
    secrets = [
        'AZURE_SPEECH_KEY',
        'AZURE_SPEECH_REGION', 
        'OPENAI_ENDPOINT',
        'OPENAI_API_KEY'
    ]
    
    for secret in secrets:
        value = input(f"Enter {secret}: ").strip()
        if value:
            run_command(f'heroku config:set {secret}={value}', f'Setting {secret}')
    
    # Deploy
    if run_command('git push heroku main', 'Deploying to Heroku'):
        print(f"\n✅ Deployed to Heroku successfully!")
        print(f"🌐 Your app is available at: https://{app_name}.herokuapp.com")
        return True
    
    return False

def deploy_docker():
    """Deploy using Docker"""
    print("\n🐳 Deploying with Docker...")
    
    # Build Docker image
    if run_command('docker build -t voicebot .', 'Building Docker image'):
        print("\n✅ Docker image built successfully!")
        print("\n📋 To run your container:")
        print("docker run -p 8501:8501 voicebot")
        print("\n📋 Or use Docker Compose:")
        print("docker-compose up")
        return True
    
    return False

def create_secrets_template():
    """Create a template for secrets"""
    secrets_file = Path('.streamlit/secrets.toml')
    secrets_file.parent.mkdir(exist_ok=True)
    
    if not secrets_file.exists():
        template = '''# Azure Speech Services Configuration
AZURE_SPEECH_KEY = "your_azure_speech_key_here"
AZURE_SPEECH_REGION = "your_azure_region_here"

# OpenAI Configuration  
OPENAI_ENDPOINT = "your_openai_endpoint_here"
OPENAI_API_KEY = "your_openai_api_key_here"
'''
        secrets_file.write_text(template)
        print("📝 Created .streamlit/secrets.toml template")
        print("⚠️  Remember to add your actual API keys!")

def main():
    """Main deployment function"""
    print("🤖 Azure Support Voice Bot - Deployment Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Setup Git
    setup_git()
    
    # Create secrets template
    create_secrets_template()
    
    # Show deployment options
    print("\n🌐 Choose deployment option:")
    print("1. Streamlit Cloud (Recommended)")
    print("2. Heroku")
    print("3. Docker")
    print("4. All of the above")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    success = False
    
    if choice == '1':
        success = deploy_streamlit_cloud()
    elif choice == '2':
        success = deploy_heroku()
    elif choice == '3':
        success = deploy_docker()
    elif choice == '4':
        print("\n🚀 Deploying to all platforms...")
        success1 = deploy_streamlit_cloud()
        success2 = deploy_heroku()
        success3 = deploy_docker()
        success = success1 or success2 or success3
    else:
        print("❌ Invalid choice")
        sys.exit(1)
    
    if success:
        print("\n🎉 Deployment completed successfully!")
        print("\n📚 Check the README.md for detailed usage instructions")
    else:
        print("\n❌ Deployment failed. Check the error messages above")

if __name__ == "__main__":
    main()
