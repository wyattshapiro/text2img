import requests
import os
import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)


def generate_image(quote, noun, adjective=None):
    image_url = None
    if adjective:
        prompt = f"a {adjective} {noun} that represents the saying {quote}"
    else:
        prompt = f"a {noun} that represents the saying {quote}"
    print(prompt)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    # print(f"Generated Image URL: {image_url}")
    return image_url

def save_image(image_url, directory_path):
    # URL of the image you want to open
    try:
        # Send an HTTP GET request to fetch the image content
        response = requests.get(image_url)
        response.raise_for_status()  # Check for any errors in the HTTP request

        # Read the image content as bytes
        image_data = BytesIO(response.content)

        # Open the image using PIL (Pillow)
        img = Image.open(image_data)

        # Now you can work with the image using PIL functions
        # For example, you can display it:
        # img.show()
        image_url_safe = re.sub(r'[^a-zA-Z]+', '_', image_url[-10:])
        image_filename = f"{directory_path}/{image_url_safe}.jpg"
        img.save(image_filename)
        return image_filename
    except requests.exceptions.RequestException as e:
        print("Error fetching the image:", e)
    except Exception as e:
        print("An error occurred:", e)

def create_image_directory(quote):
    quote_safe = re.sub(r'[^a-zA-Z]+', '_', quote[0:30])
    directory_path = f"images/{quote_safe}"
    try:
        # Create the directory
        os.mkdir(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return directory_path

def create_grid(image_filenames, grid_size_col, grid_size_row):
    # Define the dimensions of the grid
    grid_size = (grid_size_col, grid_size_row)

    # Calculate the size of each grid cell based on the dimensions of the images
    image_width, image_height = Image.open(image_filenames[0]).size
    grid_width = image_width * grid_size[0]
    grid_height = image_height * grid_size[1]

    # Create a new blank image for the grid
    grid_image = Image.new("RGB", (grid_width, grid_height))

    # # Create a drawing context for adding text
    # draw = ImageDraw.Draw(grid_image)

    # # Use a font for the text (adjust the font size and style as needed)
    # font = ImageFont.load_default()

    # Iterate through the image filenames and paste each image into the grid
    for i, image_filename in enumerate(image_filenames):
        row = i // grid_size[0]
        col = i % grid_size[0]
        x = col * image_width
        y = row * image_height

        image = Image.open(image_filename)
        grid_image.paste(image, (x, y))

        # # Add the filename as text below the image
        # filename = os.path.basename(image_filename)
        # text_x = x
        # text_y = y + image_height
        # draw.text((text_x, text_y), filename, fill="white", font=font)

    # Save the grid image
    grid_image.save("grid_of_images.jpg")

    # Display the grid image
    grid_image.show()

def test_run(quote):
    adjectives = [None, "minimalist", "modern", "creative"]
    nouns = ["icon", "graphic", "pictogram"]
    image_filenames = []
    image_directory = create_image_directory(quote)
    for noun in nouns:
        for adjective in adjectives:
            image_url = generate_image(quote, noun, adjective)
            image_filename = save_image(image_url, image_directory)
            image_filenames.append(image_filename)

    # image_filenames = [os.path.join(image_directory, file_name) for file_name in os.listdir(image_directory)]
    print(image_filenames)
    create_grid(image_filenames, 4, 3)

if __name__ == '__main__':
    # quote = "Do not go where the path may lead, go instead where there is no path and leave a trail."
    # quote = "Most people don't finish things. Learn from the process and bring that to your next creation."
    # quote = "creativity flows much better when you aren't trying to strangle an income out of it" 
    # quote = "Success is the product of daily habits—not once-in-a-lifetime transformations."
    quote = "There is no greater danger than satisfaction."
    test_run(quote)