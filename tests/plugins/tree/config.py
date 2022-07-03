from pydantic import BaseModel


class Config(BaseModel):
    # Your Config Here

    class Config:
        extra = "ignore"
