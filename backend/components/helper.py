from components import db_api, ai_description
from pymongo.errors import DuplicateKeyError
import validators
import datetime
import random
import requests

def get_website_critique(website: str) -> dict:
    """Get the critique for a website from the database. 
    If the website is not found, return None.
    
    Args:
        website (str): The website for which to get the critique.
        
    Returns:
        dict: The critique for the website. None if the website is not found.
    """
    
    # Pre-check if the website is valid
    if not is_valid_url(website):
        return None
    
    website_critique = db_api.get_website_critique(website)
    
    return website_critique

def post_critique(comment: dict) -> dict:
    """Post a critique for a website to the database.
    
    Args:
        website (str): The website for which to post the critique.
        critique (str): The critique to post.
        
    Returns:
        dict: The critique that was posted.
    """
    website = comment.get("website", None)
    
    # Pre-check if the website is valid
    if not is_valid_url(website):
        return None
    
    # Pre-check if the critique is valid
    validation_result = ai_description.validate_comment(comment['critique'])
    if str(validation_result.get("valid", False)).lower() == "false":  # Use .get() for safety
        return validation_result  # Return the validation result directly

    validation_result = db_api.add_critique(
        website,
        {
            "text": comment['critique'],
            "rating": comment['rating'],
            "time": datetime.datetime.now()
        }
    )
    if not validation_result:
        return {"valid": False}
    
    comment_and_rating = db_api.get_comments_and_reviews(website)
    website_rating = comment_and_rating.get("rating", 0)
    comments = comment_and_rating.get("comments")
    numRatings = len(comments)
    
    # Calculate the new rating
    newRating = (website_rating * (numRatings-1) + comment['rating']) / numRatings
    db_api.update_website_rating(website, newRating),

    # Get a random sample of 100 comments or all comments if less than 100
    random_comments = comments if len(comments) <= 100 else random.sample(comments, 100)
    comments = [comment["text"] for comment in random_comments]
    
    # Update the summary
    if len(comments) < 6 or numRatings % 5 == 0:
        new_summary = ai_description.summarize_comments(website, comments)
        db_api.update_website_summary(website, new_summary)
    return {"valid": True}  # Indicate successful posting

def get_top_10_websites() -> list:
    """Get the top 10 websites from the database.
    
    Returns:
        list: The top 10 trending websites based on the number of critiques in the last 24 hours.
    """
    
    top10 = db_api.get_top_10_websites(days=7)
    
    top10List = []
    for website in top10:
        top10List.append(website["_id"])
        
    return top10List
    
def validate_critique(critique: str) -> bool:
    """Validate a critique.
    
    Args:
        critique (str): The critique to validate.
        
    Returns:
        bool: True if the critique is valid, False otherwise.
    """
    
    # Pre-check if the critique is valid
    if critique is None or critique == "":
        return False
    
    return True

def add_website(domain):
    # Validate the domain
    if not is_valid_url(domain):
        print(f"Invalid URL: {domain}")
        return {"status": "Invalid URL"}

    # Check if the domain already exists in the collection
    existing_website = db_api.find_website({"domain": domain}) 
    if existing_website:
        print(f"Website already exists in the database: {domain}")
        return {"status": "Duplicate"}
    
    document = {
        "domain": domain,
        "rating" : 0.0,
        "aiSummary": ai_description.summarize_comments(domain, ai_description.generate_tags_from_website(domain)),
        "tags": ai_description.generate_tags_from_website(domain),
        "comments": ["comments"],
    }
    try:
        db_api.insert_website(document)
        print(f"New website created in the database: {domain}", "Go to Rating Page")
        return {"status": "Success"}
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"status": "Error:", "message": str(e)}
    
def handle_user_input(domain):
    normalized_url = db_api.is_valid_url(domain)
    if not normalized_url:
        return f"Invalid website URL. Please enter a valid URL."

    # Website already exists check & add website
    response = add_website(normalized_url)
    if response["status"] == "Duplicate":
        print(f"Website already exists in the database: {response['document']}")
        return f"Proceed to the rating page for {normalized_url}"
    elif response["status"] == "Success":
        print(f"New website created in the database: {normalized_url}")
        return f"Proceed to the rating page for {normalized_url}"
    else:
        return f"An error occurred: {response.get('message', 'Unknown error')}"
    
def get_search_suggestions(query):
    pipeline = [
        {
            "$search": {
                "index": "default",  
                "autocomplete": {
                    "query": query,  
                    "path": "domain",  
                    "fuzzy": {         
                        "maxEdits": 1  # Allow up to 2 character changes
                    }
                }
            }
        },
        {
            "$limit": 5 
        }
    ]
    
    cursor = db_api.get_search_suggestions(pipeline)

    # This convert the cursor to a list of suggestions
    return [{"domain": result["domain"]} for result in cursor]

def is_valid_url(url):
    # Check for a non-empty string input
    if not isinstance(url, str) or url.strip() == "":
        return False

    # Normalize the URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Validate the URL format
    if not validators.url(url):
        return False

    # Check if the URL is reachable
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 400
    except requests.RequestException:
        return False

