#!/usr/bin/env python3


import math

from fastapi import FastAPI
from pydantic import BaseModel, Field

from calculations import (
    calculate_specific_gravity,
    calc_density_60,
    convert_density_metric,
    calc_alpha_60,
    calc_ctl,
    calc_observed_density,
)

app = FastAPI(
    title="Tanker Load Planner API",
    version="0.1.0",
    description="Backend API for Tanker Load Planner",
)


class WeightRequest(BaseModel):
    api_gravity: float = Field(gt=-100, le=150, allow_inf_nan=False)
    temperature_f: float = Field(ge=-100, le=200, allow_inf_nan=False)
    gallons: float = Field(gt=0, le=100000, allow_inf_nan=False)


@app.get("/")
def home():
    return {
        "application": "Tanker Load Planner",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/calculate/weight")
def calculate_weight(request: WeightRequest):
    specific_gravity = calculate_specific_gravity(
        request.api_gravity
    )

    density_60 = calc_density_60(specific_gravity)
    density_kg = convert_density_metric(density_60)
    alpha_60 = calc_alpha_60(density_kg)

    ctl = calc_ctl(alpha_60, request.temperature_f)

    observed_density = calc_observed_density(
        density_60, ctl
    )

    if not math.isfinite(observed_density) or observed_density <= 0:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=422,
            detail="Invalid calculated density"
        )

    product_weight = request.gallons * observed_density

    return {
        "api_gravity": request.api_gravity,
        "temperature_f": request.temperature_f,
        "gallons": request.gallons,
        "specific_gravity": round(specific_gravity, 4),
        "density_60_lb_gal": round(density_60, 4),
        "observed_density_lb_gal": round(observed_density, 4),
        "ctl": round(ctl, 5),
        "product_weight_lb": round(product_weight, 2),
    }
