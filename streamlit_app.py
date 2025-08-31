import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import openai
import io
import base64
import time
from audio_recorder_streamlit import audio_recorder
import requests
import json
import threading

# Page configuration
st.set_page_config(
    page_title="🤖 Azure Speech GPT Voice Bot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #4F46E5;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .status-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .status-idle {
        background-color: #E5E7EB;
        color: #374151;
    }
    
    .status-listening {
        background-color: #FEF3C7;
        color: #92400E;
    }
    
    .status-processing {
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    
    .status-speaking {
        background-color: #D1FAE5;
        color: #065F46;
    }
    
    .conversation-box {
        background-color: #F8FAFC;
        border: 2px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .user-text {
        background-color: #EBF4FF;
        border-left: 4px solid #3B82F6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .bot-text {
        background-color: #F0FDF4;
        border-left: 4px solid #10B981;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'status' not in st.session_state:
        st.session_state.status = "Idle"
    if 'user_text' not in st.session_state:
        st.session_state.user_text = ""
    if 'bot_response' not in st.session_state:
        st.session_state.bot_response = ""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'listening_active' not in st.session_state:
        st.session_state.listening_active = False
    if 'continuous_listening' not in st.session_state:
        st.session_state.continuous_listening = False
    if 'auto_listen_trigger' not in st.session_state:
        st.session_state.auto_listen_trigger = 0
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0

def get_azure_speech_config():
    """Get Azure Speech configuration from secrets"""
    try:
        subscription_key = st.secrets["AZURE_SPEECH_KEY"]
        service_region = st.secrets["AZURE_SPEECH_REGION"]
        return speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)
    except KeyError as e:
        st.error(f"Missing Azure Speech configuration: {e}")
        st.error("Please add AZURE_SPEECH_KEY and AZURE_SPEECH_REGION to your Streamlit secrets.")
        return None

def get_openai_config():
    """Get OpenAI configuration from secrets"""
    try:
        return {
            "endpoint": st.secrets["OPENAI_ENDPOINT"],
            "api_key": st.secrets["OPENAI_API_KEY"]
        }
    except KeyError as e:
        st.error(f"Missing OpenAI configuration: {e}")
        st.error("Please add OPENAI_ENDPOINT and OPENAI_API_KEY to your Streamlit secrets.")
        return None

def continuous_speech_recognition(speech_config, openai_config, placeholder_container):
    """Continuous speech recognition with immediate processing"""
    try:
        # Create audio configuration from default microphone
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        
        # Create a copy of speech config
        temp_config = speechsdk.SpeechConfig(subscription=speech_config.subscription_key, region=speech_config.region)
        temp_config.speech_recognition_language = "en-US"
        
        # Set optimized properties for continuous recognition
        temp_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "3000")
        temp_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "1000")
        temp_config.set_property(speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, "1000")
        
        # Create speech recognizer
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=temp_config,
            audio_config=audio_config
        )
        
        def recognized_handler(evt):
            """Handle recognized speech"""
            if evt.result.text.strip():
                user_text = evt.result.text.strip()
                
                with placeholder_container.container():
                    st.write(f"🗣️ You said: {user_text}")
                    
                    with st.spinner("Getting AI response..."):
                        # Get GPT response
                        bot_response = get_gpt_response(user_text, openai_config)
                        st.write(f"🤖 Bot: {bot_response}")
                        
                        # Generate audio response
                        audio_data = text_to_speech(bot_response, speech_config)
                        
                        # Add to conversation history
                        st.session_state.conversation_history.append({
                            "user": user_text,
                            "bot": bot_response,
                            "audio": audio_data,
                            "timestamp": time.time()
                        })
                        
                        # Play audio response
                        if audio_data:
                            st.audio(audio_data, format="audio/wav")
        
        # Set up event handlers
        speech_recognizer.recognized.connect(recognized_handler)
        
        # Start continuous recognition
        speech_recognizer.start_continuous_recognition()
        
        return speech_recognizer
        
    except Exception as e:
        return f"Continuous recognition error: {str(e)}"

def direct_microphone_recognition(speech_config):
    """Use Azure Speech SDK's direct microphone access for recognition"""
    try:
        # Create audio configuration from default microphone
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        
        # Create a copy of speech config
        temp_config = speechsdk.SpeechConfig(subscription=speech_config.subscription_key, region=speech_config.region)
        temp_config.speech_recognition_language = "en-US"
        
        # Set optimized properties
        temp_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "5000")
        temp_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "3000")
        
        # Create speech recognizer
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=temp_config,
            audio_config=audio_config
        )
        
        # Perform recognition
        result = speech_recognizer.recognize_once()
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text.strip() if result.text.strip() else "Empty recognition result."
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech detected. Please try again."
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                return f"Recognition error: {cancellation_details.error_details}"
            else:
                return f"Recognition canceled: {cancellation_details.reason}"
        else:
            return f"Unexpected result: {result.reason}"
            
    except Exception as e:
        return f"Direct microphone error: {str(e)}"

