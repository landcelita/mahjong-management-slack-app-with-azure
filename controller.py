from sqlcrud import exec_insert_sql, exec_select_sql, exec_update_sql, exec_delete_sql

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