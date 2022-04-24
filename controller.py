from sqlcrud import exec_insert_sql, exec_select_sql, exec_update_sql, exec_delete_sql
from const import SCORE

def init(TonpuOrHanchan, player1Id, player2Id, player3Id, player4Id):
    game_id = exec_insert_sql("GameStatus", [TonpuOrHanchan, 1, 1, 0, 0], ["TonpuOrHanchan", "Ba", "Kyoku", "Honba", "Finished"])
    exec_insert_sql("Score", [game_id, 25000, 25000, 25000, 25000, 0])
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

def read_result(result_id: str):
    ret = {}

    res1 = exec_select_sql(table="Result",
                        cols=['TsumoRon', 'Winner', 'Han', 'Fu'],
                        where=f"ResultID = {int(result_id)}")
    ret['tsumo_or_ron'] = res1[-1][0]
    ret['winner'] = res1[-1][1]
    ret['han'] = res1[-1][2]
    ret['fu'] = res1[-1][3]
    res2 = exec_select_sql(table="Riichi",
                        cols=['Player1Riichi', 'Player2Riichi', 'Player3Riichi', 'Player4Riichi'])
    ret['riichis'] = []
    for i in range(len(res2[-1])):
        if res2[-1][i]:
            ret['riichis'].append(str(i + 1))

    return ret

def settle(game_id: str, result_id: str):
    result = read_result(result_id)
    scores = list(read_score(game_id))
    game_status = read_game_status(game_id)
    
    if result['tsumo_or_ron'] is None:
        tenpai = list(read_tenpai(result_id))
        new_game_status = settle_ryukyoku(result, scores, game_status, tenpai)
    elif result['tsumo_or_ron'] == 0:
        new_game_status = settle_tsumo(result, scores, game_status)
    else:
        new_game_status = settle_ron(result, scores, game_status)


def settle_ryukyoku(result, scores, game_status, tenpai):
    pass

def settle_tsumo(result, scores, game_status):
    # 供託金に移動
    for r in result['riichis']:
        scores[int(r) - 1] -= 1000
        scores[4] += 1000

    # ツモの分
    if result['winner'] == game_status['kyoku']:
        lose = SCORE[str(result['han'])][str(result['fu'])]['oya']['tsumo'] \
                if SCORE[str(result['han'])]['fu_required'] \
                else SCORE[str(result['han'])]['oya']['tsumo']
        lose += 100 * game_status['honba']
        for i in range(1, 5):
            if result['winner'] == i:
                scores[i-1] += lose * 3
            else:
                scores[i-1] -= lose
    else:
        ko_lose, oya_lose = SCORE[str(result['han'])][str(result['fu'])]['ko']['tsumo'] \
                            if SCORE[str(result['han'])]['fu_required'] \
                            else SCORE[str(result['han'])]['oya']['tsumo']
        ko_lose += 100 * game_status['honba']
        oya_lose += 100 * game_status['honba']
        for i in range(1, 5):
            if result['winner'] == i:
                scores[i-1] += ko_lose * 2 + oya_lose
            elif game_status['kyoku'] == i:
                scores[i-1] -= oya_lose
            else:
                scores[i-1] -= ko_lose

    # 供託金の分
    scores[result['winner'] - 1] += scores[4]
    scores[4] = 0

    # 更新
    update_score(scores, game_status)


def settle_ron(result, scores, game_status):
    pass

def read_score(game_id):
    res = exec_select_sql(table="Score",
                          cols=["Player1Score", "Player2Score", "Player3Score", "Player4Score", "Kyotaku"],
                          where=f"GameID = {game_id}")
    return res[-1]

def read_game_status(game_id):
    res = exec_select_sql(table="GameStatus",
                            cols=["TonpuOrHanchan", "Ba", "Kyoku", "Honba", "Finished", "GameID"],
                            where=f"GameID = {game_id}")
    ret = {}
    ret["tonpu_or_hanchan"] = res[-1][0]
    ret["ba"] = res[-1][1]
    ret["kyoku"] = res[-1][2]
    ret["honba"] = res[-1][3]
    ret["finished"] = res[-1][4]
    ret["game_id"] = res[-1][5]

    return ret


def read_tenpai(result_id):
    pass

def update_score(scores, game_status):
    exec_update_sql(table="Score",
                    cols=["Player1Score", "Player2Score", "Player3Score", "Player4Score", "Kyotaku"],
                    vals=scores,
                    where=f"GameID = {game_status['game_id']}")