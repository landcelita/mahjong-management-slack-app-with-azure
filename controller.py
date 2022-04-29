from pprint import pprint
from typing import Union, List
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
        han: Union[int, None], fu: Union[int, None] = None):
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

def confirm_tenpai(result_id: int, tenpai: List[bool]):
    data.create_tenpai([result_id, *tenpai])

def update_fu(result_id: int, fu: int):
    updating_data = {"fu": fu}
    data.update_result(result_id, updating_data)

def confirm_riichi(result_id: int, riichi: List[bool]):
    data.create_riichi([result_id, *riichi])

def get_result(result_id: int):
    return data.read_result(result_id)

def get_tenpai(result_id: int):
    result = data.read_result(result_id)
    if result['tsumo_ron'] is not None: return None
    return data.read_tenpai(result_id, "ResultID",
                cols=["Player1Tenpai", "Player2Tenpai", "Player3Tenpai", "Player4Tenpai"])

def settle(game_id: int, result_id: int):
    result = data.read_result(result_id)
    riichis = data.read_riichi(result_id, "ResultID",
                cols=["Player1Riichi", "Player2Riichi", "Player3Riichi", "Player4Riichi"])
    scores = list(data.read_score(game_id, "GameID",
                cols=["Player1Score", "Player2Score", "Player3Score", "Player4Score", "Kyotaku"]))
    game_status = data.read_game_status(game_id)
    
    
    if result['tsumo_ron'] is None:
        tenpais = list(data.read_tenpai(result_id, "ResultID",
                cols=["Player1Tenpai", "Player2Tenpai", "Player3Tenpai", "Player4Tenpai"]))
        new_scores, new_game_status = settle_ryukyoku(result, riichis, scores, game_status, tenpais, game_id)
        pass
    elif result['tsumo_ron'] == 0:
        new_scores, new_game_status = settle_tsumo(result, riichis, scores, game_status, game_id)
    else:
        new_scores, new_game_status = settle_ron(result, riichis, scores, game_status, game_id)

    return scores, game_status, new_scores, new_game_status

def settle_ryukyoku(result, riichis, scores, game_status, tenpais, game_id):
    new_scores = business.calc_new_score_ryukyoku(riichis, scores, tenpais)
    data.update_score(game_id, new_scores, "GameID",
                    ["Player1Score", "Player2Score", "Player3Score", "Player4Score", "Kyotaku"])
    
    new_game_status = business.calc_new_status_ryukyoku(result, new_scores, game_status, tenpais)
    data.update_game_status(result['game_id'], new_game_status)

    return new_scores, new_game_status

def settle_tsumo(result, riichis, scores, game_status, game_id):
    new_scores = business.calc_new_score_tsumo(result, riichis, scores, game_status)
    data.update_score(game_id, new_scores, "GameID",
                    ["Player1Score", "Player2Score", "Player3Score", "Player4Score", "Kyotaku"])
    
    new_game_status = business.calc_new_status_agari(result, new_scores, game_status)
    data.update_game_status(result['game_id'], new_game_status)

    return new_scores, new_game_status

def settle_ron(result, riichis, scores, game_status, game_id):
    new_scores = business.calc_new_score_ron(result, riichis, scores, game_status)
    data.update_score(game_id, new_scores, "GameID",
                    ["Player1Score", "Player2Score", "Player3Score", "Player4Score", "Kyotaku"])
    
    new_game_status = business.calc_new_status_agari(result, new_scores, game_status)
    data.update_game_status(result['game_id'], new_game_status)

    return new_scores, new_game_status
