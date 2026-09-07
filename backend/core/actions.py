import subprocess
import pyautogui

def execute_applescript(script: str) -> str:
    """Executes a piece of AppleScript using osascript."""
import time
import platform
import os
from datetime import datetime

def open_app(target: str) -> str:
    """Opens a specified application."""
    if not target:
        return "No application specified."
    try:
        if platform.system() == "Darwin":
            subprocess.run(["osascript", "-e", f'tell application "{target}" to activate'])
        elif platform.system() == "Windows":
            pyautogui.press("win")
            time.sleep(0.5)
            pyautogui.write(target)
            time.sleep(0.5)
            pyautogui.press("enter")
        return f"Opening {target}"
    except Exception as e:
        return f"Failed to open {target}: {e}"

def close_app(target: str) -> str:
    """Closes a specified application."""
    if not target:
        return "No application specified."
    try:
        if platform.system() == "Darwin":
            subprocess.run(["osascript", "-e", f'tell application "{target}" to quit'])
        elif platform.system() == "Windows":
            subprocess.run(["taskkill", "/IM", f"{target}.exe", "/F"])
        return f"Closing {target}"
    except Exception as e:
        return f"Failed to close {target}: {e}"

def change_volume(level: str) -> str:
    """Changes the system volume (0-100)."""
    try:
        vol = int(level)
        if platform.system() == "Darwin":
            subprocess.run(["osascript", "-e", f"set volume output volume {vol}"])
        elif platform.system() == "Windows":
            # Brute force volume to 0, then up to desired level (Windows steps by 2)
            for _ in range(50):
                pyautogui.press("volumedown")
            for _ in range(vol // 2):
                pyautogui.press("volumeup")
        return f"Volume set to {vol}%"
    except Exception as e:
        return f"Failed to set volume: {e}"

def type_text(text: str) -> str:
    """Types out the given text."""
    try:
        pyautogui.write(text, interval=0.01)
        return f"Typed: {text}"
    except Exception as e:
        return f"Failed to type: {e}"

def press_key(key: str) -> str:
    """Presses a specific key (e.g., 'enter', 'space', 'esc')."""
    try:
        pyautogui.press(key)
        return f"Pressed {key}"
    except Exception as e:
        return f"Failed to press {key}: {e}"

def take_screenshot(filename: str = "") -> str:
    """Takes a screenshot of the main screen."""
    try:
        os.makedirs("screenshots", exist_ok=True)
        if not filename:
            filename = f"screenshots/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return f"Screenshot saved to {filename}"
    except Exception as e:
        return f"Failed to take screenshot: {e}"

def web_search(query: str) -> str:
    """Searches the live internet for answers using duckduckgo-search."""
    try:
        from ddgs import DDGS
        results = DDGS().text(query, max_results=3)
        if not results:
            return "[Web Search Result]: No results found."
        
        snippets = [f"- {r['title']}: {r['body']}" for r in results]
        context = "\n".join(snippets)
        return f"[Web Search Result]: Here is the live data from the web:\n{context}\nPlease read this and give a natural, spoken answer."
    except Exception as e:
        return f"[Web Search Result]: Web search failed: {e}"
