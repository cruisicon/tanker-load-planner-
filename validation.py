#!/usr/bin/env python3

import math
# Safety margin below the manufacturer's data-plate capacity.
SAFETY_MARGIN = 100


# Validates a proposed compartment load against its nominal capacity.
# Returns True if the load is within the permitted limit.
def validate_compartment(gallons, nominal_capacity):

    # Reject nonnumeric and non-finite values.
    if not all(
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        for value in (gallons, nominal_capacity)
    ):
        return False

    # Reject invalid nominal capacities.
    if nominal_capacity <= SAFETY_MARGIN:
        return False

    # Reject negative gallons.
    if gallons < 0:
        return False

    # Enforce the compartment loading ceiling.
    max_gallons = nominal_capacity - SAFETY_MARGIN

    return gallons <= max_gallons