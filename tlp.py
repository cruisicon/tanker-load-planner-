import math

version = "0.1.0"


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




#-------------------------------------------------------------------------------------------------------------------

print(f"Tanker Load Planner v{version}")

#empty weight calculations for Truck/Trailer combination
emp_steer = int(input("What is your empty steer axle weight from your most recent scale ticket? "))
emp_drives = int(input("What is your empty drive axle weight from your most recent scale ticket? "))
emp_trailer = int(input("What is your empty trailer axle weight from your most recent scale ticket? "))

emp_gross = emp_steer + emp_drives + emp_trailer
print(f"Your Gross empty weight is : {emp_gross:,} ")

#Calculate target payload based on 79,600 lb target gross weight 
target_gross = 79600
target_payload = target_gross - emp_gross
print(f"You have space for {target_payload:,} lbs of product. ")

#Product density
api_gravity = float(input("Enter API gravity from recent BOL: "))
temperature = float(input("Enter Temperature from recent BOL: "))

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

total_gallons = int(input("How many total gallons would you like to load? "))

#ask driver for proposed compartment split
comp_1 = float(input("How many gallons would you like in Compartment one? "))
comp_2 = float(input("How many gallons would you like in Compartment two? "))
comp_3 = float(input("How many gallons would you like in Compartment three? "))
comp_4 = float(input("How many gallons would you like in Compartment four? "))

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

