from pydantic import BaseModel, field_validator, validator


class CreateAdvert(BaseModel):
    title: str
    description: str
    owner: str

    @field_validator("title", "description", "owner")
    @classmethod
    def check_json(cls, value):
        if value is None:
            raise ValueError(f"Не передан параметр {value}")
        return value
