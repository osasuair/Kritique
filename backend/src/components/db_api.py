from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv
from pymongo.errors import DuplicateKeyError
import datetime
from datetime import timedelta

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

def get_top_10_websites(days: int = 1):
    """The top 10 trending websites based on the number of critiques in the last 24 hours from the database

    Returns:
        list: The top 10 websites based on the number of critiques in the last 24 hours.
    """

    # Calculate the timestamp for 24 hours ago
    one_day_ago = datetime.datetime.now() - timedelta(days=days)

    pipeline = [
        # Stage 1: Filter comments within the last 24 hours
        {
            "$match": {
                "comments.time": {"$gte": one_day_ago}
            }
        },
        # Stage 2: Unwind the comments array
        {"$unwind": "$comments"},
        # Stage 3: Filter comments again after unwinding
        {
            "$match": {
                "comments.time": {"$gte": one_day_ago}
            }
        },
        # Stage 4: Group by domain and count comments
        {
            "$group": {
                "_id": "$domain",
                "count": {"$sum": 1}
            }
        },
        # Stage 5: Sort by count in descending order
        {"$sort": {"count": -1}},
        # Stage 6: Limit to the top 10
        {"$limit": 10}
    ]

    top10Websites = list(db.websites.aggregate(pipeline))
    return top10Websites
    


    
def insert_website(website):
    db.websites.insert_one(website)
    

def get_search_suggestions(pipeline):
   return db.websites.aggregate(pipeline)