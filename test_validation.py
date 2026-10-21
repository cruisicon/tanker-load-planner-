#!/usr/bin/env python3

import unittest

from validation import validate_compartment


class TestValidation(unittest.TestCase):

    # Verify a load below the permitted maximum is accepted.
    def test_valid_compartment(self):
        result = validate_compartment(2750, 3100)
        self.assertTrue(result)

    # Verify a load above the permitted maximum is rejected.
    def test_over_capacity(self):
        result = validate_compartment(3050, 3100)
        self.assertFalse(result)

    # Verify a negative load is rejected.
    def test_negative_gallons(self):
        result = validate_compartment(-100, 3100)
        self.assertFalse(result)

    # Verify a load exactly at the permitted maximum is accepted.
    def test_exact_maximum(self):
        result = validate_compartment(3000, 3100)
        self.assertTrue(result)

    # Verify one gallon above the permitted maximum is rejected.
    def test_one_gallon_over(self):
        result = validate_compartment(3001, 3100)
        self.assertFalse(result)

        # Reject NaN values.
    def test_nan_gallons(self):
        self.assertFalse(validate_compartment(float("nan"), 3100))


    # Reject infinite values.
    def test_infinite_gallons(self):
        self.assertFalse(validate_compartment(float("inf"), 3100))


    # Reject nominal capacities smaller than the safety margin.
    def test_invalid_nominal_capacity(self):
        self.assertFalse(validate_compartment(0, 50))


    # Reject nonnumeric inputs.
    def test_nonnumeric_gallons(self):
        self.assertFalse(validate_compartment("abc", 3100))


if __name__ == "__main__":
    unittest.main()