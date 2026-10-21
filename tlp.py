#!/usr/bin/env python3

from inputs import get_integer, get_float

from calculations import (
    calculate_specific_gravity,
    calc_density_60,
    convert_density_metric,
    calc_alpha_60,
    calc_ctl,
    calc_observed_density
)

version = "0.1.0"

#-------------------------------------------------------------------------------------------------------------------

print(f"Tanker Load Planner v{version}")

#empty weight calculations for Truck/Trailer combination
emp_steer = get_integer("What is your empty steer axle weight from your most recent scale ticket? ")
emp_drives = get_integer("What is your empty drive axle weight from your most recent scale ticket? ")
emp_trailer = get_integer("What is your empty trailer axle weight from your most recent scale ticket? ")

emp_gross = emp_steer + emp_drives + emp_trailer
print(f"Your Gross empty weight is : {emp_gross:,} ")

#Calculate target payload based on 79,600 lb target gross weight 
target_gross = 79600
target_payload = target_gross - emp_gross
print(f"You have space for {target_payload:,} lbs of product. ")

#Product density
api_gravity = get_float("Enter API gravity from recent BOL: ")
temperature = get_float("Enter Temperature from recent BOL: ", min_value=-100)

prod_specific_gravity = calculate_specific_gravity(api_gravity)
print(f"Specific Gravity @ 60F: {prod_specific_gravity:.4f}")

prod_density = calc_density_60(prod_specific_gravity)
print(f"Density @ 60F = {prod_density:,.4f}lb/gal ")

density_kg = convert_density_metric(prod_density)
print(f"Density @ 60F: {density_kg:.4f} kg/m³")

alpha_60 = calc_alpha_60(density_kg)
print(f"Alpha @ 60F: {alpha_60:,.7f}")

prod_ctl = calc_ctl(alpha_60, temperature)
print(f"CTL: {prod_ctl:,.5f}")

observed_density = calc_observed_density(prod_density, prod_ctl)
print(f"Observed Density: {observed_density:,.4f} lb/gal")


recommended_gallons = target_payload / observed_density
print(f"Recommended Gallons: {recommended_gallons:,.0f} ")

total_gallons = get_integer("How many total gallons would you like to load? ")

#ask driver for proposed compartment split
comp_1 = get_float("How many gallons would you like in Compartment one? ")
comp_2 = get_float("How many gallons would you like in Compartment two? ")
comp_3 = get_float("How many gallons would you like in Compartment three? ")
comp_4 = get_float("How many gallons would you like in Compartment four? ")

#calculate compartment weights
comp_1w = comp_1 * observed_density
comp_2w = comp_2 * observed_density
comp_3w = comp_3 * observed_density
comp_4w = comp_4 * observed_density

print(f"Compartment 1: {comp_1} gals / {comp_1w:,.2f} lbs")
print(f"Compartment 2: {comp_2} gals / {comp_2w:,.2f} lbs")
print(f"Compartment 3: {comp_3} gals / {comp_3w:,.2f} lbs")
print(f"Compartment 4: {comp_4} gals / {comp_4w:,.2f} lbs")


#confirm that combined compartment gallons does not exceed total gallons
total_comp_gals = comp_1 + comp_2 + comp_3 + comp_4

if total_comp_gals == total_gallons:
    print("Compartment gallons equal total gallons.")
elif total_comp_gals < total_gallons:
    print("Compartment gallons are less than total gallons.")
else:
    print("You have exceeded your total gallons!")


prod_weight = comp_1w + comp_2w + comp_3w + comp_4w
print(f"Product Weight: {prod_weight:,.2f} lbs")
gross_weight = prod_weight + emp_gross
print(f"Gross weight: {gross_weight:,.2f} lbs ")

