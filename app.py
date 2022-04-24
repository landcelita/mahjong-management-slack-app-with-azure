import json
import logging
import os
from pprint import pprint
from typing import Dict
import urllib
from sqlcrud import exec_insert_sql, exec_select_sql, exec_update_sql, exec_delete_sql
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

################################## Const ##########################################

logging.basicConfig(level=logging.INFO)

client = WebClient(os.environ["SLACK_BOT_TOKEN"])

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

BA = ['error', '東', '南', '西', '北']
KYOKU = ['error', '一', '二', '三', '四']
SCORE = {
    '1': {
        'fu_required': True,
        'fu': ['30', '40', '50', '60', '70', '80', '90', '100', '110'],
        '30': { 
            'ko': {'ron': 1000, 'tsumo': [300, 500]},
            'oya': {'ron': 1500, 'tsumo': 500},
        },
        '40': {
            'ko': {'ron': 1300, 'tsumo': [400, 700]},
            'oya': {'ron': 2000, 'tsumo': 700},
        },
        '50': {
            'ko': {'ron': 1600, 'tsumo': [400, 800]},
            'oya': {'ron': 2400, 'tsumo': 800},
        },
        '60': {
            'ko': {'ron': 2000, 'tsumo': [500, 1000]},
            'oya': {'ron': 2900, 'tsumo': 1000},
        },
        '70': {
            'ko': {'ron': 2300, 'tsumo': [600, 1200]},
            'oya': {'ron': 3400, 'tsumo': 1200},
        },
        '80': {
            'ko': {'ron': 2600, 'tsumo': [700, 1300]},
            'oya': {'ron': 3900, 'tsumo': 1300},
        },
        '90': {
            'ko': {'ron': 2900, 'tsumo': [800, 1500]},
            'oya': {'ron': 4400, 'tsumo': 1500},
        },
        '100': {
            'ko': {'ron': 3200, 'tsumo': [800, 1600]},
            'oya': {'ron': 4800, 'tsumo': 1600},
        },
        '110': {
            'ko': {'ron': 3600, 'tsumo': [900, 1800]},
            'oya': {'ron': 5300, 'tsumo': 1800},
        },
    },
    '2': {
        'fu_required': True,
        'fu': ['20', '25', '30', '40', '50', '60', '70', '80', '90', '100', '110'],
        '20': {
            'ko': {'ron': None, 'tsumo': [400, 700]},
            'oya': {'ron': None, 'tsumo': 700},
        },
        '25': {
            'ko': {'ron': 1600, 'tsumo': [None, None]},
            'oya': {'ron': 2400, 'tsumo': None},
        },
        '30': {
            'ko': {'ron': 2000, 'tsumo': [500, 1000]},
            'oya': {'ron': 2900, 'tsumo': 1000},
        },
        '40': {
            'ko': {'ron': 2600, 'tsumo': [700, 1300]},
            'oya': {'ron': 3900, 'tsumo': 1300},
        },
        '50': {
            'ko': {'ron': 3200, 'tsumo': [800, 1600]},
            'oya': {'ron': 4800, 'tsumo': 1600},
        },
        '60': {
            'ko': {'ron': 3900, 'tsumo': [1000, 2000]},
            'oya': {'ron': 5800, 'tsumo': 2000},
        },
        '70': {
            'ko': {'ron': 4500, 'tsumo': [1200, 2300]},
            'oya': {'ron': 6800, 'tsumo': 2300},
        },
        '80': {
            'ko': {'ron': 5200, 'tsumo': [1300, 2600]},
            'oya': {'ron': 7700, 'tsumo': 2600},
        },
        '90': {
            'ko': {'ron': 5800, 'tsumo': [1500, 2900]},
            'oya': {'ron': 8700, 'tsumo': 2900},
        },
        '100': {
            'ko': {'ron': 6400, 'tsumo': [1600, 3200]},
            'oya': {'ron': 9600, 'tsumo': 3200},
        },
        '110': {
            'ko': {'ron': 7100, 'tsumo': [1800, 3600]},
            'oya': {'ron': 10600, 'tsumo': 3600},
        },
    },
    '3': {
        'fu_required': True,
        'fu': ['20', '25', '30', '40', '50', '60', 'more'],
        '20': {
            'ko': {'ron': None, 'tsumo': [700, 1300]},
            'oya': {'ron': None, 'tsumo': 1300},
        },
        '25': {
            'ko': {'ron': 3200, 'tsumo': [800, 1600]},
            'oya': {'ron': 4800, 'tsumo': 1600},
        },
        '30': {
            'ko': {'ron': 3900, 'tsumo': [1000, 2000]},
            'oya': {'ron': 5800, 'tsumo': 2000},
        },
        '40': {
            'ko': {'ron': 5200, 'tsumo': [1300, 2600]},
            'oya': {'ron': 7700, 'tsumo': 2600},
        },
        '50': {
            'ko': {'ron': 6400, 'tsumo': [1600, 3200]},
            'oya': {'ron': 9600, 'tsumo': 3200},
        },
        '60': {
            'ko': {'ron': 7700, 'tsumo': [2000, 3900]},
            'oya': {'ron': 11600, 'tsumo': 3900},
        },
        'more': {
            'ko': {'ron': 8000, 'tsumo': [2000, 4000]},
            'oya': {'ron': 12000, 'tsumo': 4000},
        }
    },
    '4': {
        'fu_required': True,
        'fu': ['20', '25', '30', 'more'],
        '20': {
            'ko': {'ron': None, 'tsumo': [1300, 2600]},
            'oya': {'ron': None, 'tsumo': 2600},
        },
        '25': {
            'ko': {'ron': 6400, 'tsumo': [1600, 3200]},
            'oya': {'ron': 9600, 'tsumo': 3200},
        },
        '30': {
            'ko': {'ron': 7700, 'tsumo': [2000, 3900]},
            'oya': {'ron': 11600, 'tsumo': 3900},
        },
        'more': {
            'ko': {'ron': 8000, 'tsumo': [2000, 4000]},
            'oya': {'ron': 12000, 'tsumo': 4000},
        }
    },
    '5': {
        'fu_required': False,
        'ko': {'ron': 8000, 'tsumo': [2000, 4000]},
        'oya': {'ron': 12000, 'tsumo': 4000},
    },
    '6': {
        'fu_required': False,
        'ko': {'ron': 12000, 'tsumo': [3000, 6000]},
        'oya': {'ron': 18000, 'tsumo': 6000},
    },
    '7': {
        'fu_required': False,
        'ko': {'ron': 12000, 'tsumo': [3000, 6000]},
        'oya': {'ron': 18000, 'tsumo': 6000},
    },
    '8': {
        'fu_required': False,
        'ko': {'ron': 16000, 'tsumo': [4000, 8000]},
        'oya': {'ron': 24000, 'tsumo': 8000},
    },
    '9': {
        'fu_required': False,
        'ko': {'ron': 16000, 'tsumo': [4000, 8000]},
        'oya': {'ron': 24000, 'tsumo': 8000},
    },
    '10': {
        'fu_required': False,
        'ko': {'ron': 16000, 'tsumo': [4000, 8000]},
        'oya': {'ron': 24000, 'tsumo': 8000},
    },
    '11': {
        'fu_required': False,
        'ko': {'ron': 24000, 'tsumo': [6000, 12000]},
        'oya': {'ron': 36000, 'tsumo': 12000},
    },
    '12': {
        'fu_required': False,
        'ko': {'ron': 24000, 'tsumo': [6000, 12000]},
        'oya': {'ron': 36000, 'tsumo': 12000},
    },
    'yakuman': {
        'fu_required': False,
        'ko': {'ron': 32000, 'tsumo': [8000, 16000]},
        'oya': {'ron': 48000, 'tsumo': 16000},
    },
    'double_yakuman': {
        'fu_required': False,
        'ko': {'ron': 64000, 'tsumo': [16000, 32000]},
        'oya': {'ron': 96000, 'tsumo': 32000},
    },
    'triple_yakuman': {
        'fu_required': False,
        'ko': {'ron': 96000, 'tsumo': [24000, 48000]},
        'oya': {'ron': 144000, 'tsumo': 48000},
    }
}
FU_MAX = 999999999

