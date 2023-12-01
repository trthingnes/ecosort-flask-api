import os
import time
from uuid import uuid1
from openai import AzureOpenAI
from database.db import ConversationManager

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

hana_host = os.getenv('HANA_HOST')
hana_port = os.getenv('HANA_PORT')
hana_user = os.getenv('HANA_USER')
hana_password = os.getenv("HANA_PASSWORD")

conversation_manager = ConversationManager(hana_host, hana_port, hana_user, hana_password)

last_request_time = time.time()
conversations = {}


def create_conversation():
    """Starts a new conversation by creating an ID and inserting the system/assistant message"""

    cleanup() # Delete all conversations in memory if no requests were made in the last while

    messages = [
        {"role": "system", "content": " ".join(INSTRUCTIONS)},
        {"role": "assistant", "content": INITIAL_MESSAGE},
    ]
    uuid = str(uuid1())
    conversation_id = conversation_manager.create_conversation(uuid)
    if not conversation_id:
        conversation_id = uuid
    conversations[str(conversation_id)] = messages

    return conversation_id, messages


def send_message_in_conversation(c_id: str, message: str):
    """Sends a new user message in the conversation and returns the assistant response"""

    cleanup() # Delete all conversations in memory if no requests were made in the last while

    # Add the users message to the list
    messages = conversations[str(c_id)]
    messages.append({"role": "user", "content": message})

    # Add the assistants response to the list
    completion = client.chat.completions.create(model=MODEL, messages=messages)
    response = completion.choices[0].message
    messages.append({"role": "assistant", "content": response.content})

    # Update the conversation with two new messages
    conversations[str(c_id)] = messages

    message_id = conversation_manager.add_message(c_id, message)
    response_id = conversation_manager.add_response(message_id, response.content)

    return c_id, messages


def cleanup():
    """Clear conversations if there has been no activity last 30 min"""
    global last_request_time
    if time.time() - last_request_time > 1800:
        conversations.clear()
        conversation_manager.close_connection()
        print("Cleared conversations from previous session")
    
    last_request_time = time.time()