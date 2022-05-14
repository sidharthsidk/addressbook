from pydantic import BaseModel

class AddressBook(BaseModel):
    name : str
    address: str
    pin:int
    phone : int
    long : float
    lat:float


class ShowAddressBook(AddressBook):
    class Config():
        orm_mode =True
