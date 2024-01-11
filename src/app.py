from flask import Flask, render_template, jsonify, request
import requests
import text2image
import chat
import os

from dotenv import load_dotenv
load_dotenv()
env = os.getenv('ENV')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def get_api_data():
    try:
        # Get the user-provided API URL from the query parameter
        post = request.args.get('post')
        # category = request.args.get('category')
        adjective = request.args.get('adjective')
        print(f"create {adjective} image for {post}")

        if env == "PROD":
            # Make an API call to get category from post
            category = chat.get_category_from_text(post)
            
            # Make an API call to get quote
            quote_response = chat.get_quote_from_category(category)
            quote = quote_response['quote']
            author = quote_response['author']
            
            # Make an API call to generate image
            image_url = text2image.generate_image(quote=quote, noun="pictogram", adjective=adjective)
        else:
            # Make an API call to get quote
            if lower(category) == "actionable":
                quote = "Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time."
                author = "Thomas Edison"
            elif lower(category) == "future":
                quote = "Dreams are brief madness and madness a long dream."
                author = "Arthur Schopenhauer"
            else:
                quote = None
                author = None

            # Make an API call to generate image
            image_url = f"http://127.0.0.1:5000/static/images/{category}_{adjective}.png"

        # Check if the API call was successful (status code 200)
        if quote and author and image_url:
            print(quote, image_url)
            return jsonify({'quote': quote, 'author': author, 'image_url': image_url})
        else:            
            return jsonify({'error': 'API request failed'}), 500  # Internal Server Error for failed requests

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
