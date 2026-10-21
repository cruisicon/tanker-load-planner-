# Tanker Load Planner

**Version:** 0.1.0  
**Status:** Active Development 🚧

Tanker Load Planner (TLP) is a Python-based load planning application designed to help fuel tanker drivers calculate petroleum product weights, validate compartment loading plans, and eventually estimate loaded vehicle axle weights.

The project is being developed incrementally as both a practical tool and a software engineering learning experience.

## Current Features

### Product Weight Calculations

- Calculate petroleum product density using API gravity and observed temperature.
- Calculate total product weight from gallons and density.
- Calculate individual compartment product weights.
- Calculate estimated loaded gross vehicle weight.
- Validate that the compartment gallons match the requested load.

### Configurable Compartments

- Support different numbers of trailer compartments.
- Accept manufacturer data-plate nominal capacities.
- Validate proposed gallons against compartment capacities.
- Enforce a 100-gallon margin below nominal capacity for load recommendations.
- Reject invalid or inconsistent loading inputs.

### Axle Weight Calculations (Experimental)

- Calculate axle-weight changes using empty and loaded scale tickets.
- Maintain historical calibration load data.
- Estimate loaded steer, drive, and trailer axle weights.
- Compare predicted axle weights against actual measurements.

Two experimental prediction approaches have been implemented:

**Baseline Model:** Uses historical average axle-weight distribution to estimate loaded axle weights.

**Position-Sensitive Model:** Uses the weighted position of product across compartments to adjust axle-weight predictions.

These models are preliminary and have not been validated for operational loading decisions.

## Calibration Data

Initial axle-prediction development uses three historical calibration loads collected from a four-compartment Heil petroleum tanker trailer.

The reference trailer has manufacturer nominal compartment capacities of:

| Compartment | Nominal Capacity |
|---|---:|
| 1 | 3,100 gallons |
| 2 | 2,500 gallons |
| 3 | 1,000 gallons |
| 4 | 3,000 gallons |

Calibration records contain compartment loading quantities, empty axle weights, loaded axle weights, and additional observations.

Future calibration will use additional scale tickets to evaluate and improve prediction accuracy.

## Testing

The project currently has **40 passing automated unit tests**.

Testing covers:

- Petroleum calculations
- Input validation
- Compartment capacity validation
- Axle-weight calculations
- Prediction error calculations
- Prediction weight conservation
- Position-sensitive prediction behavior

Tests can be executed with:

```bash
python -m unittest discover -v
```

Passing tests verify the implemented behavior; they do not establish real-world axle prediction accuracy.

## Current Development Priorities

1. Compare the baseline and position-sensitive axle models against historical calibration data.
2. Measure prediction errors using leave-one-out validation.
3. Estimate trailer compartment geometry and load centers.
4. Improve the physical axle-weight distribution model.
5. Collect additional calibration loads and evaluate accuracy.
6. Integrate validated prediction functionality into the main planner.

## Future Features

- Saved truck and trailer configurations
- SQLite database integration
- Product selection and saved product specifications
- BOL-assisted product data entry
- Axle and gross-weight limit warnings
- Historical load records and calibration tracking
- Web-based user interface
- Mobile-friendly load planning workflow

## Technologies

**Current:**
- Python
- Python `unittest`
- Git and GitHub

**Planned:**
- SQLite
- Flask or a similar Python web framework
- HTML/CSS
- Web-based user interface

## Development

Tanker Load Planner is being developed incrementally while I learn Python, testing, software design, and application development.

The project is also intended to provide practical experience with Git, GitHub, data modeling, input validation, and secure software development.

Each major feature is implemented and tested separately before being integrated into the larger application.

## Disclaimer

Tanker Load Planner is an educational software project and experimental load-planning aid.

Calculated weights and predicted axle distributions are estimates. Axle-prediction models have not been validated or certified for legal weight compliance, safe loading decisions, or commercial vehicle operation.

The application does not replace certified scale measurements, official Bills of Lading, applicable laws and regulations, manufacturer specifications, company policies, or required safety procedures.

Drivers and operators remain responsible for verifying vehicle weights, product information, compartment capacities, and regulatory compliance before operating a commercial vehicle.