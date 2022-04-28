import unittest
from business import calc_new_status_tsumo, calc_new_score_tsumo

class Test_calc_new_score_tsumo(unittest.TestCase):
    def test_calc_new_score_tsumo_1(self):
        result = {
            'tsumo_ron': 0,
            'winner': 1,
            'han': 1,
            'fu': 30
        }
        riichis = [True, False, False, False]
        scores = [25000, 25000, 25000, 25000, 0]
        game_status = {
            'tonpu_or_hanchan': 1,
            'ba': 1,
            'kyoku': 1,
            'honba': 0,
            'finished': False
        }

        actual = calc_new_score_tsumo(result, riichis, scores, game_status)
        expected = [26500, 24500, 24500, 24500, 0]
        self.assertEqual(actual, expected)

    def test_calc_new_score_tsumo_2(self):
        result = {
            'tsumo_ron': 0,
            'winner': 2,
            'han': 5
        }
        riichis = [True, False, True, False]
        scores = [24000, 25000, 25000, 24000, 2000]
        game_status = {
            'tonpu_or_hanchan': 1,
            'ba': 1,
            'kyoku': 3,
            'honba': 2,
            'finished': False
        }

        actual = calc_new_score_tsumo(result, riichis, scores, game_status)
        expected = [20800, 37600, 19800, 21800, 0]
        self.assertEqual(actual, expected)

    def test_calc_new_score_tsumo_3(self):
        result = {
            'tsumo_ron': 0,
            'winner': 4,
            'han': 3000
        }
        riichis = [True, True, True, False]
        scores = [0, 0, 0, 0, 100000]
        game_status = {
            'tonpu_or_hanchan': 1,
            'ba': 2,
            'kyoku': 4,
            'honba': 4,
            'finished': False
        }

        actual = calc_new_score_tsumo(result, riichis, scores, game_status)
        expected = [-49400, -49400, -49400, 248200, 0]
        self.assertEqual(actual, expected)

