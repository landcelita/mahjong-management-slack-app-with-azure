import logging
from slack_sdk.errors import SlackApiError

def delete_this_message(body, client):
    channel_id = body['container']['channel_id']
    message_ts = body['container']['message_ts']
    try:
        result = client.chat_delete(
            channel=channel_id,
            ts=message_ts
        )
    except SlackApiError as e:
        logging.error(f"Error deleting message: {e}")

def generate_option_dicts(texts, values):
    ret = []
    for i in range(len(texts)):
        ret.append({
            "text": {"type": "plain_text", "text": texts[i], "emoji": True},
            "value": values[i]
        })
    return ret

def confirm_button(value, action_id):
    return {
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": "確定",
            "emoji": True
        },
        "value": value,
        "action_id": action_id
    }