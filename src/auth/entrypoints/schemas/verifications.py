from pydantic import BaseModel, EmailStr


class RegistrationRequest(BaseModel):
    email: EmailStr
