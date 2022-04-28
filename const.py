BA = ['error', '東', '南', '西', '北']

KYOKU = ['error', '一', '二', '三', '四']

FU_MAX = 999999999

RYUKYOKU_WINNER = 0

SCORE = {
    '1': {
        'represent': '1翻',
        'fu_required': True,
        'fu': ['30', '40', '50', '60', '70', '80', '90', '100', '110'],
        '30': { 
            'ko': {'ron': 1000, 'tsumo': [300, 500]},
            'oya': {'ron': 1500, 'tsumo': 500},
        },
        '40': {
            'ko': {'ron': 1300, 'tsumo': [400, 700]},
            'oya': {'ron': 2000, 'tsumo': 700},
        },
        '50': {
            'ko': {'ron': 1600, 'tsumo': [400, 800]},
            'oya': {'ron': 2400, 'tsumo': 800},
        },
        '60': {
            'ko': {'ron': 2000, 'tsumo': [500, 1000]},
            'oya': {'ron': 2900, 'tsumo': 1000},
        },
        '70': {
            'ko': {'ron': 2300, 'tsumo': [600, 1200]},
            'oya': {'ron': 3400, 'tsumo': 1200},
        },
        '80': {
            'ko': {'ron': 2600, 'tsumo': [700, 1300]},
            'oya': {'ron': 3900, 'tsumo': 1300},
        },
        '90': {
            'ko': {'ron': 2900, 'tsumo': [800, 1500]},
            'oya': {'ron': 4400, 'tsumo': 1500},
        },
        '100': {
            'ko': {'ron': 3200, 'tsumo': [800, 1600]},
            'oya': {'ron': 4800, 'tsumo': 1600},
        },
        '110': {
            'ko': {'ron': 3600, 'tsumo': [900, 1800]},
            'oya': {'ron': 5300, 'tsumo': 1800},
        },
    },
    '2': {
        'represent': '2翻',
        'fu_required': True,
        'fu': ['20', '25', '30', '40', '50', '60', '70', '80', '90', '100', '110'],
        '20': {
            'ko': {'ron': None, 'tsumo': [400, 700]},
            'oya': {'ron': None, 'tsumo': 700},
        },
        '25': {
            'ko': {'ron': 1600, 'tsumo': [None, None]},
            'oya': {'ron': 2400, 'tsumo': None},
        },
        '30': {
            'ko': {'ron': 2000, 'tsumo': [500, 1000]},
            'oya': {'ron': 2900, 'tsumo': 1000},
        },
        '40': {
            'ko': {'ron': 2600, 'tsumo': [700, 1300]},
            'oya': {'ron': 3900, 'tsumo': 1300},
        },
        '50': {
            'ko': {'ron': 3200, 'tsumo': [800, 1600]},
            'oya': {'ron': 4800, 'tsumo': 1600},
        },
        '60': {
            'ko': {'ron': 3900, 'tsumo': [1000, 2000]},
            'oya': {'ron': 5800, 'tsumo': 2000},
        },
        '70': {
            'ko': {'ron': 4500, 'tsumo': [1200, 2300]},
            'oya': {'ron': 6800, 'tsumo': 2300},
        },
        '80': {
            'ko': {'ron': 5200, 'tsumo': [1300, 2600]},
            'oya': {'ron': 7700, 'tsumo': 2600},
        },
        '90': {
            'ko': {'ron': 5800, 'tsumo': [1500, 2900]},
            'oya': {'ron': 8700, 'tsumo': 2900},
        },
        '100': {
            'ko': {'ron': 6400, 'tsumo': [1600, 3200]},
            'oya': {'ron': 9600, 'tsumo': 3200},
        },
        '110': {
            'ko': {'ron': 7100, 'tsumo': [1800, 3600]},
            'oya': {'ron': 10600, 'tsumo': 3600},
        },
    },
    '3': {
        'represent': '3翻',
        'fu_required': True,
        'fu': ['20', '25', '30', '40', '50', '60', f'{FU_MAX}'],
        '20': {
            'ko': {'ron': None, 'tsumo': [700, 1300]},
            'oya': {'ron': None, 'tsumo': 1300},
        },
        '25': {
            'ko': {'ron': 3200, 'tsumo': [800, 1600]},
            'oya': {'ron': 4800, 'tsumo': 1600},
        },
        '30': {
            'ko': {'ron': 3900, 'tsumo': [1000, 2000]},
            'oya': {'ron': 5800, 'tsumo': 2000},
        },
        '40': {
            'ko': {'ron': 5200, 'tsumo': [1300, 2600]},
            'oya': {'ron': 7700, 'tsumo': 2600},
        },
        '50': {
            'ko': {'ron': 6400, 'tsumo': [1600, 3200]},
            'oya': {'ron': 9600, 'tsumo': 3200},
        },
        '60': {
            'ko': {'ron': 7700, 'tsumo': [2000, 3900]},
            'oya': {'ron': 11600, 'tsumo': 3900},
        },
        f'{FU_MAX}': {
            'ko': {'ron': 8000, 'tsumo': [2000, 4000]},
            'oya': {'ron': 12000, 'tsumo': 4000},
        }
    },
    '4': {
        'represent': '4翻',
        'fu_required': True,
        'fu': ['20', '25', '30', f'{FU_MAX}'],
        '20': {
            'ko': {'ron': None, 'tsumo': [1300, 2600]},
            'oya': {'ron': None, 'tsumo': 2600},
        },
        '25': {
            'ko': {'ron': 6400, 'tsumo': [1600, 3200]},
            'oya': {'ron': 9600, 'tsumo': 3200},
        },
        '30': {
            'ko': {'ron': 7700, 'tsumo': [2000, 3900]},
            'oya': {'ron': 11600, 'tsumo': 3900},
        },
        f'{FU_MAX}': {
            'ko': {'ron': 8000, 'tsumo': [2000, 4000]},
            'oya': {'ron': 12000, 'tsumo': 4000},
        }
    },
    '5': {
        'represent': '5翻',
        'fu_required': False,
        'ko': {'ron': 8000, 'tsumo': [2000, 4000]},
        'oya': {'ron': 12000, 'tsumo': 4000},
    },
    '6': {
        'represent': '6翻',
        'fu_required': False,
        'ko': {'ron': 12000, 'tsumo': [3000, 6000]},
        'oya': {'ron': 18000, 'tsumo': 6000},
    },
    '7': {
        'represent': '7翻',
        'fu_required': False,
        'ko': {'ron': 12000, 'tsumo': [3000, 6000]},
        'oya': {'ron': 18000, 'tsumo': 6000},
    },
    '8': {
        'represent': '8翻',
        'fu_required': False,
        'ko': {'ron': 16000, 'tsumo': [4000, 8000]},
        'oya': {'ron': 24000, 'tsumo': 8000},
    },
    '9': {
        'represent': '9翻',
        'fu_required': False,
        'ko': {'ron': 16000, 'tsumo': [4000, 8000]},
        'oya': {'ron': 24000, 'tsumo': 8000},
    },
    '10': {
        'represent': '10翻',
        'fu_required': False,
        'ko': {'ron': 16000, 'tsumo': [4000, 8000]},
        'oya': {'ron': 24000, 'tsumo': 8000},
    },
    '11': {
        'represent': '11翻',
        'fu_required': False,
        'ko': {'ron': 24000, 'tsumo': [6000, 12000]},
        'oya': {'ron': 36000, 'tsumo': 12000},
    },
    '12': {
        'represent': '12翻',
        'fu_required': False,
        'ko': {'ron': 24000, 'tsumo': [6000, 12000]},
        'oya': {'ron': 36000, 'tsumo': 12000},
    },
    '1000': {
        'represent': '役満',
        'fu_required': False,
        'ko': {'ron': 32000, 'tsumo': [8000, 16000]},
        'oya': {'ron': 48000, 'tsumo': 16000},
    },
    '2000': {
        'represent': 'ダブル役満',
        'fu_required': False,
        'ko': {'ron': 64000, 'tsumo': [16000, 32000]},
        'oya': {'ron': 96000, 'tsumo': 32000},
    },
    '3000': {
        'represent': 'トリプル役満',
        'fu_required': False,
        'ko': {'ron': 96000, 'tsumo': [24000, 48000]},
        'oya': {'ron': 144000, 'tsumo': 48000},
    }
}

