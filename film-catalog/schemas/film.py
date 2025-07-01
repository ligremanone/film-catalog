from typing import Annotated
from datetime import datetime
from annotated_types import Len, Interval, MaxLen
from pydantic import BaseModel

NameString = Annotated[
    str,
    Len(min_length=1, max_length=100),
]
YearNumber = Annotated[
    int,
    Interval(ge=1895, le=datetime.now().year + 5),
]
DescriptionString = Annotated[
    str,
    MaxLen(256),
]


class FilmBase(BaseModel):
    name: str
    description: str
    year: int


class Film(FilmBase):
    slug: str
    rating: float
    notes: Annotated[
        str,
        MaxLen(256),
    ] = ""


class FilmRead(FilmBase):
    slug: str
    rating: float


class FilmCreate(FilmBase):
    slug: str
    name: NameString
    year: YearNumber
    description: DescriptionString


class FilmUpdate(FilmBase):
    name: NameString
    year: YearNumber
    description: DescriptionString


class FilmUpdatePartial(BaseModel):
    name: NameString | None = None
    year: YearNumber | None = None
    description: DescriptionString | None = None
