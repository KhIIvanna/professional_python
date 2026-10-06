from pydantic import BaseModel, Field

class CarCreate(BaseModel):
    make: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1886, le=2100)
    price: float = Field(ge=0)
    mileage: int = Field(ge=0)
    vin: str | None = Field(default=None, max_length=17)
    manufacturer_id: int | None = Field(default=None, gt=0)

class CarUpdate(BaseModel):
    make: str | None = Field(default=None, min_length=1, max_length=100)
    model: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1886, le=2100)
    price: float | None = Field(default=None, ge=0)
    mileage: int | None = Field(default=None, ge=0)
    vin: str | None = Field(default=None, max_length=17)
    manufacturer_id: int | None = Field(default=None, gt=0)

class CarResponse(BaseModel):
    id: int
    make: str
    model: str
    year: int
    price: float
    mileage: int
    vin: str | None
    manufacturer_id: int | None

    model_config = {
        "from_attributes": True
    }