from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Address
from .schemas import AddressCreate
from .utils import haversine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses/")
def create_address(data: AddressCreate, db: Session = Depends(get_db)):
    address = Address(**data.dict())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found.")
    db.delete(address)
    db.commit()
    return {"message": "Address deleted."}

@app.get("/addresses/nearby")
def nearby_addresses(lat: float, lon: float, distance: float, db: Session = Depends(get_db)):
    results = []
    addresses = db.query(Address).all()

    for addr in addresses:
        dist = haversine(lat, lon, addr.latitude, addr.longitude)
        if dist <= distance:
            results.append(addr)

    return results