def speech_to_text(audio_data, speech_config):
    """Convert audio to text using Azure Speech Services with improved handling"""
    try:
        # Check if audio data is valid
        if not audio_data or len(audio_data) < 1000:  # Less than ~0.1 seconds of audio
            return "Audio too short or empty. Please record for at least 1-2 seconds."
        
        # Create a copy of speech config to avoid modifying the original
        temp_config = speechsdk.SpeechConfig(subscription=speech_config.subscription_key, region=speech_config.region)
        temp_config.speech_recognition_language = "en-US"
        
        # Set optimized properties for better recognition
        temp_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "5000")
        temp_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "2000")
        temp_config.set_property(speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, "2000")
        
        # Create audio stream and configuration
        audio_stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
        
        # Create speech recognizer
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=temp_config, 
            audio_config=audio_config
        )
        
        # Push audio data to the stream
        audio_stream.write(audio_data)
        audio_stream.close()
        
        # Perform recognition
        result = speech_recognizer.recognize_once()
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            if result.text.strip():
                return result.text.strip()
            else:
                return "Empty recognition result. Please speak more clearly."
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech detected. Please speak louder and more clearly."
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                return f"Recognition error: {cancellation_details.error_details}"
            else:
                return f"Recognition canceled: {cancellation_details.reason}"
        else:
            return f"Unexpected recognition result: {result.reason}"
        
    except Exception as e:
        return f"Error in speech recognition: {str(e)}"

