import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
from core.audio import speak, listen_for_wake_word, listen_and_transcribe
from core.llm import get_llm_response
from core.parser import parse_and_execute
from core.briefing import get_morning_briefing
from core.ui import UltronUI
import speech_recognition as sr

class AudioWorker(QThread):
    state_changed = pyqtSignal(str, str) # state, message
    
    def run(self):
        print("Initializing ComrAde System...")
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        self.state_changed.emit("LISTENING", "Booting up...")
        speak("I am on.")
        self.state_changed.emit("SLEEPING", "")
        
        while True:
            try:
                # Passive listening
                woke = listen_for_wake_word(recognizer, microphone, wake_word="comrade")
                
                if woke:
                    self.state_changed.emit("SPEAKING", "Waking up...")
                    briefing = get_morning_briefing()
                    speak("Yes Boss!" + briefing)
                    
                    chat_history = []
                    
                    while True: # Active Session
                        self.state_changed.emit("LISTENING", "Listening...")
                        prompt = listen_and_transcribe(recognizer, microphone)
                        
                        if not prompt:
                            continue
                        
                        if "shutdown system" in prompt.lower() or "exit system" in prompt.lower():
                            self.state_changed.emit("SPEAKING", "Shutting down...")
                            speak("Shutting down completely.")
                            # Exit application
                            QApplication.quit()
                            return
                        
                        if any(word in prompt.lower() for word in ["bye", "go to sleep", "stop listening"]):
                            self.state_changed.emit("SPEAKING", "Sleeping...")
                            speak("Going back to sleep. Wake me if you need me!")
                            self.state_changed.emit("SLEEPING", "")
                            break 
                        
                        self.state_changed.emit("THINKING", "Thinking...")
                        raw_response = get_llm_response(prompt, chat_history)
                        
                        chat_history.append({"role": "user", "content": prompt})
                        chat_history.append({"role": "assistant", "content": raw_response})
                        if len(chat_history) > 10:
                            chat_history = chat_history[-10:]
                        
                        self.state_changed.emit("SPEAKING", "Speaking...")
                        spoken_response, executed_actions = parse_and_execute(raw_response)
                        
                        if spoken_response:
                            speak(spoken_response)
                            
                        for result in executed_actions:
                            if "[Web Search Result]" in result:
                                self.state_changed.emit("THINKING", "Reading search results...")
                                chat_history.append({"role": "user", "content": result})
                                follow_up = get_llm_response(result, chat_history)
                                chat_history.append({"role": "assistant", "content": follow_up})
                                
                                clean_follow_up, _ = parse_and_execute(follow_up)
                                if clean_follow_up:
                                    self.state_changed.emit("SPEAKING", "Speaking...")
                                    speak(clean_follow_up)
                
            except Exception as e:
                print(f"Audio loop error: {e}")
                self.state_changed.emit("SLEEPING", "")

def main():
    app = QApplication(sys.argv)
    
    # Initialize UI (hidden by default)
    ui = UltronUI()
    
    # Initialize background audio thread
    worker = AudioWorker()
    worker.state_changed.connect(ui.update_state)
    worker.start()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
