from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

import validators

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
                                           {"_id": 0, "comments._id": 0}
                                           ).sort("comments.time", 1).limit(1).to_list()
    
    return websiteCritique

def add_critique(website: str, critique: str):
    """Add a critique for a website to the database.
    
    Args:
        website (str): The website for which to add the critique.
        critique (str): The critique to add.
        
    Returns:
        dict: The critique that was added.
    """
    
    # Connect to the database and add the critique
    result = db.websites.update_one(
        {"domain": website},
        {"$push": {"critiques": critique}},
        upsert=True
    )
    
    return True if result.modified_count == 1 else False

def is_valid_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    if validators.url(url):
        return url
    return None


    
def insert_website(website):
    db.websites.insert_one(website)
    

def get_search_suggestions(pipeline):
   return db.websites.aggregate(pipeline)