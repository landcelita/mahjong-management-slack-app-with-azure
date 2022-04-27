import json
from pprint import pprint
from typing import Dict, List, Union
import utility as util
from const import BA, KYOKU, SCORE, FU_MAX
import controller

def gamestart(say):
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
                        "options": util.generate_option_dicts(
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
                    "elements": [ util.confirm_button("confirm", "actionId-confirm-players") ]
                }
            ]
        }
    )

def wait_done(ba, kyoku, honba, game_id, say):
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
                        "options": util.generate_option_dicts(
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
                    "elements": [ util.confirm_button("confirm", "actionId-done") ]
                }
            ]
        }
    )

def tsumo(game_id, say):
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
                        "options": util.generate_option_dicts(
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
                        "options": util.generate_option_dicts(
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
                    "elements": [ util.confirm_button("value", "actionId-tsumo-han") ]
                }
            ]
        }
    )

def ron(game_id, say):
    pass

def ryukyoku(game_id, say):
    pass

def fu(game_id: str, result_id: str, han: str, say):
    hidden = {'game_id': game_id, 'result_id': result_id}
    fus = SCORE[han]['fu']
    fu_list = []
    values = []

    for fu in fus:
        if fu == f'{FU_MAX}': fu_list.append("それ以上")
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
                        "options": util.generate_option_dicts(
                                fu_list,
                                values
                        ),
                        "action_id": "static_select-action"
                    }
                },
                {
                    "type": "actions",
                    "elements": [ util.confirm_button("value", "actionId-fu") ]
                }
            ]
        }
    )

def riichi(game_id: str, result_id: str, say):
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
                    "elements": [ util.confirm_button("value", "actionId-riichi") ]
                }
            ]
        }
    )

def confirmation(game_id: str, result_id: str, result: Dict[str, Union[int, None]],
         riichis: List[bool], say):
    hidden = {'game_id': game_id, 'result_id': result_id}
    content = "以下の内容でよろしいですか?\n\n"

    if result['fu'] == FU_MAX: 
        result['fu'] = "満貫"
    elif result['fu'] is not None:
        result['fu'] = f"{result['fu']}符"
    else:
        result['fu'] = ""

    riichi_str = "リーチ者: "
    for i in range(len(riichis)):
        if riichis[i] == True: riichi_str += f"{i+1} "

    if result['tsumo_ron'] is None:
        content += "流局\n" + riichi_str
    elif result['tsumo_ron']:
        content += "ロン\n"
        content += f"上がり: {result['tsumo_ron']} → {result['winner']}\n"
        content += f"{result['han']}翻" + result['fu'] + "\n"
        content += riichi_str
    else:
        content += "ツモ\n"
        content += f"上がり: {result['winner']}\n"
        content += f"{result['han']}翻" + result['fu'] + "\n"
        content += riichi_str

    say(
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": content
                    }
                },
                {
                    "type": "actions",
                    "block_id": "confirm",
                    "elements": [util.confirm_button(
                        json.dumps(hidden),
                        "actionId-confirmation-ok"
                    )]
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
                            "value": "retry",
                            "action_id": "actionId-confirmation-retry"
                        }
                    ]
                }
            ]
        }
    )

def kyoku_result(old_scores, old_game_status, new_scores, say):

    pprint(old_scores)
    pprint(old_game_status)
    pprint(new_scores)
    diff = [new_scores[i] - old_scores[i] for i in range(len(new_scores))]

    text = f"{BA[old_game_status['ba']]}{KYOKU[old_game_status['kyoku']]}局"
    if old_game_status['honba'] > 0: text += f"{old_game_status['honba']}本場"
    text += "\n"
    text += "得点\n"\
            f"player1: {new_scores[0]}点 ({'{:+}'.format(diff[0])})\n"\
            f"player2: {new_scores[1]}点 ({'{:+}'.format(diff[1])})\n"\
            f"player3: {new_scores[2]}点 ({'{:+}'.format(diff[2])})\n"\
            f"player4: {new_scores[3]}点 ({'{:+}'.format(diff[3])})\n"\
    
    say(
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    }
                }
            ]
        }
    )

def game_over(say):
    say(
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "ゲーム終了"
                    }
                }
            ]
        }
    )
