from pprint import pprint
from typing import List, Union, Dict
from const import GAMESTATUS_PASCAL_TO_SNAKE, GAMESTATUS_SNAKE_TO_PASCAL, RESULT_PASCAL_TO_SNAKE, RESULT_SNAKE_TO_PASCAL
import crud
import re

def create_game_status(vals: Dict[str, int]):
    keys = [GAMESTATUS_SNAKE_TO_PASCAL[key] for key in list(vals.keys())]
    values = list(vals.values())
    game_id = crud.exec_insert_sql("GameStatus", values, keys)
    return game_id

def read_game_status(whereval: int, wherecol: str = "GameID",
        cols: List[str] = ["TonpuOrHanchan", "Ba", "Kyoku", "Honba", "Finished"],
        onlylast: bool = True):
    res = crud.exec_select_sql("GameStatus", cols, 
                        f"{wherecol} = {whereval}")

    col_names = [GAMESTATUS_PASCAL_TO_SNAKE[col] for col in cols]

    if onlylast:
        ret = {}
        for i in range(len(col_names)):
            ret[col_names[i]] = res[-1][i]
        return ret
    else:
        ret = []
        for r in res:
            ret0 = {}
            for i in range(len(col_names)):
                ret0[col_names[i]] = r[i]
            ret.append(ret0)
        return ret

def update_game_status(whereval: int, vals: Dict[str, int],
        wherecol: str = "GameID"):
    keys = [GAMESTATUS_SNAKE_TO_PASCAL[key] for key in list(vals.keys())]
    values = list(vals.values())
    crud.exec_update_sql(table="GameStatus",
                        cols=keys,
                        vals=values,
                        where=f"{wherecol} = {whereval}")

def create_score(vals: List[int], cols: List[str] = ["GameID", "Player1Score",\
        "Player2Score", "Player3Score", "Player4Score", "Kyotaku"]):
    return crud.exec_insert_sql("Score", vals, cols)

def read_score(whereval: int, wherecol: str = "ScoreID",
        cols: List[str] = ["GameID", "Player1Score", "Player2Score",
                            "Player3Score", "Player4Score", "Kyotaku"],
        onlylast: bool = True):
    res = crud.exec_select_sql("Score", cols, f"{wherecol} = {whereval}")

    if onlylast:
        return res[-1]
    else:
        return res

def update_score(whereval: int, vals: Union[List[int], int],
        wherecol: str = "ScoreID",
        cols: Union[List[str], str] = ["GameID", "Player1Score", "Player2Score",
                                        "Player3Score", "Player4Score", "Kyotaku"]):
    crud.exec_update_sql("Score", cols, vals, f"{wherecol} = {whereval}")

def create_participants(vals: List[Union[int, str]], cols: List[str] = \
        ["GameID", "Player1SlackID", "Player2SlackID", "Player3SlackID", "Player4SlackID"]):
    return crud.exec_insert_sql("Participants", vals, cols)

def create_result(vals: Dict[str, Union[int, None]]):
    keys = [RESULT_SNAKE_TO_PASCAL[key] for key in list(vals.keys())]
    values = list(vals.values())
    return crud.exec_insert_sql("Result", values, keys)

def read_result(whereval: int, wherecol: str = "ResultID",
        cols: List[str] = ["GameID", "Ba", "Kyoku", "Honba", "Winner", "TsumoRon", "Han", "Fu"],
        onlylast: bool = True):
    res = crud.exec_select_sql("Result", cols, f"{wherecol} = {whereval}")

    col_names = [RESULT_PASCAL_TO_SNAKE[col] for col in cols]

    if onlylast:
        ret = {}
        for i in range(len(col_names)):
            ret[col_names[i]] = res[-1][i]
        return ret
    else:
        ret = []
        for r in res:
            ret0 = {}
            for i in range(len(col_names)):
                ret0[col_names[i]] = r[i]
            ret.append(ret0)
        return ret

def update_result(whereval: Union[int, None], vals: Dict[str, Union[int, None]],
        wherecol: str = "ResultID"):
    keys = [RESULT_SNAKE_TO_PASCAL[key] for key in list(vals.keys())]
    values = list(vals.values())
    crud.exec_update_sql(table="Result",
                        cols=keys,
                        vals=values,
                        where=f"{wherecol} = {whereval}")

def create_riichi(vals: List[int], cols: List[str] = \
        ["ResultID", "Player1Riichi", "Player2Riichi", "Player3Riichi", "Player4Riichi"]):
    return crud.exec_insert_sql("Riichi", vals, cols)

def read_riichi(whereval: int , wherecol: str = "RiichiID",
        cols: List[str] = ["ResultID", "Player1Riichi", "Player2Riichi",
                            "Player3Riichi", "Player4Riichi"],
        onlylast: bool = True):
    res = crud.exec_select_sql("Riichi", cols, f"{wherecol} = {whereval}")
    
    if onlylast:
        return res[-1]
    else:
        return res

def create_tenpai(vals: List[int], cols: List[str] = \
        ["ResultID", "Player1Tenpai", "Player2Tenpai", "Player3Tenpai", "Player4Tenpai"]):
    return crud.exec_insert_sql("Tenpai", vals, cols)

def read_tenpai(whereval: int , wherecol: str = "TenpaiID",
        cols: List[str] = ["ResultID", "Player1Tenpai", "Player2Tenpai",
                            "Player3Tenpai", "Player4Tenpai"],
        onlylast: bool = True):
    res = crud.exec_select_sql("Tenpai", cols, f"{wherecol} = {whereval}")
    
    if onlylast:
        return res[-1]
    else:
        return res