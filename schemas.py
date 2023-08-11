from pydantic import BaseModel, EmailStr


class UserRegistration(BaseModel):
    first_name: str
    email: EmailStr
    password: str
    phone: str


class UserRegistrationWithPicture(UserRegistration):
    profile_picture: str
