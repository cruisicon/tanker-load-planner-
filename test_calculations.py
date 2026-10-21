#!/usr/bin/env

import unittest

from calculations import (
    calculate_specific_gravity,
    calc_density_60,
    convert_density_metric,
    calc_ctl,
    calc_alpha_60,
    calc_observed_density
)


class TestCalculations(unittest.TestCase):

    # Verify specific gravity for an API gravity of 50.
    def test_specific_gravity(self):
        result = calculate_specific_gravity(50)
        expected = 141.5 / 181.5
        self.assertAlmostEqual(result, expected, places=6)

    # Verify density at 60°F using a known specific gravity.
    def test_density_60(self):
        result = calc_density_60(0.78)
        expected = 6.50301054
        self.assertAlmostEqual(result, expected, places=6)

    # Verify conversion from lb/gal to kg/m³.
    def test_metric_conversion(self):
        result = convert_density_metric(6.5)
        expected = 778.8717755
        self.assertAlmostEqual(result, expected, places=6)
    
    # Verify CTL equals 1.0 at the reference temperature of 60°F.
    # Verify CTL equals 1.0 at 60°F.
    def test_ctl_at_60(self):
        result = calc_ctl(0.0007, 60)
        self.assertAlmostEqual(result, 1.0, places=6)

        # Verify CTL decreases as temperature rises above 60°F.
    def test_ctl_above_60(self):
        result = calc_ctl(0.0007, 80)
        self.assertLess(result, 1.0)


    # Verify CTL increases as temperature drops below 60°F.
    def test_ctl_below_60(self):
        result = calc_ctl(0.0007, 40)
        self.assertGreater(result, 1.0)

        # Verify gasoline coefficients are selected.
    def test_alpha_gasoline(self):
        density = 750
        expected = 192.4571 / density**2 + 0.2438 / density
        result = calc_alpha_60(density)
        self.assertAlmostEqual(result, expected, places=8)


    # Verify transition coefficients are selected.
    def test_alpha_transition(self):
        density = 780
        expected = 1489.067 / density**2 - 0.0018684
        result = calc_alpha_60(density)
        self.assertAlmostEqual(result, expected, places=8)


    # Verify jet fuel coefficients are selected.
    def test_alpha_jet_fuel(self):
        density = 810
        expected = 330.301 / density**2
        result = calc_alpha_60(density)
        self.assertAlmostEqual(result, expected, places=8)


    # Verify fuel oil coefficients are selected.
    def test_alpha_fuel_oil(self):
        density = 850
        expected = 103.8720 / density**2 + 0.2701 / density
        result = calc_alpha_60(density)
        self.assertAlmostEqual(result, expected, places=8)   

        # Verify observed density when CTL equals 1.0.
    def test_observed_density_at_60(self):
        result = calc_observed_density(6.5, 1.0)
        self.assertAlmostEqual(result, 6.5, places=6)


    # Verify observed density with temperature correction.
    def test_observed_density_corrected(self):
        result = calc_observed_density(6.5, 0.985)
        self.assertAlmostEqual(result, 6.4025, places=6)   

        # Verify transition coefficients at the exact lower boundary.
    def test_alpha_transition_boundary(self):
        density = 770.3520
        expected = 1489.067 / density**2 - 0.0018684
        result = calc_alpha_60(density)
        self.assertAlmostEqual(result, expected, places=8)


    # Verify jet fuel coefficients at the exact lower boundary.
    def test_alpha_jet_fuel_boundary(self):
        density = 787.5195
        expected = 330.301 / density**2
        result = calc_alpha_60(density)
        self.assertAlmostEqual(result, expected, places=8)


    # Verify fuel oil coefficients at the exact lower boundary.
    def test_alpha_fuel_oil_boundary(self):
        density = 838.3127
        expected = 103.8720 / density**2 + 0.2701 / density
        result = calc_alpha_60(density)
        self.assertAlmostEqual(result, expected, places=8)     

if __name__ == "__main__":
    unittest.main()