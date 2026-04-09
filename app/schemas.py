from pydantic import BaseModel, validator

class AddressCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

    @validator("latitude")
    def valid_lat(cls, v):
        if v < -90 or v > 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return v

    @validator("longitude")
    def valid_lon(cls, v):
        if v < -180 or v > 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return v
