import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

#Load Env 
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

#API KEY CHECK
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
try:
    gemini_client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    gemini_client = None

#-------------------
def generate_grounded_answer():
    #user_prompt = f"USER QUESTION: {query}"
    #full_prompt = context + user_prompt
    full_prompt  = "tell me who i am"

    #LLM Generation
    try:
        config = types.GenerateContentConfig(
            #system_instruction=system_instruction,
            temperature=0.2, 
            # Lower temperature for RAG responses factual and less creative
        )
        response = gemini_client.models.generate_content(
            model=MODEL_NAME,
            contents=[full_prompt],
            config=config,
        )
        return response.text
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return "An error occurred while generating the LLM response."

print(generate_grounded_answer())