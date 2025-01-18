from components import db_api
import validators
import datetime

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

def post_critique(comment: dict) -> bool:
    """Post a critique for a website to the database.
    
    Args:
        website (str): The website for which to post the critique.
        critique (str): The critique to post.
        
    Returns:
        dict: The critique that was posted.
    """
    
    # Pre-check if the website is valid
    if not is_valid_url(comment['website']):
        return None
    
    # Pre-check if the critique is valid
    if not validate_critique(comment['critique']):
        return None
    
    return db_api.add_critique(
        comment['website'], 
        {
            "text": comment['critique'],
            "rating": comment['rating'],
            "time": datetime.datetime.now()
        })
    
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

def is_valid_url(url):
    if type(url) is not str or str == "":
        return False
    if not url.startswith(("http://", "https://")):
        test_url = "https://" + url
    if validators.url(test_url):
        return True
    return False