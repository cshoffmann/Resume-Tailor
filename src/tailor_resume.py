"""
tailor_resume.py

This module provides functions to interact with the OpenAI API to tailor resume content.
It includes functions to create an OpenAI client, get chat responses from the API, and
tailor the resume experience by generating customized content.

Functions:
- create_openai_client(): Creates and returns an OpenAI client using the API key from environment variables.
- get_chat_response(client, message, model="gpt-3.5-turbo"): Gets a chat response from the OpenAI API.
- tailor_experience(): Main function to execute the script, which loads environment variables, creates an OpenAI client,
  sends a message to the API, and returns the response content.

Expected Return:
- The `tailor_experience` function returns the content of the chat response from the OpenAI API.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

def create_openai_client():
    """Create and return an OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
    return OpenAI(api_key=api_key)

def get_chat_response(client, message, model="gpt-3.5-turbo"):
    """Get a chat response from the OpenAI API."""
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": message}],
        model=model,
    )
    return chat_completion

def tailor_experience():
    """Main function to execute the script."""
    load_dotenv()  # Load environment variables from .env file
    client = create_openai_client()
    message = "Tell me this is a test. Also tell me a random joke"
    response = get_chat_response(client, message)
    
    # Return the response
    response = response.choices[0].message.content
    return(response)
