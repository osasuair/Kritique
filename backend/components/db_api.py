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
        # Stage 1: Facet the results into two groups: recent and overall
        {
            "$facet": {
                "recent": [
                    # Stage 1a: Unwind the comments array
                    {"$unwind": "$comments"},
                    # Stage 1b: Filter comments within the last 24 hours
                    {
                        "$match": {
                            "comments.time": {"$gte": one_day_ago}
                        }
                    },
                    # Stage 1c: Group by domain and count comments
                    {
                        "$group": {
                            "_id": "$domain",
                            "count": {"$sum": 1}
                        }
                    },
                    # Stage 1d: Sort by count in descending order
                    {"$sort": {"count": -1}},
                    # Stage 1e: Limit to the top 10
                    {"$limit": 10}
                ],
                "overall": [
                    # Stage 2a: Unwind the comments array
                    {"$unwind": "$comments"},
                    # Stage 2b: Group by domain and count comments
                    {
                        "$group": {
                            "_id": "$domain",
                            "count": {"$sum": 1}
                        }
                    },
                    # Stage 2c: Sort by count in descending order
                    {"$sort": {"count": -1}},
                    # Stage 2d: Limit to the top 10
                    {"$limit": 10}
                ]
            }
        },
        # Stage 3: Project the results
        {
            "$project": {
                "top10": {
                    # Stage 3a: Conditionally choose the results
                    "$cond": [
                        {"$gte": [{"$size": "$recent"}, 10]},  # Check if there are at least 10 recent websites
                        "$recent",  # If yes, use the recent results
                        {
                            # If no, use the overall results and remove any that are in the recent results
                            "$setDifference": ["$overall", "$recent"]
                        }
                    ]
                }
            }
        },
        # Stage 4: Unwind the top10 array
        {"$unwind": "$top10"},
        # Stage 5: Replace the root with the top10 array
        {"$replaceRoot": {"newRoot": "$top10"}},
        # Stage 6: Limit to the top 10
        {"$limit": 10}
    ]

    top10Websites = list(db.websites.aggregate(pipeline))
    return top10Websites

def get_comments_and_reviews(website: str):
    """Get the comments for a website from the database.
    
    Args:
        website (str): The website for which to get the comments.
        
    Returns:
        list: A list of comments for the website.
    """
    
    # Get the comments for the website sorted by time
    comments_reviews = db.websites.find_one({"domain": website}, {"comments.text": 1, "rating": 1, "_id": 0})
    return comments_reviews

def update_website_rating(website: str, rating: int):
    """Update the rating for a website in the database.
    
    Args:
        website (str): The website for which to update the rating.
        rating (int): The new rating to update.
        
    Returns:
        bool: True if the rating was updated, False otherwise.
    """
    
    result = db.websites.update_one(
        {"domain": website},
        {"$set": {"rating": rating}}
    )

    return True if result.modified_count == 1 else False

def update_website_summary(website: str, summary: str):
    """Update the summary for a website in the database.
    
    Args:
        website (str): The website for which to update the summary.
        
    Returns:
        bool: True if the summary was updated, False otherwise.
    """
    
    result = db.websites.update_one(
        {"domain": website},
        {"$set": {"aiSummary": summary}}
    )

    return True if result.modified_count == 1 else False
    
def insert_website(website):
    db.websites.insert_one(website)
    

def get_search_suggestions(pipeline):
   return db.websites.aggregate(pipeline)