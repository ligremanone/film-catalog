from pydantic import BaseModel


class FilmBase(BaseModel):
    id: int
    name: str
    description: str
    year: int
    rating: float


class Film(FilmBase):
    pass
