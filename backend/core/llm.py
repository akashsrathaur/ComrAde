import os
from openai import OpenAI

# Initialize the OpenAI client pointing to local Ollama instance
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # required by client, but unused by Ollama
)

def get_llm_response(prompt: str, system_prompt: str = "You are TiaRa, a highly capable, concise, and helpful AI desktop assistant.") -> str:
    """
    Sends the transcribed text to the local Ollama LLM and retrieves the response.
    """
    try:
        response = client.chat.completions.create(
            model="llama3", # Change this if you have a different model pulled, e.g., llama3.1
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150, # Keep it concise for faster voice output
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return "I'm sorry, I couldn't connect to my brain. Please make sure Ollama is running and the model is downloaded."