################################## Event Handler ##########################################

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
                        "options": generate_option_dicts(
                            ["東風戦", "半荘戦"],
                            ["0", "1"]
                        ),
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
                    "elements": [ confirm_button("confirm", "actionId-confirm-players") ]
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

    tonpu_or_hanchan = int(tonpu_or_hanchan_obj['value'])

    game_id = init(tonpu_or_hanchan, player1Id, player2Id, player3Id, player4Id)

    say("member(あとでちゃんと処理入れとく)")
    say_wait_done(1, 1, 0, game_id, say)

    # test中は消えると面倒なのでコメントアウト　あとで戻しておく
    # delete_this_message(body, client)

@app.action("actionId-done")
def handle_done(ack, body, say, client):
    ack()
    # pprint(body)
    option = body['state']['values']['how_finished']['radio']['selected_option']

    validated = True
    if option is None:
        say("ツモ、ロン、流局のどれかを選んでください")
        validated = False
    if not validated: return

    value = json.loads(option['value'])
    if value['val'] == 'tsumo':
        say_tsumo(value['game_id'], say)
    elif value['val'] == 'ron':
        say_ron(value['game_id'], say)
    elif value['val'] == 'ryukyoku':
        say_ryukyoku(value['game_id'], say)

    # test中は消えると面倒なのでコメントアウト　あとで戻しておく
    # delete_this_message(body, client)

