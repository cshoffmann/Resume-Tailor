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

def main():
    """Main function to execute the script."""
    load_dotenv()  # Load environment variables from .env file
    client = create_openai_client()
    message = "Tell me this is a test. Also tell me a random joke"
    response = get_chat_response(client, message)
    
    # Print the response content
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
