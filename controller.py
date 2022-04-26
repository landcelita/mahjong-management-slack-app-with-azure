from typing import Union, List
from crud import exec_insert_sql, exec_select_sql, exec_update_sql, exec_delete_sql
import data
import business
from const import SCORE

def init(tonpu_or_hanchan: bool, player1Id: str, player2Id: str, player3Id: str, player4Id: str):
    game_start_status = {
        'tonpu_or_hanchan': tonpu_or_hanchan,
        'ba': 1,
        'kyoku': 1,
        'honba': 0,
        'finished': 0
    }
    game_id = data.create_game_status(game_start_status)
    
    game_start_scores = [game_id, 25000, 25000, 25000, 25000, 0]
    data.create_score(game_start_scores)

    game_start_participants = [game_id, player1Id, player2Id, player3Id, player4Id]
    data.create_participants(game_start_participants)
    
    return game_id

def confirm_result(game_id: int, winner: int, tsumo_ron: Union[int, None],\
        han: int, fu: Union[int, None] = None):
    # tsumo_ron: 0のときはツモ、1-4のときはロンされた人

    game_status = data.read_game_status(game_id)
    result = {
        'game_id': game_id,
        'ba': game_status['ba'],
        'kyoku': game_status['kyoku'],
        'honba': game_status['honba'],
        'winner': winner,
        'tsumo_ron': tsumo_ron,
        'han': han,
        'fu': fu
    }
    result_id = data.create_result(result)

    return result_id

def update_fu(result_id: int, fu: int):
    updating_data = {"fu": fu}
    data.update_result(result_id, updating_data)

def confirm_riichi(result_id: int, riichi: List[bool]):
    data.create_riichi([result_id, *riichi])

def settle(game_id: int, result_id: int):
    result = data.read_result(result_id)
    riichis = data.read_riichi(result_id, "ResultID",
                cols=["Player1Riichi", "Player2Riichi", "Player3Riichi", "Player4Riichi"])
    scores = list(data.read_score(game_id, "GameID",
                cols=["Player1Score", "Player2Score", "Player3Score", "Player4Score"]))
    game_status = data.read_game_status(game_id)
    
    
    if result['tsumo_or_ron'] is None:
        # tenpai = list(read_tenpai(result_id))
        # new_game_status = settle_ryukyoku(result, scores, game_status, tenpai)
        pass
    elif result['tsumo_or_ron'] == 0:
        new_scores, new_game_status = settle_tsumo(result, riichis, scores, game_status)
    else:
        # new_game_status = settle_ron(result, scores, game_status)
        pass

    return scores, game_status, new_scores, new_game_status

def settle_ryukyoku(result, scores, game_status, tenpai):
    pass # todo

def settle_tsumo(result, riichis, scores, game_status):
    new_scores = business.calc_new_score_tsumo(result, riichis, scores, game_status)
    data.update_score(game_status["game_id"], new_scores, "GameID",
                    ["Player1Score", "Player2Score", "Player3Score", "Player4Score", "Kyotaku"])

    new_game_status = business.calc_new_status_tsumo(result, riichis, new_scores, game_status)
    data.update_game_status(result['game_id'], new_game_status)

    return new_scores, new_game_status

def settle_ron(result, scores, game_status):
    pass # todo

