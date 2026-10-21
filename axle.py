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


def calculate_load_position(compartment_weights):
    """
    Calculate the weighted average compartment position.

    Positions are normalized from 0 (front) to 1 (rear).
    """
    if not compartment_weights or any(
        not isinstance(w, (int, float))
        or isinstance(w, bool)
        or not math.isfinite(w)
        or w < 0
        for w in compartment_weights
    ):
        raise ValueError("Invalid compartment weights.")

    total_weight = sum(compartment_weights)

    if total_weight <= 0:
        raise ValueError("Payload must be positive.")

    count = len(compartment_weights)

    if count == 1:
        return 0.5

    positions = [
        i / (count - 1)
        for i in range(count)
    ]

    return sum(
        position * weight
        for position, weight in zip(positions, compartment_weights)
    ) / total_weight


def predict_axles_by_position(
    empty_axles,
    compartment_weights,
    calibration_loads,
    regularization=0.01
):
    """
    Preliminary position-sensitive axle prediction.

    Uses historical axle shares and a regularized linear
    relationship with the load's weighted position.
    """

    validate_axles(empty_axles)

    if not calibration_loads:
        raise ValueError("Calibration data is required.")

    if not math.isfinite(regularization) or regularization <= 0:
        raise ValueError("Regularization must be positive.")

    current_position = calculate_load_position(compartment_weights)
    current_payload = sum(compartment_weights)

    positions = []
    axle_shares = []

    for load in calibration_loads:
        gallons = load["compartment_gallons"]

        added = calculate_added_axle_weights(
            load["loaded_axles"],
            load["empty_axles"]
        )

        total_added = sum(added)

        if total_added <= 0:
            raise ValueError("Invalid calibration payload.")

        # Scale-derived density for historical loads.
        density = total_added / sum(gallons)

        weights = [g * density for g in gallons]

        positions.append(calculate_load_position(weights))

        axle_shares.append([
            weight / total_added
            for weight in added
        ])

    mean_position = sum(positions) / len(positions)

    position_variance = sum(
        (p - mean_position) ** 2 for p in positions
    )

    predicted_shares = []

    for axle in range(3):
        shares = [row[axle] for row in axle_shares]
        mean_share = sum(shares) / len(shares)

        covariance = sum(
            (p - mean_position) * (s - mean_share)
            for p, s in zip(positions, shares)
        )

        slope = covariance / (position_variance + regularization)

        predicted_share = (
            mean_share + slope * (current_position - mean_position)
        )

        predicted_shares.append(predicted_share)

    # Normalize shares so total predicted payload is conserved.
    predicted_shares = [
        max(0.0, share) for share in predicted_shares
    ]

    share_total = sum(predicted_shares)

    if share_total <= 0:
        raise ValueError("Invalid predicted axle distribution.")

    predicted_shares = [
        share / share_total for share in predicted_shares
    ]

    return [
        empty + current_payload * share
        for empty, share in zip(empty_axles, predicted_shares)
    ]

