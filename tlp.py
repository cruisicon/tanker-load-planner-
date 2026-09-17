version = "0.1.0"
print(f"Tanker Load Planner v{version}")
#Product density
prod_density = 7.37  # test value for Biodiesel

#ask driver how many gallons are being loaded
prod_gallons = float(input("How many gallons of product are you loading? "))

#calculate product weight
prod_weight = prod_gallons * prod_density



#ask driver for proposed compartment split
comp_1 = float(input("How many gallons would you like in Compartment one? "))
comp_2 = float(input("How many gallons would you like in Compartment two? "))
comp_3 = float(input("How many gallons would you like in Compartment three? "))
comp_4 = float(input("How many gallons would you like in Compartment four? "))

#calculate compartment weights
comp_1w = comp_1 * prod_density
comp_2w = comp_2 * prod_density
comp_3w = comp_3 * prod_density
comp_4w = comp_4 * prod_density

print(f"Compartment 1: {comp_1} gals / {comp_1w:,.2f} lbs")
print(f"Compartment 2: {comp_2} gals / {comp_2w:,.2f} lbs")
print(f"Compartment 3: {comp_3} gals / {comp_3w:,.2f} lbs")
print(f"Compartment 4: {comp_4} gals / {comp_4w:,.2f} lbs")


#confirm that combined compartment gallons does not exceed total gallons
total_comp_gals = comp_1 + comp_2 + comp_3 + comp_4

if total_comp_gals == prod_gallons:
    print("Compartment gallons equal total gallons.")
elif total_comp_gals < prod_gallons:
    print("Compartment gallons are less than total gallons.")
else:
    print("You have exceeded your total gallons!")

print(f"Product Weight: {prod_weight:,.2f} lbs")
