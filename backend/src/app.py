import time
from flask import Flask, request
from components.helper import get_website_critique, post_critique, get_search_suggestions, add_website

app = Flask(__name__)

# # Dummy API endpoint
# @app.route('/time')
# def get_current_time():
#     return {'time': time.time()}

# Get Critique API endpoint with a param of the website
@app.route('/get_website_critique')
def get_critique():
    website = request.args.get('website')
    return get_website_critique(website)

# Post Critique API endpoint to add a critique to the a website's critique
@app.route('/post_critique', methods=['POST'])
def post_critique():
    website = request.json['website']
    comment = request.json['critique']
    return post_critique(website, comment)

@app.route('/add_website')
def add_site():
    domain = request.args.get('domain')
    return add_website(domain)

# Get Critique API endpoint with a param of the query
@app.route('/get_search_suggestions')
def getsSuggestions():
    query = request.args.get('query')
    return get_search_suggestions(query)