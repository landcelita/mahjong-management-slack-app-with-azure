import json
import logging
import os
import pprint
from typing import Dict
import urllib
from sqlcrud import exec_insert_sql, exec_select_sql, exec_update_sql, exec_delete_sql
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


logging.basicConfig(level=logging.INFO)

client = WebClient(os.environ["SLACK_BOT_TOKEN"])

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.message("ゲームスタート")
def message_gamestart(message, say):
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
                                "value": "0"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "半荘戦",
                                    "emoji": True
                                },
                                "value": "1"
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
def handle_confirm_players(ack, body, say, client):
    ack()
    tonpu_or_hanchan_obj = body['state']['values']['tonpu_or_hanchan']['radio']['selected_option']
    player1Id = body['state']['values']['player1']['users_select-action']['selected_user']
    player2Id = body['state']['values']['player2']['users_select-action']['selected_user']
    player3Id = body['state']['values']['player3']['users_select-action']['selected_user']
    player4Id = body['state']['values']['player4']['users_select-action']['selected_user']

    validated = True
    if(tonpu_or_hanchan_obj is None):
        say("東風戦か半荘戦か選択してください")
        validated = False
    if(player1Id is None or player2Id is None or player3Id is None or player4Id is None):
        say("プレイヤーを全員入力してください")
        validated = False
    if(len(set([player1Id, player2Id, player3Id, player4Id])) < 4):
        say("プレイヤーは全員異なるようにしてください")
        validated = False
    if(not validated): return

    # test中は消えると面倒なのでコメントアウト　あとで戻しておく
    # channel_id = body['container']['channel_id']
    # message_ts = body['container']['message_ts']
    # try:
    #     result = client.chat_delete(
    #         channel=channel_id,
    #         ts=message_ts
    #     )
    # except SlackApiError as e:
    #     logging.error(f"Error deleting message: {e}")

    tonpu_or_hanchan = int(tonpu_or_hanchan_obj['value'])

    game_id = init(tonpu_or_hanchan, player1Id, player2Id, player3Id, player4Id)
    hidden = {'game_id': str(game_id)}

    say("member")
    wait_done(1, 1, 0, hidden, say)

@app.action("users_select-action")
def handle_some_action(ack, body, logger):
    ack()

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

def init(TonpuOrHanchan, player1Id, player2Id, player3Id, player4Id):
    game_id = exec_insert_sql("GameStatus", [TonpuOrHanchan, 1, 1, 0, 0], ["TonpuOrHanchan", "Ba", "Kyoku", "Honba", "Finished"])
    exec_insert_sql("Score", [game_id, 25000, 25000, 25000, 25000])
    exec_insert_sql("Participants", [game_id, player1Id, player2Id, player3Id, player4Id])
    return game_id

def wait_done(ba, kyoku, honba, hidden, say):
    statement = "東" if ba == 1 else "南" if ba == 2 else "西" if ba == 3 else "北"
    statement += ("一" if kyoku == 1 else "二" if kyoku == 2 else "三" if kyoku == 3 else "四") + "局"
    if honba > 0:
        statement += f" {kyoku}本場"

    say(
        {
            "blocks": [
                {
                    "type": "input",
                    "block_id": "1234",
                    "label": {
                        "type": "plain_text",
                        "text": statement,
                        "emoji": True
                    },
                    "element": {
                        "type": "radio_buttons",
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "ツモ",
                                    "emoji": True
                                },
                                "value": "0"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "ロン",
                                    "emoji": True
                                },
                                "value": "1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "流局",
                                    "emoji": True
                                },
                                "value": "2"
                            }
                        ]
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
                            "action_id": "actionId-done"
                        }
                    ]
                }
            ]
        }
    )

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)