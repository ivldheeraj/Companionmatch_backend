from dataclasses import dataclass, field
from typing import Optional

@dataclass
class AddressModel:
    street: str
    city: str
    state: str
    zipcode: str
    address_id: Optional[int] = field(default=None)

@dataclass
class UserRegisterModel:
    email: str
    password: str
    first_name: str
    last_name: str
    address: AddressModel
    student_bio: str
    user_id: Optional[int] = field(default=None)

@dataclass
class UserLoginModel:
    email: str
    password: str