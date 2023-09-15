from pydantic import BaseModel


class BaseShema(BaseModel):
    result: bool = True

    class Config:
        orm_mode = True