GAMESTATUS_PASCAL_TO_SNAKE = {
    "TonpuOrHanchan": "tonpu_or_hanchan",
    "Ba": "ba",
    "Kyoku": "kyoku",
    "Honba": "honba",
    "Finished": "finished",
}

GAMESTATUS_SNAKE_TO_PASCAL = {
    "tonpu_or_hanchan": "TonpuOrHanchan",
    "ba": "Ba",
    "kyoku": "Kyoku",
    "honba": "Honba",
    "finished": "Finished",
}

RESULT_PASCAL_TO_SNAKE = {
    "GameID": "game_id",
    "Ba": "ba",
    "Kyoku": "kyoku",
    "Honba": "honba",
    "Winner": "winner",
    "TsumoRon": "tsumo_ron",
    "Han": "han",
    "Fu": "fu",
}

RESULT_SNAKE_TO_PASCAL = {
    "game_id": "GameID",
    "ba": "Ba",
    "kyoku": "Kyoku",
    "honba": "Honba",
    "winner": "Winner",
    "tsumo_ron": "TsumoRon",
    "han": "Han",
    "fu": "Fu",
}

KYOTAKU_INDEX = 4

TONPU = 0
HANCHAN = 1
OLAS_KYOKU = 4
OLAS_TONPU_BA = 1
OLAS_HANCHAN_BA = 2
BA_LAST_KYOKU = 4