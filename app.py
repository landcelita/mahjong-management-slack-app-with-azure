import json
import logging
import os
from pprint import pprint
import urllib
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
import controller
import utility as util
import says
from const import BA, KYOKU, RYUKYOKU_WINNER, SCORE, FU_MAX

logging.basicConfig(level=logging.INFO)

client = WebClient(os.environ["SLACK_BOT_TOKEN"])

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

################################## Event Handler ##########################################

@app.message("ゲームスタート")
def message_gamestart(message, say):
    says.gamestart(say)

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

    tonpu_or_hanchan = bool(tonpu_or_hanchan_obj['value'])

    game_id = controller.init(tonpu_or_hanchan, player1Id, player2Id, player3Id, player4Id)

    say("member(saysの方にあとでちゃんと処理入れとく,東風戦か半荘戦かも記述)")
    says.wait_done(say, 1, 1, 0, game_id)

    util.delete_this_message(body, client)

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
        says.tsumo(say, value['game_id'])
    elif value['val'] == 'ron':
        says.ron(say, value['game_id'])
    elif value['val'] == 'ryukyoku':
        says.tenpai(say, value['game_id'])

    util.delete_this_message(body, client)

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
    han = int(han_value['val'])
    winner = int(winner_value['val'])
    game_id = int(han_value['game_id'])

    result_id = controller.confirm_result(game_id, winner, 0, han)

    if SCORE[str(han)]['fu_required']:
        says.fu(say, str(game_id), str(result_id), str(han))
    else:
        says.riichi(say, str(game_id), str(result_id))
        
    util.delete_this_message(body, client)

@app.action("actionId-ron-han")
def handle_ron_han(ack, body, logger, say):
    ack()
    han_option = body['state']['values']['han']['static_select-action']['selected_option']
    winner_option = body['state']['values']['winner']['radio_buttons-action']['selected_option']
    loser_option = body['state']['values']['loser']['radio_buttons-action']['selected_option']

    winner_value = None
    loser_value = None

    validated = True
    if han_option is None:
        say("翻数を選択してください")
        validated = False
    if winner_option is None:
        say("上がった人を選択してください")
        validated = False
    if loser_option is None:
        say("当てられた人を選択してください")
        validated = False
    if winner_option is not None and loser_option is not None:
        winner_value = json.loads(winner_option['value'])
        loser_value = json.loads(loser_option['value'])
        if winner_value['val'] == loser_value['val']:
            say("上がった人と当てられた人は別の人を選んでください")
            validated = False
    if not validated: return

    han_value = json.loads(han_option['value'])
    han = int(han_value['val'])
    winner = int(winner_value['val'])
    loser = int(loser_value['val'])
    game_id = int(han_value['game_id'])

    result_id = controller.confirm_result(game_id, winner, loser, han)

    if SCORE[str(han)]['fu_required']:
        says.fu(say, str(game_id), str(result_id), str(han))
    else:
        says.riichi(say, str(game_id), str(result_id))
        
    util.delete_this_message(body, client)

@app.action("actionId-tenpai")
def handle_tenpai(ack, body, say, client):
    ack()

    tenpai_options = body['state']['values']['tenpai']['checkboxes-action']['selected_options']
    hidden = json.loads(body['message']['blocks'][0]['accessory']['options'][0]['value'])
    game_id = int(hidden['game_id'])

    tenpais = [False, False, False, False]
    for option in tenpai_options:
        value = json.loads(option['value'])
        tenpais[int(value['val']) - 1] = True
    
    result_id = controller.confirm_result(game_id, RYUKYOKU_WINNER, None, None)
    controller.confirm_tenpai(result_id, tenpais)
    says.riichi(say, str(game_id), str(result_id))

    util.delete_this_message(body, client)

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
    fu = int(fu_value['val'])
    game_id = int(fu_value['game_id'])
    result_id = int(fu_value['result_id'])

    controller.update_fu(result_id, fu)
    says.riichi(say, str(game_id), str(result_id))

    util.delete_this_message(body, client)

@app.action("actionId-riichi")
def handle_riichi(ack, body, say, client):
    ack()
    riichi_options = body['state']['values']['riichi']['checkboxes-action']['selected_options']
    hidden = json.loads(body['message']['blocks'][0]['accessory']['options'][0]['value'])
    game_id = int(hidden['game_id'])
    result_id = int(hidden['result_id'])

    riichis = [False, False, False, False]
    for option in riichi_options:
        value = json.loads(option['value'])
        riichis[int(value['val']) - 1] = True
    controller.confirm_riichi(result_id, riichis)
    result = controller.get_result(result_id)
    says.confirmation(say, str(game_id), str(result_id), result, riichis)

    util.delete_this_message(body, client)

@app.action("actionId-confirmation-ok")
def handle_confirmation_ok(ack, body, logger, say):
    ack()
    hidden = json.loads(body['message']['blocks'][1]['elements'][0]['value'])
    game_id = int(hidden['game_id'])
    result_id = int(hidden['result_id'])

    old_scores, old_game_status, new_scores, new_game_status\
        = controller.settle(game_id, result_id)
    
    says.kyoku_result(say, old_scores, old_game_status, new_scores)
    if not new_game_status['finished']:
        says.wait_done(say, new_game_status['ba'], new_game_status['kyoku'], \
                    new_game_status['honba'], game_id)
    else:
        says.game_over(say)

    util.delete_this_message(body, client)

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

@app.action("radio")
def handle_radio(ack, body, logger):
    ack()

@app.event("message")
def handle_message_events(body, logger):
    pass
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