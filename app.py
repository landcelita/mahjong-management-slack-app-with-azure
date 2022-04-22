import logging
import os
from sqlcrud import exec_insert_sql, exec_select_sql, exec_update_sql, exec_delete_sql
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient


logging.basicConfig(level=logging.INFO)

client = WebClient(os.environ["SLACK_BOT_TOKEN"])

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.message("ゲームスタート")
def message_gamestart(message, say):
    init()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Test block with users select"
                },
                "accessory": {
                    "type": "users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a user",
                        "emoji": True
                    },
                    "action_id": "users_select-action"
                }
            }
        ]
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    ack()
    say(f"<@{body['user']['id']}> clicked the button")

from flask import Flask, request

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

def init():
    game_id = exec_insert_sql("GameStatus", [1, 1, 0, 0], ["Ba", "Kyoku", "Honba", "Finished"])
    exec_insert_sql("Point", [game_id, 25000, 25000, 25000, 25000])
    exec_insert_sql("Participants", [game_id, None, None, None, None])

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)