@app.action("actionId-tsumo-han")
def handle_tsumo_han(ack, body, say, client):
    ack()
    han_option = body['state']['values']['han']['static_select-action']['selected_option']
    winner_option = body['state']['values']['winner']['radio_buttons-action']['selected_option']

    validated = True
    if han_option is None:
        say("翻数を選択してください")
        validated = False
    if winner_option is None:
        say("上がった人を選択してください")
        validated = False
    if not validated: return

    han_value = json.loads(han_option['value'])
    winner_value = json.loads(winner_option['value'])
    han = han_value['val']
    winner = winner_value['val']
    game_id = han_value['game_id']

    result_id, _, _, _ = create_result(game_id, winner, 0, han)

    if SCORE[han]['fu_required']:
        say_fu(game_id, str(result_id), han, say)

    # test中は消えると面倒なのでコメントアウト　あとで戻しておく
    # delete_this_message(body, client)

@app.action("actionId-fu")
def handle_fu(ack, body, say, client):
    ack()
    fu_option = body['state']['values']['fu']['static_select-action']['selected_option']

    validated = True
    if fu_option is None:
        say("符数を選択してください")
        validated = False
    if not validated: return

    fu_value = json.loads(fu_option['value'])
    fu = int(fu_value['val']) if fu_value['val'] != "more" else FU_MAX
    game_id = str(fu_value['game_id'])
    result_id = str(fu_value['result_id'])

    update_result(result_id, "fu", fu)
    say_riichi(game_id, result_id, say)

    # test中は消えると面倒なのでコメントアウト　あとで戻しておく
    # delete_this_message(body, client)

@app.action("actionId-riichi")
def handle_riichi(ack, body, say, client):
    ack()
    riichi_options = body['state']['values']['riichi']['checkboxes-action']['selected_options']
    hidden = json.loads(body['message']['blocks'][0]['accessory']['options'][0]['value'])
    game_id = hidden['game_id']
    result_id = hidden['result_id']

    riichi = [False, False, False, False]
    for option in riichi_options:
        value = json.loads(option['value'])
        riichi[int(value['val']) - 1] = True
    create_riichi(result_id, *riichi)

    say_confirmation(game_id, result_id, say)

    # test中は消えると面倒なのでコメントアウト　あとで戻しておく
    # delete_this_message(body, client)

# 以下はINFOを抑制するため
@app.action("users_select-action")
def handle_users_select_action(ack, body, logger):
    ack()

@app.action("static_select-action")
def handle_static_select_action(ack, body, logger):
    ack()

