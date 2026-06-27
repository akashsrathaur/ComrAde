import speech_recognition as sr
from core.audio import speak, listen_for_wake_word, listen_and_transcribe
from core.llm import get_llm_response

def main():
    print("Initializing TiaRa System...")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    speak("TiaRa system is online and ready.")
    
    while True:
        try:
            # Step 1: Wait for wake word
            woke = listen_for_wake_word(recognizer, microphone, wake_word="tiara")
            
            if woke:
                # Step 2: Listen for the actual command
                prompt = listen_and_transcribe(recognizer, microphone)
                
                if not prompt:
                    continue
                
                # Check for exit commands
                if any(word in prompt.lower() for word in ["shutdown", "exit", "stop listening"]):
                    speak("Shutting down the system. Goodbye.")
                    break
                
                # Step 3: Get response from local LLM (Ollama)
                response = get_llm_response(prompt)
                
                # Step 4: Speak the response back
                speak(response)
                
        except KeyboardInterrupt:
            print("\nShutting down manually.")
            break
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")

if __name__ == "__main__":
    main()
