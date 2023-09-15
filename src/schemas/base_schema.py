from pydantic import BaseModel, ConfigDict


class BaseShema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: bool = True
