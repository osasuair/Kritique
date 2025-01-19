from components import db_api, ai_description
from pymongo.errors import DuplicateKeyError

def get_website_critique(website: str) -> dict:
    """Get the critique for a website from the database. 
    If the website is not found, return None.
    
    Args:
        website (str): The website for which to get the critique.
        
    Returns:
        dict: The critique for the website. None if the website is not found.
    """
    
    # Pre-check if the website is valid
    if not validate_website(website):
        return None
    
    website_critique = db_api.get_website_critique(website)
    
    return website_critique

def post_critique(website: str, critique: str) -> bool:
    """Post a critique for a website to the database.
    
    Args:
        website (str): The website for which to post the critique.
        critique (str): The critique to post.
        
    Returns:
        dict: The critique that was posted.
    """
    
    # Pre-check if the website is valid
    if not validate_website(website):
        return None
    
    # Pre-check if the critique is valid
    if not validate_critique(critique):
        return None
    
    return db_api.add_critique(website, critique)

def validate_website(website: str) -> bool:
    """Validate a website.
    
    Args:
        website (str): The website to validate.
        
    Returns:
        bool: True if the website is valid, False otherwise.
    """
    
    # Pre-check if the website is valid
    if website is None or website == "":
        return False
    
    return True

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
    document = {
        "domain": domain,
        "rating" : 0.0,
        "aiSummary": ai_description.summarize_comments(domain, ai_description.generate_tags_from_website(domain)),
        "tags": ai_description.generate_tags_from_website(domain),
        "comments": "comments",
    }
    try:
        db_api.insert_website(document)
        print(f"New website created in the database: {domain}", "Go to Rating Page")
        return {"status": "Success"}
    except DuplicateKeyError:
        print(f"Website already exists in the database")
        return {"status": "Duplicate"}
    except Exception as e:
        print(f"Error occurred: {e}")
        # return {"status": "Error", "message": str(e)}
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