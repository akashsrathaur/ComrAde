import os
import subprocess
import speech_recognition as sr
import whisper
import warnings
import re

CONTRACTIONS = {
    r"\bI'm\b": "I am", r"\bi'm\b": "I am",
    r"\bI've\b": "I have", r"\bI'd\b": "I would", r"\bI'll\b": "I will",
    r"\bYou're\b": "You are", r"\byou're\b": "you are",
    r"\bYou've\b": "You have", r"\bYou'll\b": "You will",
    r"\bHe's\b": "He is", r"\bShe's\b": "She is", r"\bIt's\b": "It is", r"\bit's\b": "it is",
    r"\bWe're\b": "We are", r"\bThey're\b": "They are", r"\bThat's\b": "That is", r"\bWhat's\b": "What is",
    r"\bwho's\b": "who is", r"\bWho's\b": "Who is",
    r"\bDon't\b": "Do not", r"\bdon't\b": "do not",
    r"\bDoesn't\b": "Does not", r"\bdoesn't\b": "does not",
    r"\bDidn't\b": "Did not", r"\bdidn't\b": "did not",
    r"\bCan't\b": "Cannot", r"\bcan't\b": "cannot",
    r"\bWon't\b": "Will not", r"\bwon't\b": "will not",
    r"\bWouldn't\b": "Would not", r"\bwouldn't\b": "would not",
    r"\bShouldn't\b": "Should not", r"\bshouldn't\b": "should not",
    r"\bCouldn't\b": "Could not", r"\bcouldn't\b": "could not",
    r"\bIsn't\b": "Is not", r"\bisn't\b": "is not",
    r"\bAren't\b": "Are not", r"\baren't\b": "are not",
    r"\bWasn't\b": "Was not", r"\bwasn't\b": "was not",
    r"\bWeren't\b": "Were not", r"\bweren't\b": "were not",
    r"\bHaven't\b": "Have not", r"\bhaven't\b": "have not",
    r"\bHasn't\b": "Has not", r"\bhasn't\b": "has not",
    r"\bHadn't\b": "Had not", r"\bhadn't\b": "had not"
}

# Suppress some common warnings from PyTorch/Whisper about FP16
warnings.filterwarnings("ignore", category=UserWarning)

print("Loading local Whisper model (this may take a few seconds on the first run)...")
# "base.en" provides the best balance of extremely high accuracy and fast M2 speed
whisper_model = whisper.load_model("base.en")
print("Whisper model loaded.")

def speak(text: str):
    """
    Uses macOS built-in say command for fast Text-to-Speech (TTS).
    """
    # Clean the text slightly to avoid breaking the shell command
    clean_text = text.replace('"', '').replace("'", "")
    
    # Force expand all contractions since Llama 3 keeps trying to use them
    for pattern, replacement in CONTRACTIONS.items():
        clean_text = re.sub(pattern, replacement, clean_text)
        
    print(f"ComrAde says: {text}")
    
    # Generate speech using ultra-realistic Microsoft Edge Neural TTS (Global Female)
    subprocess.run(["edge-tts", "--voice", "en-US-AriaNeural", "--text", clean_text, "--write-media", "temp.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Play the file natively on macOS
    subprocess.run(["afplay", "temp.mp3"])

def listen_for_wake_word(recognizer: sr.Recognizer, microphone: sr.Microphone, wake_word: str = "comrade") -> bool:
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
        # Play a system sound to indicate the assistant is listening (Disabled since she now says 'Yes Boss!')
        # os.system('afplay /System/Library/Sounds/Ping.aiff')
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # Removed phrase_time_limit so she doesn't cut you off mid-sentence
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=None)
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