def get_gpt_response(user_input, openai_config):
    """Get response from OpenAI GPT with optimized settings"""
    try:
        headers = {
            "Content-Type": "application/json",
            "api-key": openai_config["api_key"]
        }
        
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Keep responses concise and conversational."},
                {"role": "user", "content": user_input}
            ],
            "max_tokens": 150,  # Reduced for faster responses
            "temperature": 0.7,
            "stream": False
        }
        
        # Set timeout for faster failure detection
        response = requests.post(
            openai_config["endpoint"],
            headers=headers,
            json=data,
            timeout=10  # 10 second timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.Timeout:
        return "Response timeout. Please try again."
    except Exception as e:
        return f"Error getting GPT response: {str(e)}"

def text_to_speech(text, speech_config):
    """Convert text to speech using Azure Speech Services with optimization"""
    try:
        # Limit text length for faster synthesis
        if len(text) > 300:
            text = text[:300] + "..."
        
        # Create speech synthesizer with faster voice
        speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"  # Fast, natural voice
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        
        # Synthesize speech with timeout
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # Return audio data for playback
            return result.audio_data
        else:
            st.error(f"Speech synthesis failed: {result.reason}")
            return None
            
    except Exception as e:
        st.error(f"Error in text-to-speech: {str(e)}")
        return None

def display_status(status):
    """Display current status with styling"""
    status_class = {
        "Idle": "status-idle",
        "Listening...": "status-listening", 
        "Processing...": "status-processing",
        "Speaking...": "status-speaking"
    }.get(status, "status-idle")
    
    st.markdown(f'<div class="status-box {status_class}">Status: {status}</div>', 
                unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Azure Support Agent</h1>', 
                unsafe_allow_html=True)
    
    # Get configurations
    speech_config = get_azure_speech_config()
    openai_config = get_openai_config()
    
    if not speech_config or not openai_config:
        st.stop()
    
    # Status display
    display_status(st.session_state.status)
    
    # Always use direct microphone and continuous mode (simplified UX)
    use_direct_mic = True
    continuous_mode = True
    
    # Audio recording section
    st.markdown("### 🎤 Voice Interaction:")
    
    # Initialize variables
    audio_bytes = None
    user_text = None
    
    if continuous_mode:
        st.info("🔄 **Continuous Mode Active** - The bot is listening continuously. Just speak naturally!")
        
        # Update session state
        st.session_state.continuous_listening = True
        
        # Start/Stop continuous listening
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔴 Start Continuous Listening", type="primary"):
                st.session_state.listening_active = True
                st.rerun()
        with col2:
            if st.button("⏹️ Stop Listening"):
                st.session_state.listening_active = False
                st.rerun()
        
        # Continuous listening placeholder
        continuous_placeholder = st.empty()
        
        if st.session_state.listening_active:
            with continuous_placeholder.container():
                st.success("🎤 **Automatic Continuous Listening Active**")
                st.info("🔊 Speak naturally - I'll listen, respond, and automatically listen again!")
                
                # Auto-trigger listening cycle
                current_trigger = st.session_state.auto_listen_trigger
                
                # Show current status
                if st.session_state.status == "Idle":
                    st.markdown("🟢 **Ready to listen... Speak now!**")
                    
                    # Automatically start listening
                    with st.spinner("🎤 Listening... Speak now!"):
                        user_text = direct_microphone_recognition(speech_config)
                        
                    if user_text and "Error" not in user_text and "No speech" not in user_text and "Empty" not in user_text:
                        # Process the recognized speech
                        st.session_state.status = "Processing"
                        
                        with st.spinner("🤖 Processing your request..."):
                            # Get GPT response
                            bot_response = get_gpt_response(user_text, openai_config)
                            
                            # Generate audio
                            audio_data = text_to_speech(bot_response, speech_config)
                            
                            # Add to conversation history
                            st.session_state.conversation_history.append({
                                "user": user_text,
                                "bot": bot_response,
                                "audio": audio_data,
                                "timestamp": time.time()
                            })
                            
                            # Increment conversation count
                            st.session_state.conversation_count += 1
                            
                            # Display the conversation
                            st.write(f"🗣️ **You said:** {user_text}")
                            st.write(f"🤖 **Bot replied:** {bot_response}")
                            
                            # Play audio response
                            if audio_data:
                                st.audio(audio_data, format="audio/wav")
                                st.success(f"✅ Response #{st.session_state.conversation_count} complete! Automatically listening for your next message...")
                            else:
                                st.warning("⚠️ Audio generation failed, but text response is ready.")
                            
                            # Reset status and trigger next listening cycle
                            st.session_state.status = "Idle"
                            st.session_state.auto_listen_trigger += 1
                            
                            # Brief pause to let audio play, then auto-restart
                            time.sleep(2)
                            st.rerun()
                    else:
                        # Handle recognition errors
                        if "No speech" in user_text:
                            st.info("🔇 No speech detected. Listening again...")
                        else:
                            st.error(f"❌ Speech recognition issue: {user_text}")
                            st.info("🔄 Trying to listen again...")
                        
                        # Auto-retry after brief pause
                        time.sleep(1)
                        st.rerun()
                else:
                    # Show processing status
                    st.markdown(f"🟡 **Status:** {st.session_state.status}")
    else:
        st.info("💡 **Single Interaction Mode** - Click to record each message")
        
        if use_direct_mic:
            st.markdown("**Direct Microphone Mode**")
            if st.button("🎤 Start Listening", type="primary"):
                with st.spinner("Listening... Speak now!"):
                    user_text = direct_microphone_recognition(speech_config)
                    st.write(f"🗣️ Recognized: {user_text}")
        else:
            st.markdown("**Browser Recording Mode**")
            audio_bytes = audio_recorder(
                text="Click to record",
                recording_color="#e74c3c",
                neutral_color="#34495e",
                icon_name="microphone",
                icon_size="2x",
                key="audio_recorder"
            )
            
            # Show audio info for debugging
            if audio_bytes:
                st.write(f"📊 Audio data received: {len(audio_bytes)} bytes")
    
    # Process audio or direct speech recognition
    if audio_bytes or user_text:
        with st.spinner("Processing your voice..."):
            progress_bar = st.progress(0)
            
            # Get user text from either method
            if user_text is None:  # From audio recorder
                st.session_state.status = "Converting speech to text..."
                progress_bar.progress(25)
                user_text = speech_to_text(audio_bytes, speech_config)
                progress_bar.progress(50)
            else:  # From direct microphone
                progress_bar.progress(50)
            
            st.session_state.user_text = user_text
            
            if user_text and "Error" not in user_text and "No speech" not in user_text:
                # Get GPT response
                st.session_state.status = "Getting AI response..."
                progress_bar.progress(75)
                
                bot_response = get_gpt_response(user_text, openai_config)
                st.session_state.bot_response = bot_response
                
                # Convert response to speech (always enabled)
                st.session_state.status = "Generating audio..."
                progress_bar.progress(90)
                audio_data = text_to_speech(bot_response, speech_config)
                
                # Add to conversation history
                st.session_state.conversation_history.append({
                    "user": user_text,
                    "bot": bot_response,
                    "audio": audio_data,
                    "timestamp": time.time()
                })
                
                progress_bar.progress(100)
                st.session_state.status = "Idle"
                st.success("✅ Response ready!")
            else:
                st.session_state.status = "Idle"
                st.error(f"❌ Speech recognition issue: {user_text}")
        
        st.rerun()
    
    # Display conversation
    if st.session_state.conversation_history:
        st.markdown("### 💬 Conversation:")
        
        for i, conv in enumerate(reversed(st.session_state.conversation_history[-5:])):  # Show last 5 conversations
            with st.container():
                st.markdown(f'<div class="user-text"><strong>You said:</strong><br>{conv["user"]}</div>', 
                           unsafe_allow_html=True)
                st.markdown(f'<div class="bot-text"><strong>Bot replied:</strong><br>{conv["bot"]}</div>', 
                           unsafe_allow_html=True)
                
                # Play audio response
                if conv.get("audio"):
                    st.audio(conv["audio"], format="audio/wav")
                else:
                    st.warning("⚠️ Audio generation failed for this response")
                
                st.markdown("---")
    
    # Instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. **Click the microphone button** to start recording your voice
        2. **Speak clearly** into your microphone
        3. **Wait** for the AI to process your speech and generate a response
        4. **Listen** to the AI's spoken response
        5. **Repeat** for continued conversation
        
        **Note:** Make sure your microphone is enabled and you're in a quiet environment for best results.
        """)
    
    # Clear conversation button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.conversation_history = []
        st.session_state.user_text = ""
        st.session_state.bot_response = ""
        st.session_state.status = "Idle"
        st.rerun()

if __name__ == "__main__":
    main()
