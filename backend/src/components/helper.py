from components import db_api

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