import json
import logging
import os
import pprint
import urllib
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
        {
	"blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "ゲームを開始します",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "block_id": "tonpu_or_hanchan",
                    "label": {
                        "type": "plain_text",
                        "text": "東風戦or半荘戦",
                        "emoji": True
                    },
                    "element": {
                        "type": "radio_buttons",
                        "action_id": "radio",
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "東風戦",
                                    "emoji": True
                                },
                                "value": "1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "半荘戦",
                                    "emoji": True
                                },
                                "value": "2"
                            }
                        ]
                    }
                },
                {
                    "type": "section",
                    "block_id": "player1",
                    "text": {
                        "type": "mrkdwn",
                        "text": "東家"
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
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "南家"
                    },
                    "block_id": "player2",
                    "accessory": {
                        "type": "users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a user",
                            "emoji": True
                        },
                        "action_id": "users_select-action"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "西家"
                    },
                    "block_id": "player3",
                    "accessory": {
                        "type": "users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a user",
                            "emoji": True
                        },
                        "action_id": "users_select-action"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "北家"
                    },
                    "block_id": "player4",
                    "accessory": {
                        "type": "users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a user",
                            "emoji": True
                        },
                        "action_id": "users_select-action"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "確定",
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "action_id": "actionId-confirm-players"
                        }
                    ]
                }
            ]
        }
    )

@app.action("actionId-confirm-players")
def handle_confirm_players(ack, body, say):
    ack()
    tonpu_or_hanchan = body['state']['values']['tonpu_or_hanchan']['radio']['selected_option']
    player1Id = body['state']['values']['player1']['users_select-action']['selected_user']
    player2Id = body['state']['values']['player2']['users_select-action']['selected_user']
    player3Id = body['state']['values']['player3']['users_select-action']['selected_user']
    player4Id = body['state']['values']['player4']['users_select-action']['selected_user']

    validated = True
    if(tonpu_or_hanchan is None):
        say("東風戦か半荘戦か選択してください")
        validated = False
    if(player1Id is None or player2Id is None or player3Id is None or player4Id is None):
        say("プレイヤーを全員入力してください")
        validated = False
    if(len(set([player1Id, player2Id, player3Id, player4Id])) < 4):
        say("プレイヤーは全員異なるようにしてください")
        validated = False
    if(not validated): return

    

@app.action("users_select-action")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)

from flask import Flask, request

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    
    r = urllib.parse.unquote(request.get_data().decode())
    r1 = r.replace("payload=", "")
    res = json.loads(r1)
    # pprint.pprint(res)

    return handler.handle(request)

def init():
    game_id = exec_insert_sql("GameStatus", [1, 1, 0, 0], ["Ba", "Kyoku", "Honba", "Finished"])
    exec_insert_sql("Point", [game_id, 25000, 25000, 25000, 25000])
    exec_insert_sql("Participants", [game_id, "0", "0", "0", "0", 0])

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)