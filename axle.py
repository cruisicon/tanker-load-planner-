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

def predict_axle_weights(
    empty_axles,
    compartment_weights,
    calibration_loads
):
    """
    Predict loaded axle weights using historical
    calibration data.
    """

    validate_axles(empty_axles)

    if not calibration_loads:
        raise ValueError("Calibration data is required.")

    if not compartment_weights or any(
        not isinstance(weight, (int, float))
        or isinstance(weight, bool)
        or not math.isfinite(weight)
        or weight < 0
        for weight in compartment_weights
    ):
        raise ValueError("Invalid compartment weights.")

    payload = sum(compartment_weights)

    if payload <= 0:
        raise ValueError("Product payload must be positive.")

    axle_shares = []

    for load in calibration_loads:
        added = calculate_added_axle_weights(
            load["loaded_axles"],
            load["empty_axles"]
        )

        total_added = sum(added)

        if total_added <= 0:
            raise ValueError("Invalid calibration payload.")

        axle_shares.append([
            weight / total_added
            for weight in added
        ])

    average_shares = [
        sum(shares[i] for shares in axle_shares) / len(axle_shares)
        for i in range(3)
    ]

    predicted_added = [
        payload * share
        for share in average_shares
    ]

    predicted_loaded = [
        empty + added
        for empty, added in zip(empty_axles, predicted_added)
    ]

    return predicted_loaded
