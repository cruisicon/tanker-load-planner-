#!/usr/bin/env python3


# axle_data.py
# Initial axle calibration dataset for the Heil four-compartment trailer.

CALIBRATION_LOADS = [
    {
        "id": 1,
        "product": "Gasoline E10",
        "compartment_gallons": [3000, 2150, 950, 2700],
        "empty_axles": [9760, 9040, 6480],
        "loaded_axles": [11740, 33520, 33620],
        "notes": ""
    },
    {
        "id": 2,
        "product": "Renewable Diesel",
        "compartment_gallons": [2600, 1800, 900, 2600],
        "empty_axles": [9720, 9040, 6480],
        "loaded_axles": [11580, 31640, 33200],
        "notes": ""
    },
    {
        "id": 3,
        "product": "Renewable Diesel",
        "compartment_gallons": [2900, 2050, 950, 2500],
        "empty_axles": [9760, 9000, 6500],
        "loaded_axles": [11900, 34040, 33900],
        "notes": "Minor pre-load gasoline retain"
    }
]

