# PicturePerfect

A simple web app to generate a quote and accompanying image based on a text (ie. blog) input.


## Motivation

When a writer makes a blog post, the posts can do better when there is a visual. However, it is very time consuming to create a unique visual. So we want to augment the generation of visuals

An ideal outcome would include a visual that is a brain teaser because this makes it more engaging and shareable.

Example: An infographic based on a Winston Churchill quote.


## Resources
This project has the following key dependencies:

| Dependency Name | Documentation                | Description                                                                            |
|-----------------|------------------------------|----------------------------------------------------------------------------------------|
| Flask         | https://flask.palletsprojects.com/en/3.0.x/ | a lightweight and web framework for Python |
| OpenAI (ChatGPT, DALL-E)        | https://platform.openai.com/docs/api-reference | an artificial intelligence research lab and company that focuses on developing advanced AI technologies |
| Llama Index         | https://docs.llamaindex.ai/en/stable/ | a data framework for LLM-based applications to ingest, structure, and access private or domain-specific data |


## Quickstart

- Clone the repo locally
- $ python3 -m venv venv
- $ source venv/bin/activate
- $ pip install -r requirements.txt
- $ python3 app.py
- Access on localhost:5000