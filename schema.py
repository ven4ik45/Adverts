from pydantic import BaseModel, field_validator, validator


class AdvertBase(BaseModel):
    title: str | None = None
    description: str | None = None
    owner: str | None = None

    @field_validator("title", "description", "owner")
    @classmethod
    def check_json(cls, value):
        if value is None:
            raise ValueError(f"Не передан параметр {value}")
        return value


class CreateAdvert(AdvertBase):
    title: str
    description: str
    owner: str


class UpdateAdvert(AdvertBase):
    title: str | None = None
    description: str | None = None
    owner: str | None = None
