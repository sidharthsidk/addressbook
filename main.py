from sqlite3 import dbapi2
from fastapi import Depends, FastAPI, Query,status,Response
from . import models, schemas
from .schemas import AddressBook,ShowAddressBook
from .database import SessionLocal, engine, Base
from sqlalchemy.orm import Session


from geopy.geocoders import Nominatim

 
models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/add-address',status_code=status.HTTP_201_CREATED)
def add_address(request:AddressBook,response: Response,db: Session = Depends(get_db)):
    try:
        data ={}
        new_address = models.AddressBook(name = request.name,address = request.address,pin = request.pin,
                        phone = request.phone,long = request.long,lat = request.lat)
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        data['status'] = "success"
        data['type'] = str(type(request.name))
        data['message'] = "A new address has been added succsessfully!"
        return data
    except Exception as e:
        data['status'] = "failed"
        data['message'] = "failed to add a new address"
        data['error'] = f"failed due to an error : {e}"
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        return data
        

@app.delete('/delete-address/{id}',status_code=status.HTTP_200_OK)
def deleteaddress(id,db: Session = Depends(get_db)):
    try:
        data ={}
        db.query(models.AddressBook).filter(models.AddressBook.id == id).delete(synchronize_session=False)
        db.commit()
        data['status'] = "success"
        data['message'] = "Successfully deleted an address"
        return data
    except Exception as e:
        data['status'] = "failed"
        data["message"] = "Failed to delete address"
        return data


@app.get("/",status_code=status.HTTP_200_OK)
def all_address(db : Session = Depends(get_db)):
    try:
        all_address = db.query(models.AddressBook).all()
        return all_address
    except Exception as e:
        return {"status" : "failed to load data from database"}

@app.get("/address-details/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowAddressBook)
def address_details(id,db : Session = Depends(get_db)):
    try:
        all_address = db.query(models.AddressBook).filter(models.AddressBook.id == id).first()
        return all_address
    except Exception as e:
        return {"status" : "failed to load data from database"}

@app.put("/update-address/{id}",status_code=status.HTTP_200_OK)
def update_address(id,request:AddressBook,db : Session = Depends(get_db)):
    try:
        data = db.query(models.AddressBook).filter(models.AddressBook.id == id).first()    
        data.name = request.name
        data.address = request.address
        data.pin = request.pin
        data.phone = request.phone
        data.long = request.long
        data.lat = request.lat
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return {"status" : "failed to update data!!"}

@app.get("/fetch-nearby/",status_code=status.HTTP_200_OK)
def address_finder(distance:int,long:int,lat:int,db : Session = Depends(get_db)):
    try:
        address_list = []
        for i in db.query(models.AddressBook).all():
            d = (lat -i.lat)*(lat -i.lat) + (long -i.long)*(long -i.long)
            if d < (distance*distance):
                address_list.append(i)
        return address_list
    except Exception as e:
        return {"status" : f"failed to load data from database{e}"}