@app.action("radio_buttons-action")
def handle_radio_buttons_action(ack, body, logger):
    ack()

@app.action("checkboxes-action")
def handle_checkboxes_action(ack, body, logger):
    ack()

################################## Controller ##########################################

def init(TonpuOrHanchan, player1Id, player2Id, player3Id, player4Id):
    game_id = exec_insert_sql("GameStatus", [TonpuOrHanchan, 1, 1, 0, 0], ["TonpuOrHanchan", "Ba", "Kyoku", "Honba", "Finished"])
    exec_insert_sql("Score", [game_id, 25000, 25000, 25000, 25000])
    exec_insert_sql("Participants", [game_id, player1Id, player2Id, player3Id, player4Id])
    return game_id

def create_result(game_id, winner, tsumo_ron, han, fu=None):
    game_id = str(game_id)

    # tsumo_ron: 0のときはツモ、1-4のときはロンされた人
    res = exec_select_sql(table="GameStatus",
                        cols=["Ba", "Kyoku", "Honba"], 
                        where="GameID = " + game_id)

    ba, kyoku, honba = res[0]
    game_id = int(game_id)
    winner = int(winner)
    tsumo_ron = int(tsumo_ron)
    han = int(han)
    if fu is not None: fu = int(fu)
    result_id = exec_insert_sql(table="Result",
                                vals=[game_id, ba, kyoku, honba, winner, 0, han, fu],
                                cols=["GameID", "Ba", "Kyoku", "Honba", "Winner", "TsumoRon", "Han", "Fu"])
    return (result_id, ba, kyoku, honba)

def update_result(result_id: str, cols, vals):
    exec_update_sql(table="Result",
                    cols=cols,
                    vals=vals,
                    where="ResultID = " + result_id)

def create_riichi(result_id, is1Riichi, is2Riichi, is3Riichi, is4Riichi):
    exec_insert_sql(table="Riichi",
                    cols=["ResultID", "Player1Riichi", "Player2Riichi", "Player3Riichi", "Player4Riichi"],
                    vals=[result_id, is1Riichi, is2Riichi, is3Riichi, is4Riichi])

def read_result(result_id):
    pass

################################## Say ##########################################

def say_wait_done(ba, kyoku, honba, game_id, say):
    statement = BA[ba] + KYOKU[kyoku] + "局"
    if honba > 0:
        statement += f" {honba}本場"
    hidden = {'game_id': str(game_id)}

    say(
        {
            "blocks": [
                {
                    "type": "input",
                    "block_id": "how_finished",
                    "label": {
                        "type": "plain_text",
                        "text": statement,
                        "emoji": True
                    },
                    "element": {
                        "type": "radio_buttons",
                        "action_id": "radio",
                        "options": generate_option_dicts(
                            ["ツモ", "ロン", "流局"],
                            [
                                json.dumps({"val": "tsumo"} | hidden),
                                json.dumps({"val": "ron"} | hidden),
                                json.dumps({"val": "ryukyoku"} | hidden)
                            ]
                        )
                    }
                },
                {
                    "type": "actions",
                    "elements": [ confirm_button("confirm", "actionId-done") ]
                }
            ]
        }
    )

