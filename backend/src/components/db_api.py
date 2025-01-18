from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv
from pymongo.errors import DuplicateKeyError

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@kritiquedb.fng36.mongodb.net/?retryWrites=true&w=majority&appName=kritiqueDB"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.kritiqueDB

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
def get_website_critique(website: str):
    """Get the critique for a website from the database. 
    If the website is not found, return None.
    
    Args:
        website (str): The website for which to get the critique.
        
    Returns:
        dict: The critique for the website. None if the website is not found.
    """
    
    # Connect to the database and get the critique sorted by _id
    websiteCritique = db.websites.find({"domain": website}, 
                                           {"_id": 0}
                                           ).sort("comments.time", 1).limit(1).to_list()
    
    return websiteCritique

def add_critique(website: str, comment: dict):
    """Add a critique for a website to the database.
    
    Args:
        website (str): The website for which to add the critique.
        critique (str): The critique to add.
        
    Returns:
        dict: The critique that was added.
    """
    
    result = db.websites.update_one(
        {"domain": website},
        {"$push": {"comments": comment}},
        upsert=True
    )
    
    return True if result.modified_count == 1 else False

def add_website(domain, rating=0.0, aiSummary="", tags=[], comments=[]):
    document = {
        "domain": domain,
        "rating": rating,
        "aiSummary": aiSummary,
        "tags": tags,
        "comments": comments,
    }
    try:
        result = collection.insert_one(document)
        return {"status": "Success", "document": document}
    except DuplicateKeyError:
        duplicate_document = website_exists(domain)
        return {"status": "Duplicate", "document": duplicate_document}
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"status": "Error", "message": str(e)}
    
def handle_user_input(domain):
    normalized_url = is_valid_url(domain)
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