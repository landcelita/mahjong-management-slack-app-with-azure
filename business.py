from typing import List, Union, Dict
from const import SCORE


def calc_new_score_tsumo(result: Dict[str, Union[int, None]], 
                    riichis: List[Union[int, bool]],
                    scores: List[int], 
                    game_status: Dict[str, Union[int, bool]]):
    new_scores = scores

    # 供託金に移動
    for i in range(len(riichis)):
        new_scores[i] -= 1000
        new_scores[4] += 1000

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
    new_scores[result['winner'] - 1] += new_scores[4]
    new_scores[4] = 0

    return new_scores

def calc_new_status_tsumo(result: Dict[str, Union[int, None]], 
                    riichis: List[Union[int, bool]],
                    scores: List[int], 
                    game_status: Dict[str, Union[int, bool]]):
    return game_status # ダミー　あとできちんと実装する