def say_tsumo(game_id, say):
    hidden = {'game_id': game_id}

    say(
        {
            "blocks": [
                {
                    "type": "section",
                    "block_id": "winner",
                    "text": {
                        "type": "mrkdwn",
                        "text": "上がった人"
                    },
                    "accessory": {
                        "type": "radio_buttons",
                        "options": generate_option_dicts(
                                ["player1", "player2", "player3", "player4"],
                                [
                                    json.dumps({"val": "1"} | hidden),
                                    json.dumps({"val": "2"} | hidden),
                                    json.dumps({"val": "3"} | hidden),
                                    json.dumps({"val": "4"} | hidden),
                                ]
                        ),
                        "action_id": "radio_buttons-action"
                    }
                },
                {
                    "type": "section",
                    "block_id": "han",
                    "text": {
                        "type": "mrkdwn",
                        "text": "翻数"
                    },
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "翻数を選んでください",
                            "emoji": True
                        },
                        "options": generate_option_dicts(
                            ["1翻", "2翻", "3翻", "4翻", "5翻", "6翻", "7翻", "8翻", "9翻", "10翻", "11翻", "12翻", "役満", "ダブル役満", "トリプル役満"],
                            [
                                json.dumps({"val": "1"} | hidden),
                                json.dumps({"val": "2"} | hidden),
                                json.dumps({"val": "3"} | hidden),
                                json.dumps({"val": "4"} | hidden),
                                json.dumps({"val": "5"} | hidden),
                                json.dumps({"val": "6"} | hidden),
                                json.dumps({"val": "7"} | hidden),
                                json.dumps({"val": "8"} | hidden),
                                json.dumps({"val": "9"} | hidden),
                                json.dumps({"val": "10"} | hidden),
                                json.dumps({"val": "11"} | hidden),
                                json.dumps({"val": "12"} | hidden),
                                json.dumps({"val": "yakuman"} | hidden),
                                json.dumps({"val": "double_yakuman"} | hidden),
                                json.dumps({"val": "triple_yakuman"} | hidden),
                            ]
                        ),
                        "action_id": "static_select-action"
                    }
                },
                {
                    "type": "actions",
                    "elements": [ confirm_button("value", "actionId-tsumo-han") ]
                }
            ]
        }
    )

def say_ron(game_id, say):
    pass

def say_ryukyoku(game_id, say):
    pass

def say_fu(game_id: str, result_id: str, han: str, say):
    hidden = {'game_id': game_id, 'result_id': result_id}
    fus = SCORE[han]['fu']
    fu_list = []
    values = []

    for fu in fus:
        if fu == 'more': fu_list.append("それ以上")
        else: fu_list.append(fu + "符")
        
        values.append(json.dumps({'val': fu} | hidden))

    say(
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "符数"
                    },
                    "block_id": "fu",
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "翻数を選んでください",
                            "emoji": True
                        },
                        "options": generate_option_dicts(
                                fu_list,
                                values
                        ),
                        "action_id": "static_select-action"
                    }
                },
                {
                    "type": "actions",
                    "elements": [ confirm_button("value", "actionId-fu") ]
                }
            ]
        }
    )

def say_riichi(game_id: str, result_id: str, say):
    hidden = {'game_id': game_id, 'result_id': result_id}

    say(
        {
            "blocks": [
                {
                    "type": "section",
                    "block_id": "riichi",
                    "text": {
                        "type": "mrkdwn",
                        "text": "リーチ者を選んでください"
                    },
                    "accessory": {
                        "type": "checkboxes",
                        "options": [
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "player1"
                                },
                                "value": json.dumps({"val": "1"} | hidden)
                            },
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "player2"
                                },
                                "value": json.dumps({"val": "2"} | hidden)
                            },
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "player3"
                                },
                                "value": json.dumps({"val": "3"} | hidden)
                            },
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "player4"
                                },
                                "value": json.dumps({"val": "4"} | hidden)
                            }
                        ],
                        "action_id": "checkboxes-action"
                    }
                },
                {
                    "type": "actions",
                    "elements": [ confirm_button("value", "actionId-riichi") ]
                }
            ]
        }
    )

def say_confirmation(game_id: str, result_id: str, say):
    hidden = {'game_id': game_id, 'result_id': result_id}
    # tsumo_or_ron, winner, han, fu, riichis = read_result(result_id)

    say(
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "以下の内容でよろしいですか？\n\nツモ\n上がり: player1\nn翻m符\nリーチ者: player3 player4"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "OK",
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "action_id": "actionId-0"
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "再入力",
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "action_id": "actionId-0"
                        }
                    ]
                }
            ]
        }
    )

################################## Utility ##########################################

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


################################## Entrypoint ##########################################

from flask import Flask, request

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    r = urllib.parse.unquote(request.get_data().decode())
    r1 = r.replace("payload=", "")
    res = json.loads(r1)
    # pprint(res)

    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)