class Test_calc_new_status_tsumo(unittest.TestCase):
    def test_calc_new_status_tsumo_1(self):
        # 東一局1本場で親がツモって1位になったとき
        result = {
            'tsumo_ron': 0,
            'winner': 1,
            'han': 1,
            'fu': 30
        }
        scores = [28000, 22000, 25000, 25000, 0]
        game_status = {
            'tonpu_or_hanchan': 0,
            'ba': 1,
            'kyoku': 1,
            'honba': 1,
            'finished': False
        }

        actual = calc_new_status_tsumo(result, scores, game_status)
        expected = {
            'tonpu_or_hanchan': 0,
            'ba': 1,
            'kyoku': 1,
            'honba': 2,
            'finished': False
        }
        self.assertEqual(actual, expected)

    def test_calc_new_status_tsumo_2(self):
        # 東一局5本場で親がツモって子が飛んだとき
        result = {
            'tsumo_ron': 0,
            'winner': 1,
            'han': 1,
            'fu': 40
        }
        scores = [50100, -100, 25000, 25000, 0]
        game_status = {
            'tonpu_or_hanchan': 0,
            'ba': 1,
            'kyoku': 1,
            'honba': 5,
            'finished': False
        }

        actual = calc_new_status_tsumo(result, scores, game_status)
        expected = {
            'tonpu_or_hanchan': 0,
            'ba': 1,
            'kyoku': 1,
            'honba': 5,
            'finished': True
        }
        self.assertEqual(actual, expected)

    def test_calc_new_status_tsumo_3(self):
        # 東風戦、東四局で子がツモったとき
        result = {
            'tsumo_ron': 0,
            'winner': 1,
            'han': 1,
            'fu': 40
        }
        scores = [16000, 25000, 10000, 60000, 0]
        game_status = {
            'tonpu_or_hanchan': 0,
            'ba': 1,
            'kyoku': 4,
            'honba': 0,
            'finished': False
        }

        actual = calc_new_status_tsumo(result, scores, game_status)
        expected = {
            'tonpu_or_hanchan': 0,
            'ba': 1,
            'kyoku': 4,
            'honba': 0,
            'finished': True
        }
        self.assertEqual(actual, expected)

    def test_calc_new_status_tsumo_4(self):
        # 半荘戦、東四局で子がツモったとき
        result = {
            'tsumo_ron': 0,
            'winner': 1,
            'han': 1,
            'fu': 40
        }
        scores = [16000, 25000, 10000, 60000, 0]
        game_status = {
            'tonpu_or_hanchan': 1,
            'ba': 1,
            'kyoku': 4,
            'honba': 0,
            'finished': False
        }

        actual = calc_new_status_tsumo(result, scores, game_status)
        expected = {
            'tonpu_or_hanchan': 1,
            'ba': 2,
            'kyoku': 1,
            'honba': 0,
            'finished': False
        }
        self.assertEqual(actual, expected)
    
    def test_calc_new_status_tsumo_5(self):
        # 東風戦、東四局で親がツモって一位でないとき
        result = {
            'tsumo_ron': 0,
            'winner': 4,
            'han': 1,
            'fu': 40
        }
        scores = [30000, 30000, 30000, 10000, 0]
        game_status = {
            'tonpu_or_hanchan': 0,
            'ba': 1,
            'kyoku': 4,
            'honba': 0,
            'finished': False
        }

        actual = calc_new_status_tsumo(result, scores, game_status)
        expected = {
            'tonpu_or_hanchan': 0,
            'ba': 1,
            'kyoku': 4,
            'honba': 1,
            'finished': False
        }
        self.assertEqual(actual, expected)

    def test_calc_new_status_tsumo_6(self):
        # 東風戦、東四局で親がツモって一位のとき
        result = {
            'tsumo_ron': 0,
            'winner': 4,
            'han': 1,
            'fu': 40
        }
        scores = [24000, 24000, 24000, 28000, 0]
        game_status = {
            'tonpu_or_hanchan': 0,
            'ba': 1,
            'kyoku': 4,
            'honba': 0,
            'finished': False
        }

        actual = calc_new_status_tsumo(result, scores, game_status)
        expected = {
            'tonpu_or_hanchan': 0,
            'ba': 1,
            'kyoku': 4,
            'honba': 0,
            'finished': True
        }
        self.assertEqual(actual, expected)

    def test_calc_new_status_tsumo_7(self):
        # 半荘戦、東四局で親がツモって一位のとき
        result = {
            'tsumo_ron': 0,
            'winner': 4,
            'han': 1,
            'fu': 40
        }
        scores = [24000, 24000, 24000, 28000, 0]
        game_status = {
            'tonpu_or_hanchan': 1,
            'ba': 1,
            'kyoku': 4,
            'honba': 0,
            'finished': False
        }

        actual = calc_new_status_tsumo(result, scores, game_status)
        expected = {
            'tonpu_or_hanchan': 1,
            'ba': 1,
            'kyoku': 4,
            'honba': 1,
            'finished': False
        }
        self.assertEqual(actual, expected)

    def test_calc_new_status_tsumo_8(self):
        # 半荘戦、南四局で親がツモって一位のとき
        result = {
            'tsumo_ron': 0,
            'winner': 4,
            'han': 1,
            'fu': 40
        }
        scores = [24000, 24000, 24000, 28000, 0]
        game_status = {
            'tonpu_or_hanchan': 1,
            'ba': 2,
            'kyoku': 4,
            'honba': 0,
            'finished': False
        }

        actual = calc_new_status_tsumo(result, scores, game_status)
        expected = {
            'tonpu_or_hanchan': 1,
            'ba': 2,
            'kyoku': 4,
            'honba': 0,
            'finished': True
        }
        self.assertEqual(actual, expected)

    def test_calc_new_status_tsumo_9(self):
        # 半荘戦、南四局で子がツモったとき
        result = {
            'tsumo_ron': 0,
            'winner': 1,
            'han': 1,
            'fu': 40
        }
        scores = [30000, 24000, 24000, 22000, 0]
        game_status = {
            'tonpu_or_hanchan': 1,
            'ba': 2,
            'kyoku': 4,
            'honba': 1,
            'finished': False
        }

        actual = calc_new_status_tsumo(result, scores, game_status)
        expected = {
            'tonpu_or_hanchan': 1,
            'ba': 2,
            'kyoku': 4,
            'honba': 1,
            'finished': True
        }
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
