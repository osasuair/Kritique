from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
import validators

import os
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@kritiquedb.fng36.mongodb.net/?retryWrites=true&w=majority&appName=kritiqueDB"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["kritiqueDB"]
collection = db["websites"]

def is_valid_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    if validators.url(url):
        return url
    return None

def website_exists(domain):
    try:
        return collection.find_one({"domain": domain})
    except Exception as e:
        print(f"Error querying the database: {e}")
        return None

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