import os
import subprocess
import speech_recognition as sr
import whisper
import warnings

# Suppress some common warnings from PyTorch/Whisper about FP16
warnings.filterwarnings("ignore", category=UserWarning)

print("Loading local Whisper model (this may take a few seconds on the first run)...")
# "base" model is a good tradeoff for speed and accuracy on M2
whisper_model = whisper.load_model("base")
print("Whisper model loaded.")

def speak(text: str):
    """
    Uses macOS built-in say command for fast Text-to-Speech (TTS).
    """
    # Clean the text slightly to avoid breaking the shell command
    clean_text = text.replace('"', '').replace("'", "")
    print(f"TiaRa says: {text}")
    # We use 'Samantha' as a default voice, but you can change this
    subprocess.run(["say", "-v", "Samantha", clean_text])

def listen_for_wake_word(recognizer: sr.Recognizer, microphone: sr.Microphone, wake_word: str = "tiara") -> bool:
    """
    Listens in the background for the wake word using lightweight SpeechRecognition.
    """
    print(f"\nListening for wake word ('{wake_word}')...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
        except sr.WaitTimeoutError:
            return False
    
    try:
        # Use simple Google STT here for quick wake-word catching
        # We don't use Whisper here to save resources while idling
        transcription = recognizer.recognize_google(audio).lower()
        if wake_word in transcription:
            return True
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass
    
    return False

def listen_and_transcribe(recognizer: sr.Recognizer, microphone: sr.Microphone) -> str:
    """
    Listens to the user's prompt and transcribes it locally using Whisper.
    """
    print("\nListening for your command...")
    with microphone as source:
        # Play a system sound to indicate the assistant is listening
        os.system('afplay /System/Library/Sounds/Ping.aiff')
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""
    
    print("Transcribing with local Whisper...")
    # Write audio to a temporary wav file for Whisper to process
    temp_filename = "temp_audio.wav"
    with open(temp_filename, "wb") as f:
        f.write(audio.get_wav_data())
    
    try:
        # Transcribe using Whisper (runs locally on M2)
        result = whisper_model.transcribe(temp_filename, fp16=False)
        text = result["text"].strip()
        print(f"You said: {text}")
        return text
    finally:
        # Clean up the temporary audio file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
