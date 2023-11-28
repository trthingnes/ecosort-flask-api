import os
import time
from uuid import uuid1
from openai import AzureOpenAI


MODEL = "gpt-35-turbo"
INSTRUCTIONS = [
    "You are a friendly helpful chatbot named EcoSort who helps users recycle and sort their waste.",
    "Feel free to ask follow-up questions about the waste to more efficiently help the user.",
    "Answers should be maximum a few sentences long.",
    "Answers should specify what specific bin the waste belongs in, not just 'recycling bin'."
]
INITIAL_MESSAGE = (
    "Welcome to EcoSort! What type of waste are you trying to sort out today?"
)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)
last_request_time = time.time()
conversations = {}


def create_conversation():
    """Starts a new conversation by creating an ID and inserting the system/assistant message"""

    cleanup() # Delete all conversations in memory if no requests were made in the last while

    uuid = str(uuid1())
    messages = [
        {"role": "system", "content": " ".join(INSTRUCTIONS)},
        {"role": "assistant", "content": INITIAL_MESSAGE},
    ]
    conversations[uuid] = messages

    return uuid, messages


def send_message_in_conversation(uuid: str, message: str):
    """Sends a new user message in the conversation and returns the assistant response"""

    cleanup() # Delete all conversations in memory if no requests were made in the last while

    # Add the users message to the list
    messages = conversations[uuid]
    messages.append({"role": "user", "content": message})

    # Add the assistants response to the list
    completion = client.chat.completions.create(model=MODEL, messages=messages)
    response = completion.choices[0].message
    messages.append({"role": "assistant", "content": response.content})

    # Update the conversation with two new messages
    conversations[uuid] = messages

    return uuid, messages


def cleanup():
    """Clear conversations if there has been no activity last 30 min"""
    global last_request_time
    
    if time.time() - last_request_time > 1800:
        conversations.clear()
        print("Cleared conversations from previous session")
    
    last_request_time = time.time()