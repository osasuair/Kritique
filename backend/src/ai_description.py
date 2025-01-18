import os
from dotenv import load_dotenv

from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
MODEL = 'gemini-2.0-flash-exp'
google_search_tool = Tool(
    google_search = GoogleSearch()
)

def summarize_comments(website: str, comments: list[str]) -> str:
    """Summarizes a list of comments about a website using an AI model.

    Args:
        website (str): The website being reviewed.
        comments (list[str]): A list of comments about the website.

    Returns:
        str: A summary of the comments in the third person with a limit of 30 words.
    """
    
    # Join the comments into a single string
    comments_text = "{" + ", ".join(comments) + "}"
    
    # Define the prompt for the AI
    prompt = f"Summarize the following comments for the website [{website}] in the third person with a limit of 30 words: {comments_text}"
    
    # Call the GenAI API to get the summary
    response = client.models.generate_content(
        model=MODEL, 
        contents=prompt, 
        config=GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=100
        )
    )
    
    return response.text

def generate_tags_from_website(website: str) -> list[str]:
    """Generates relevant word-tags describing the purpose of a website using an AI model.
    
    Args:
        website (str): The website for which to generate tags.
        
    Returns:
        list[str]: A list of 6 relevant word-tags describing the purpose of the website. None if the website is not found.
    """

    # Define the prompt for the AI
    prompt = f"""
    Generate 6 relevant word-tags describing the purpose of the website: {website}
    With no Additional Context
    In json array format
    If you are unable to generate 6 tags, please generate as many as possible and make sure to close the array
    If you are unable to response, include the word "error" in the response
    Format: [tag1, tag2, tag3, tag4, tag5, tag6]
    """
    
    # Generate content using the AI model
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=GenerateContentConfig(
            tools=[google_search_tool],
            max_output_tokens=100,  # Increased for more detailed output
            response_modalities=["TEXT"]
        )
    )
    
    # Check if the response contains the word "error"
    if "error" in response.text:
        return None

    # Extract and return the tags
    # 1. Find the indices of the first and last square brackets
    first_bracket = response.text.find('[')
    last_bracket = response.text.rfind(']')

    # 2. Splice the string to include the brackets
    json_string = response.text[first_bracket : last_bracket + 1]

    # 3. Parse the JSON string
    tags = json.loads(json_string)
    return tags