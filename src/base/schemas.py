from pydantic import BaseModel


class Message(BaseModel):

    msg: str


class File(BaseModel):

    filename: str
    type: str
    subtype: str
    content: bytes
