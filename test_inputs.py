#!/usr/bin/env

import unittest
from unittest.mock import patch

from inputs import get_integer, get_float

class TestInputs(unittest.TestCase):

    # Verify a valid integer is accepted.
    @patch("builtins.input", return_value="2500")
    def test_valid_integer(self, mock_input):
        result = get_integer("Enter gallons: ")
        self.assertEqual(result, 2500)

    # Verify a valid float is accepted.
    @patch("builtins.input", return_value="49.3")
    def test_valid_float(self, mock_input):
        result = get_float("Enter API gravity: ")
        self.assertAlmostEqual(result, 49.3)

     # Verify invalid integer input is rejected before accepting a valid one.
    @patch("builtins.input", side_effect=["abc", "2500"])
    def test_invalid_integer(self, mock_input):
        result = get_integer("Enter gallons: ")

        self.assertEqual(result, 2500)
        self.assertEqual(mock_input.call_count, 2)


    # Verify negative values are rejected before accepting a valid integer.
    @patch("builtins.input", side_effect=["-500", "2500"])
    def test_negative_integer(self, mock_input):
        result = get_integer("Enter gallons: ")

        self.assertEqual(result, 2500)
        self.assertEqual(mock_input.call_count, 2)

    # Verify nonnumeric input is rejected before accepting a valid float.
    @patch("builtins.input", side_effect=["abc", "49.3"])
    def test_invalid_float(self, mock_input):
        result = get_float("Enter API gravity: ")

        self.assertAlmostEqual(result, 49.3)
        self.assertEqual(mock_input.call_count, 2)


    # Verify NaN is rejected before accepting a valid float.
    @patch("builtins.input", side_effect=["nan", "49.3"])
    def test_nan_float(self, mock_input):
        result = get_float("Enter API gravity: ")

        self.assertAlmostEqual(result, 49.3)
        self.assertEqual(mock_input.call_count, 2)


    # Verify infinity is rejected before accepting a valid float.
    @patch("builtins.input", side_effect=["inf", "49.3"])
    def test_infinity_float(self, mock_input):
        result = get_float("Enter API gravity: ")

        self.assertAlmostEqual(result, 49.3)
        self.assertEqual    

    # Verify negative temperatures are accepted when permitted.
    @patch("builtins.input", return_value="-10.5")
    def test_negative_temperature(self, mock_input):
        result = get_float("Enter temperature: ", min_value=-100)

        self.assertAlmostEqual(result, -10.5)
        self.assertEqual(mock_input.call_count, 1)

if __name__ == "__main__":
    unittest.main()