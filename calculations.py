#!/usr/bin/env python3

import math

#Coefficient lists [K0, K1, K2]
gasoline = [192.4571, 0.2438, 0]
transition = [1489.067, 0, -0.0018684]
jet_fuel = [330.301, 0, 0]
fuel_oil = [103.8720, 0.2701,0]

#function calculates specific gravity @ 60F using API gravity from BOL
def calculate_specific_gravity(api_gravity):
    specific_gravity = 141.5 / (api_gravity + 131.5)
    return specific_gravity

#calculates product density in pounds per gallon @ 60F
def calc_density_60(specific_gravity):
    density_60 = specific_gravity * 8.337193
    return density_60

# Converts product density from lb/gal to kg/m3
def convert_density_metric(density_lbs):
    density_kg = density_lbs * 119.826427
    return density_kg

# Selects the correct coefficient range based on product density
# and calculates the thermal expansion coefficient at 60F
def calc_alpha_60(density_kg):
    if density_kg < 770.3520:
        coefficients = gasoline

    elif density_kg < 787.5195:
        coefficients = transition

    elif density_kg < 838.3127:
        coefficients = jet_fuel
        
    else:
        coefficients = fuel_oil

    alpha_60 = coefficients[0] / (density_kg ** 2) + coefficients[1] / density_kg + coefficients[2]

    return alpha_60

# Calculates the Correction for Temperature of Liquid (CTL)
# using the product expansion coefficient and observed BOL temperature
def calc_ctl(alpha_60, temperature):
    delta_temp = temperature - 60
    ctl = math.exp((-alpha_60 * delta_temp) * (1 + 0.8 * alpha_60 * delta_temp))
    return ctl

def calc_observed_density(density_60, ctl):
    observed_density = ctl * density_60
    return observed_density

