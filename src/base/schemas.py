from pydantic import BaseModel


class Message(BaseModel):
    """ Message """

    msg: str


class File(BaseModel):
    """ File """

    filename: str
    type: str
    subtype: str
    content: bytes
