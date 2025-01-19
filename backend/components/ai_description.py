import os
from dotenv import load_dotenv

from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from groq import Groq

import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
MODEL = 'gemini-2.0-flash-exp'
google_search_tool = Tool(
    google_search = GoogleSearch()
)

groqClient = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
    prompt = f"""
    Summarize the following user comments about the website [{website}] in a concise and informative way, limited to 30 words. 

    Focus on the main points of the feedback, and present the summary in the third person.

    Here are the comments:
    {comments_text}
    """    
    # Call the GenAI API to get the summary
    # response = client.models.generate_content(
    #     model=MODEL, 
    #     contents=prompt, 
    #     config=GenerateContentConfig(
    #         temperature=0.7,
    #         max_output_tokens=100
    #     )
    # )
    
    chat_completion = groqClient.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="gemma2-9b-it"
    )
    
    return chat_completion.choices[0].message.content

def validate_comment(comment: str) -> bool:
    """Validates a comment to check if it is appropriate and relevant.

    Args:
        comment (str): The comment to validate.

    Returns:
        bool: True if the comment is valid, False otherwise.
    """
    
    # Define the prompt for the AI
    prompt = f"""
    Analyze the following comment and determine if it violates any of the following rules:
    {comment}

    1. **No Profanity:** The comment must not contain any swear words or expletives.
    2. **Respectful Language:** The comment must not be offensive, discriminatory, or hateful towards any group or individual based on their background, identity, or beliefs.
    3. **Negative Responses:** The comment is allowed and will often express criticism or negative feedback, if it doesn't violate the other rules.
    
    If the comment violates any of these rules, return a JSON object like this: 
    {{"valid": false, "reason": "<A concise explanation of why the comment is invalid>"}}

    If the comment is acceptable, return a JSON object like this:
    {{"valid": true, "reason": "The comment is valid"}}
    
    Do not include any additional information in the response.

    Important: Only flag comments that clearly break the rules. Err on the side of allowing comments if they are borderline. 
    """
        
    # Call the GenAI API to get the validation
    chat_completion = groqClient.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="gemma2-9b-it"
    )
    
    response = chat_completion.choices[0].message.content
    
    if not "{" in response or not "}" in response:
        return {"invalid": "error"} 
    
    # 1. Find the indices of the first and last square brackets
    first_bracket = response.find('{')
    last_bracket = response.rfind('}')

    # 2. Splice the string to include the brackets
    json_string = response[first_bracket : last_bracket + 1]

    # 3. Parse the JSON string
    json_res = json.loads(json_string)
    
    # Check if the response contains the word "valid"
    return json_res

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