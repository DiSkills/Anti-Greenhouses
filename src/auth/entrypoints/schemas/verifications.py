from pydantic import BaseModel, EmailStr


class RegistrationRequest(BaseModel):
    """ Registration request """

    email: EmailStr
