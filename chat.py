def forward_message_to_openai(conversation_id, message):
    is_new_conversation = conversation_id is None

    if is_new_conversation:
        pass # If the conversation is new, create a new conversation in the database.

    # Send the message and then send the response, keeping the conversation id intact.

    return { "conversation_id": conversation_id, "response": "This is ChatGPT's response to the message." }