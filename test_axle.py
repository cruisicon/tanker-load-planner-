#!/usr/bin/env python3

import unittest

from axle import (
    calculate_added_axle_weights,
    calculate_prediction_error
)


class TestAxle(unittest.TestCase):

    def test_added_axle_weights(self):
        result = calculate_added_axle_weights(
            [11740, 33520, 33620],
            [9760, 9040, 6480]
        )

        self.assertEqual(result, [1980, 24480, 27140])

    def test_prediction_error(self):
        result = calculate_prediction_error(
            [11850, 33800, 34100],
            [11900, 34040, 33900]
        )

        self.assertEqual(result[0]["error_lbs"], -50)
        self.assertEqual(result[1]["error_lbs"], -240)
        self.assertEqual(result[2]["error_lbs"], 200)

    def test_invalid_axle_count(self):
        with self.assertRaises(ValueError):
            calculate_added_axle_weights(
                [11740, 33520],
                [9760, 9040, 6480]
            )

    def test_zero_axle_weight(self):
        with self.assertRaises(ValueError):
            calculate_prediction_error(
                [0, 33800, 34100],
                [11900, 34040, 33900]
            )


if __name__ == "__main__":
    unittest.main()