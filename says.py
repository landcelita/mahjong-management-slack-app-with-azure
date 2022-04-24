import json
import utility as util
from const import BA, KYOKU, SCORE, FU_MAX

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

def confirmation(game_id: str, result_id: str, say):
    hidden = {'game_id': game_id, 'result_id': result_id}
    # tsumo_or_ron, winner, han, fu, riichis = controller.read_result(result_id)

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