from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class New_User(BaseModel):
    name: str
    email: str
    hash: str
    cep: str
    address: str
    gender: str
    tel: str
    birth: date

class Waiting_User(BaseModel):
    id: int
    name: str
    email: str
    hash: str
    cep: str
    address: str
    gender: str
    tel: str
    birth: date
    added: Optional[date]

    class Config:
        orm_mode = True

class Add_User(BaseModel):
    user_to_del: Optional[int]
    name: str
    email: str
    hash: str
    is_admin: bool = False
    is_designer: bool = False

class Add_User_Data(BaseModel):
    cep: str
    address: str
    gender: str
    tel: str
    birth: date
    added: Optional[date]

class Get_User(BaseModel):
    id: int
    email: str

class User_List(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class User_Data(BaseModel):
    id: int
    name: str
    email: str
    hash: str
    is_admin: bool
    is_designer: bool

    class Config:
        orm_mode = True

class Delete_User(BaseModel):
    id: int

class User_Upgrade(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    hash: Optional[str]
    is_admin: Optional[bool]
    is_designer: Optional[bool]
    cep: Optional[str]
    address: Optional[str]
    gender: Optional[str]
    tel: Optional[str]
    birth: Optional[date]
    added: Optional[date]

class Standard_Output(BaseModel):
    confirm: bool

class Tithe_Register(BaseModel):
    user_id: int
    value: float
    tithe_date: date
    treasurer_id: int

class Tithe_List(BaseModel):
    id: int
    user_id: int
    value: float
    tithe_date: date
    username: Optional[str]
    treasurer: Optional[str]

    class Config:
        orm_mode = True

class Tithe_List_Response(BaseModel):
    tithe_list: List[Tithe_List]

class Expense_Register(BaseModel):
    value: float
    description: str
    expense_date: date
    treasurer_id: int

class Expense_List(BaseModel):
    id: int
    value: float
    description: str
    expense_date: date
    treasurer_id: int

    class Config:
        orm_mode = True

class Offer_Include(BaseModel):
    value: float
    offer_date: date
    treasurer_id: int


class Offer_List(BaseModel):
    id: int
    value: float
    offer_date: date
    treasurer_id: int

    class Config:
        orm_mode = True

class Finance_Values(BaseModel):
    offers: List[float]
    tithes: List[float]
    expenses: List[float]
    previous_balance: List[float]

class Finance_Include(BaseModel):
    entry: float
    issues: float
    start: date
    end: date
    period_balance: float
    total_balance: float

class Finance_List(BaseModel):
    id: int
    entry: float
    issues: float
    start: date
    end: date
    period_balance: float
    total_balance: float

    class Config:
        orm_mode = True

class Finance_Data(BaseModel):
    entry: float
    issues: float
    start: date
    end: date
    period_balance: float
    total_balance: float