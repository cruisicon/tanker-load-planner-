# Tanker Load Planner

**Version:** 0.1.0  
**Status:** Early Development 🚧

Tanker Load Planner is a Python-based project designed to assist fuel tanker
drivers with load planning calculations.

The project currently calculates product weight and individual compartment
weights based on product density and a proposed compartment split.

The long-term goal is to develop the project into a web-based load planning
tool capable of storing truck and trailer configurations, calculating product
density from BOL or specification data, and estimating loaded axle weights.

## Current Features

- Calculate total product weight
- Enter total gallons to be loaded
- Enter a proposed four-compartment load split
- Calculate the product weight in each compartment
- Compare total compartment gallons against the requested load
- Display formatted weight calculations

## Planned Features

- Product density calculations using BOL or specification data
- Product selection
- Truck and trailer empty weight calculations
- Estimated steer, drive, and trailer axle weights
- Gross vehicle weight calculations
- Compartment capacity validation
- Axle and gross weight limit warnings
- Multiple truck configurations
- Multiple trailer configurations
- Saved compartment capacities
- SQLite database integration
- Web-based user interface
- Input validation and error handling

## Current Calculation Process

The current version uses a temporary product density for testing.

The driver enters:

1. Total gallons of product being loaded
2. Gallons planned for Compartment 1
3. Gallons planned for Compartment 2
4. Gallons planned for Compartment 3
5. Gallons planned for Compartment 4

The program then calculates:

- Total product weight
- Product weight in each compartment
- Combined compartment gallons
- Whether the proposed compartment split matches the requested load

## Example

Example load:

    Total Product: 7000 gallons

    Compartment 1: 2,600 gallons
    Compartment 2:  900 gallons
    Compartment 3:  900 gallons
    Compartment 4: 2,600 gallons

The program calculates the product weight in each compartment and verifies
the proposed compartment distribution against the requested total gallons.

## Future BOL Integration

A future version is planned to use product information from a Bill of Lading
(BOL) or applicable product specification data rather than relying on a
hard-coded product density.

This will allow the application to calculate the appropriate product weight
using information associated with the current load.

## Future Vehicle Database

Future versions are planned to store truck and trailer configuration data in
a database.

Stored information may include:

- Truck/unit identifier
- Trailer identifier
- Empty axle weights
- Trailer compartment capacities
- Vehicle configuration information

Drivers will eventually be able to select a truck and trailer configuration
instead of manually entering the same vehicle information for each load.

## Technologies

### Current

- Python

### Planned

- SQLite
- Flask or similar Python web framework
- HTML/CSS
- Web-based user interface

## Development

This project is being developed incrementally while I learn Python and
software development.

New functionality will be added as the project progresses, with each major
feature being developed and tested separately.

The project is also intended to provide practical experience with:

- Python programming
- Git and GitHub
- Database design
- Web application development
- Input validation
- Testing
- Secure software development

## Disclaimer

Tanker Load Planner is an educational software project and load-planning aid.

All calculated weights and load distributions should be considered estimates.
The application is not a substitute for certified scale weights, official
Bills of Lading, applicable laws and regulations, equipment limitations,
company policies, or required safety procedures.

Drivers and operators remain responsible for verifying vehicle weights,
product information, compartment capacities, and regulatory compliance before
operating a commercial vehicle.
