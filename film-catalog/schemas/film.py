from typing import Annotated
from datetime import datetime
from annotated_types import Len, Interval
from pydantic import BaseModel


class FilmBase(BaseModel):
    name: str
    description: str
    year: int


class Film(FilmBase):
    id: int
    rating: float


class FilmCreate(FilmBase):
    name: Annotated[
        str,
        Len(min_length=1, max_length=100),
    ]
    year: Annotated[
        int,
        Interval(ge=1895, le=datetime.now().year + 5),
    ]
