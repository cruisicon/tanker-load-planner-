#!/usr/bin/env python3

import math


def validate_axles(axles):
    if len(axles) != 3:
        raise ValueError("Exactly three axle weights are required.")

    if any(
        not isinstance(weight, (int, float))
        or isinstance(weight, bool)
        or not math.isfinite(weight)
        or weight <= 0
        for weight in axles
    ):
        raise ValueError("Axle weights must be positive, finite numbers.")

def calculate_added_axle_weights(loaded_axles, empty_axles):
    """
    Calculate weight added to each axle group.

    Axle order:
    steer, drives, trailer
    """
    validate_axles(loaded_axles)
    validate_axles(empty_axles)
    added_weights = []

    for loaded, empty in zip(loaded_axles, empty_axles):
        added_weights.append(loaded - empty)

    return added_weights

def calculate_prediction_error(predicted_axles, actual_axles):
    
    validate_axles(predicted_axles)
    validate_axles(actual_axles)
    errors = []

    for predicted, actual in zip(predicted_axles, actual_axles):
        error_lbs = predicted - actual
        error_percent = (error_lbs / actual) * 100

        errors.append({
            "error_lbs": error_lbs,
            "error_percent": error_percent
        })

    return errors