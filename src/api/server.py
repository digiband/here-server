"""
Here Server - FastAPI Application
Accepts location data and returns information about the location.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

app = FastAPI(
    title="Here Server",
    description="Backend for the Here App - finds interesting info about nearby points of interest",
    version="0.1.0"
)

# Allow CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize geocoder
geolocator = Nominatim(user_agent="here-server")


class LocationRequest(BaseModel):
    """Request model for location endpoint."""
    lat: float = Field(..., description="Latitude from GPS", ge=-90, le=90)
    lon: float = Field(..., description="Longitude from GPS", ge=-180, le=180)


class LocationResponse(BaseModel):
    """Response model for location endpoint."""
    lat: float
    lon: float
    location_name: str
    success: bool
    error: str | None = None


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "Here Server"}


@app.post("/location", response_model=LocationResponse)
async def get_location_name(request: LocationRequest):
    """
    Accept GPS coordinates and return the name of the location.

    Uses reverse geocoding to convert lat/lon to a human-readable location name.
    """
    try:
        location = geolocator.reverse(
            (request.lat, request.lon),
            exactly_one=True,
            language="en"
        )

        if location:
            return LocationResponse(
                lat=request.lat,
                lon=request.lon,
                location_name=location.address,
                success=True
            )
        else:
            return LocationResponse(
                lat=request.lat,
                lon=request.lon,
                location_name="Unknown location",
                success=False,
                error="Could not determine location name"
            )

    except GeocoderTimedOut:
        return LocationResponse(
            lat=request.lat,
            lon=request.lon,
            location_name="Unknown location",
            success=False,
            error="Geocoding service timed out"
        )
    except GeocoderServiceError as e:
        return LocationResponse(
            lat=request.lat,
            lon=request.lon,
            location_name="Unknown location",
            success=False,
            error=f"Geocoding service error: {str(e)}"
        )
