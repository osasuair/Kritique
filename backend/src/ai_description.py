from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
MODEL = 'gemini-2.0-flash-exp'

def summarize_comments(website: str, comments: list[str]) -> str:
    # Join the comments into a single string
    comments_text = "{" + ", ".join(comments) + "}"
    
    # Define the prompt for the AI
    prompt = f"Summarize the following comments for the website [{website}] in the third person with a limit of 30 words: {comments_text}"
    
    # Call the OpenAI API to get the summary
    response = client.models.generate_content(
        model=MODEL, 
        contents=prompt, 
        config={
            "temperature": 0.7,
            "maxOutputTokens": 100
        }
    )
    
    return response.text