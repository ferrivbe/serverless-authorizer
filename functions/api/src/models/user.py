from pydantic import BaseModel


class UserAdd(BaseModel):
    """
    The user add data transfer object.
    """

    email: str
    username: str
    password: str


class UserCreated(BaseModel):
    """
    The user created data transfer object.
    """

    email: str
    username: str
    message: str


class UserConfirm(BaseModel):
    """
    The user confirm data transfer object.
    """

    email: str
    code: str
