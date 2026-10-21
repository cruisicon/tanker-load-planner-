#!/usr/bin/env python3

import math

from inputs import get_integer, get_float

from calculations import (
    calculate_specific_gravity,
    calc_density_60,
    convert_density_metric,
    calc_alpha_60,
    calc_ctl,
    calc_observed_density
)

from validation import validate_compartment, SAFETY_MARGIN


version = "0.1.0"
TARGET_GROSS = 79600

print(f"\nTanker Load Planner v{version}")
print("-" * 55)


# ---------------------------------------------------------
# EMPTY TRUCK / TRAILER WEIGHTS
# ---------------------------------------------------------

emp_steer = get_integer(
    "What is your empty steer axle weight from your most recent scale ticket? "
)

emp_drives = get_integer(
    "What is your empty drive axle weight from your most recent scale ticket? "
)

emp_trailer = get_integer(
    "What is your empty trailer axle weight from your most recent scale ticket? "
)

emp_gross = emp_steer + emp_drives + emp_trailer

print(f"\nYour gross empty weight is: {emp_gross:,} lbs")

target_payload = TARGET_GROSS - emp_gross

if target_payload <= 0:
    print("ERROR: Empty gross weight meets or exceeds the target.")
    raise SystemExit(1)

print(f"Available product weight: {target_payload:,} lbs")


# ---------------------------------------------------------
# PRODUCT DENSITY CALCULATIONS
# ---------------------------------------------------------

api_gravity = get_float("Enter API gravity from recent BOL: ")

temperature = get_float(
    "Enter temperature from recent BOL: ",
    min_value=-100
)

prod_specific_gravity = calculate_specific_gravity(api_gravity)

prod_density = calc_density_60(prod_specific_gravity)

density_kg = convert_density_metric(prod_density)

alpha_60 = calc_alpha_60(density_kg)

prod_ctl = calc_ctl(alpha_60, temperature)

observed_density = calc_observed_density(
    prod_density,
    prod_ctl
)

if not math.isfinite(observed_density) or observed_density <= 0:
    print("ERROR: Invalid calculated product density.")
    raise SystemExit(1)

print("\n--- Product Density ---")
print(f"Specific Gravity @ 60F: {prod_specific_gravity:.4f}")
print(f"Density @ 60F: {prod_density:,.4f} lb/gal")
print(f"Density @ 60F: {density_kg:.4f} kg/m³")
print(f"Alpha @ 60F: {alpha_60:,.7f}")
print(f"CTL: {prod_ctl:,.5f}")
print(f"Observed Density: {observed_density:,.4f} lb/gal")


# ---------------------------------------------------------
# RECOMMENDED TOTAL GALLONS
# ---------------------------------------------------------

recommended_gallons = target_payload / observed_density

print(f"\nRecommended Gallons: {recommended_gallons:,.0f}")

total_gallons = get_integer(
    "How many total gallons would you like to load? "
)


# ---------------------------------------------------------
# TRAILER COMPARTMENT CONFIGURATION
# ---------------------------------------------------------

num_compartments = get_integer(
    "How many compartments does your trailer have? ",
    min_value=1
)

nominal_capacities = []

print("\nEnter capacities from the manufacturer's data plate.")

for comp in range(1, num_compartments + 1):

    nominal_capacity = get_float(
        f"Nominal capacity for compartment {comp}: ",
        min_value=SAFETY_MARGIN + 1
    )

    nominal_capacities.append(nominal_capacity)


# ---------------------------------------------------------
# PROPOSED COMPARTMENT LOADS
# ---------------------------------------------------------

while True:

    compartment_gallons = []

    print("\n--- Proposed Compartment Split ---")

    for comp, nominal_capacity in enumerate(
        nominal_capacities,
        start=1
    ):

        max_gallons = nominal_capacity - SAFETY_MARGIN

        print(
            f"\nCompartment {comp} "
            f"(TLP maximum: {max_gallons:,.0f} gallons)"
        )

        while True:

            gallons = get_float(
                f"Enter gallons for compartment {comp}: "
            )

            if validate_compartment(gallons, nominal_capacity):
                compartment_gallons.append(gallons)
                break

            print(
                f"Invalid load. Maximum permitted: "
                f"{max_gallons:,.0f} gallons."
            )

    actual_total = sum(compartment_gallons)

    if math.isclose(
        actual_total,
        total_gallons,
        rel_tol=0,
        abs_tol=0.01
    ):
        print("\nCompartment gallons match requested total.")
        break

    print("\nERROR: Compartment gallons do not match requested total.")
    print(f"Requested total: {total_gallons:,.2f} gallons")
    print(f"Compartment total: {actual_total:,.2f} gallons")
    print("Please re-enter the compartment split.")


# ---------------------------------------------------------
# COMPARTMENT WEIGHT CALCULATIONS
# ---------------------------------------------------------

compartment_weights = []

for gallons in compartment_gallons:

    weight = gallons * observed_density

    compartment_weights.append(weight)


print("\n--- Compartment Loading Summary ---")

for comp, (gallons, weight) in enumerate(
    zip(compartment_gallons, compartment_weights),
    start=1
):

    print(
        f"Compartment {comp}: "
        f"{gallons:,.0f} gals / {weight:,.2f} lbs"
    )


# ---------------------------------------------------------
# PRODUCT AND GROSS WEIGHT
# ---------------------------------------------------------

prod_weight = sum(compartment_weights)

gross_weight = prod_weight + emp_gross

print("\n--- Weight Summary ---")

print(f"Empty Gross Weight: {emp_gross:,.2f} lbs")
print(f"Product Weight: {prod_weight:,.2f} lbs")
print(f"Calculated Gross Weight: {gross_weight:,.2f} lbs")
print(f"Target Gross Weight: {TARGET_GROSS:,.2f} lbs")

weight_difference = TARGET_GROSS - gross_weight

if weight_difference >= 0:

    print(
        f"Below target gross by: "
        f"{weight_difference:,.2f} lbs"
    )

else:

    print(
        f"WARNING: Exceeds target gross by "
        f"{abs(weight_difference):,.2f} lbs"
    )
    raise SystemExit(1)

print("\nTLP calculations completed.")
print("Axle-weight distribution has not been validated.")
