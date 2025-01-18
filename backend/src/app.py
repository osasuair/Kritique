import time
from flask import Flask, request
from components import helper

app = Flask(__name__)

# # Dummy API endpoint
# @app.route('/time')
# def get_current_time():
#     return {'time': time.time()}

# Get Critique API endpoint with a param of the website
@app.route('/get_website_critique')
def get_critique():
    website = request.args.get('website')
    return helper.get_website_critique(website)

# Post Critique API endpoint to add a critique to the a website's critique
@app.route('/post_critique', methods=['POST'])
def post_critique():
    return {'success': helper.post_critique(request.json)}