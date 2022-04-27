from pprint import pprint
from typing import List, Union, Dict
from const import BA_LAST_KYOKU, HANCHAN, KYOTAKU_INDEX, OLAS_HANCHAN_BA, OLAS_KYOKU, OLAS_TONPU_BA, SCORE, TONPU


def calc_new_score_tsumo(result: Dict[str, Union[int, None]], 
                    riichis: List[Union[int, bool]],
                    scores: List[int], 
                    game_status: Dict[str, Union[int, bool]]):
    new_scores = scores.copy()

    # 供託金に移動
    for i in range(len(riichis)):
        new_scores[i] -= 1000
        new_scores[KYOTAKU_INDEX] += 1000

    # ツモの分
    if result['winner'] == game_status['kyoku']: # 親
        lose = SCORE[str(result['han'])][str(result['fu'])]['oya']['tsumo'] \
                if SCORE[str(result['han'])]['fu_required'] \
                else SCORE[str(result['han'])]['oya']['tsumo']
        lose += 100 * game_status['honba']
        for i in range(1, 5):
            if result['winner'] == i:
                new_scores[i-1] += lose * 3
            else:
                new_scores[i-1] -= lose
    else: # 子
        ko_lose, oya_lose = SCORE[str(result['han'])][str(result['fu'])]['ko']['tsumo'] \
                            if SCORE[str(result['han'])]['fu_required'] \
                            else SCORE[str(result['han'])]['oya']['tsumo']
        ko_lose += 100 * game_status['honba']
        oya_lose += 100 * game_status['honba']
        for i in range(1, 5):
            if result['winner'] == i:
                new_scores[i-1] += ko_lose * 2 + oya_lose
            elif game_status['kyoku'] == i:
                new_scores[i-1] -= oya_lose
            else:
                new_scores[i-1] -= ko_lose

    # 供託金の分
    new_scores[result['winner'] - 1] += new_scores[KYOTAKU_INDEX]
    new_scores[KYOTAKU_INDEX] = 0

    return new_scores

def calc_new_status_tsumo(result: Dict[str, Union[int, None]], 
                    scores: List[int], 
                    game_status: Dict[str, Union[int, bool]]):
    new_game_status = game_status.copy()

    # 終了条件 トビorオーラス(子アガリor親トップ)
    is_finished: bool = False
    if all([x < 0 for x in scores]): is_finished = True
    if is_olas(game_status):
        if result['winner'] != OLAS_KYOKU-1: is_finished = True
        # ラス親は起家から最も遠いので、他家の点数に比べて真に大きくなくてはならない
        if all([x < scores[OLAS_KYOKU-1] for x in scores[0:OLAS_KYOKU-1]]):
            is_finished = True
    if is_finished:
        new_game_status['finished'] = True
        return new_game_status

    # 連チャン条件
    if result['winner'] == game_status['kyoku']:
        new_game_status['honba'] += 1
        return new_game_status

    # 次局
    new_game_status['honba'] = 0
    new_game_status['kyoku'] += 1
    if new_game_status['kyoku'] == BA_LAST_KYOKU + 1:
        new_game_status['ba'] += 1
        new_game_status['kyoku'] = 1

    return new_game_status

def is_olas(game_status):
    if game_status['tonpu_or_hanchan'] == TONPU:
        if game_status['ba'] == OLAS_TONPU_BA and game_status['kyoku'] == OLAS_KYOKU:
            return True
        return False
    elif game_status['tonpu_or_hanchan'] == HANCHAN:
        if game_status['ba'] == OLAS_HANCHAN_BA and game_status['kyoku'] == OLAS_KYOKU:
            return True
        return False