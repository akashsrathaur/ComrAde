import re
import json
from typing import Tuple, List
from core.actions import open_app, close_app, change_volume, type_text, press_key, take_screenshot, web_search

def parse_and_execute(text: str) -> Tuple[str, List[str]]:
    """
    Looks for <ACTION>...</ACTION> tags, extracts JSON, executes the action, 
    and returns the clean text (to be spoken) along with action results.
    """
    clean_text = text
    results = []
    
    # Find all <ACTION> blocks
    pattern = r"<ACTION>(.*?)</ACTION>"
    matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        full_tag = match.group(0)
        json_str = match.group(1).strip()
        
        # Remove the tag from the text to be spoken
        clean_text = clean_text.replace(full_tag, "").strip()
        
        try:
            # Ensure proper quotes around keys if LLM messed it up occasionally
            action_data = json.loads(json_str)
            action_type = action_data.get("type")
            target = action_data.get("target") or action_data.get("query")
            
            if not action_type:
                continue
            
            
            print(f"\n[Action Parser] Intercepted request to: {action_type} -> {target}")
            
            if action_type == "open_app":
                res = open_app(target)
            elif action_type == "close_app":
                res = close_app(target)
            elif action_type == "change_volume":
                try:
                    res = change_volume(int(target))
                except ValueError:
                    res = "Volume target must be a number."
            elif action_type == "type_text":
                res = type_text(target)
            elif action_type == "press_key":
                res = press_key(target)
            elif action_type == "take_screenshot":
                res = take_screenshot()
            elif action_type == "web_search":
                res = web_search(target)
            else:
                res = f"Unknown action type: {action_type}"
                
            results.append(res)
            print(f"[Action Parser] Result: {res}\n")
            
        except json.JSONDecodeError:
            print(f"\n[Action Parser] Failed to parse action JSON: {json_str}\n")
            results.append("Failed to parse action.")
            
    return clean_text, results
