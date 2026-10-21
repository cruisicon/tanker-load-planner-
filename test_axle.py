#!/usr/bin/env python3

import unittest
from axle_data import CALIBRATION_LOADS
from axle import predict_axle_weights

from axle import (
    calculate_added_axle_weights,
    calculate_prediction_error
)

from axle import calculate_load_position, predict_axles_by_position

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

    def test_prediction_conserves_weight(self):

        empty_axles = [9760, 9040, 6480]

        compartment_weights = [
            18000,
            14000,
            6000,
            15000
        ]

        predicted = predict_axle_weights(
            empty_axles,
            compartment_weights,
            CALIBRATION_LOADS
        )

        predicted_payload = sum(predicted) - sum(empty_axles)

        self.assertAlmostEqual(
            predicted_payload,
            sum(compartment_weights),
            places=6
        )

    def test_load_position(self):
        front_heavy = calculate_load_position([30000, 10000, 5000, 5000])
        rear_heavy = calculate_load_position([5000, 5000, 10000, 30000])

        self.assertLess(front_heavy, rear_heavy)


    def test_position_model_conserves_weight(self):
        empty = [9760, 9040, 6480]
        weights = [18000, 14000, 6000, 15000]

        predicted = predict_axles_by_position(
            empty,
            weights,
            CALIBRATION_LOADS
        )

        self.assertAlmostEqual(
            sum(predicted) - sum(empty),
            sum(weights),
            places=6
        )


    def test_position_model_changes_with_split(self):
        empty = [9760, 9040, 6480]

        front_heavy = [20000, 14000, 6000, 13000]
        rear_heavy = [13000, 14000, 6000, 20000]

        front_prediction = predict_axles_by_position(
            empty, front_heavy, CALIBRATION_LOADS
        )

        rear_prediction = predict_axles_by_position(
            empty, rear_heavy, CALIBRATION_LOADS
        )

        self.assertNotAlmostEqual(
            front_prediction[1],
            rear_prediction[1],
            places=6
        )


if __name__ == "__main__":
    unittest.main()