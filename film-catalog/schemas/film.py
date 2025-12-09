from datetime import UTC, datetime
from typing import Annotated

from annotated_types import Interval, Len, MaxLen
from pydantic import AnyHttpUrl, BaseModel

DESCRIPTION_MAX_LENGTH = 200
NameString = Annotated[
    str,
    Len(min_length=1, max_length=100),
]
YearNumber = Annotated[
    int,
    Interval(ge=1895, le=datetime.now(tz=UTC).year + 5),
]
DescriptionString = Annotated[
    str,
    MaxLen(DESCRIPTION_MAX_LENGTH),
]


class FilmBase(BaseModel):
    name: str
    description: str
    year: int
    url: AnyHttpUrl


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
    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]
    name: NameString
    year: YearNumber
    description: DescriptionString = "Foo"


class FilmUpdate(FilmBase):
    name: NameString
    year: YearNumber
    description: DescriptionString = ""


class FilmUpdatePartial(BaseModel):
    name: NameString | None = None
    year: YearNumber | None = None
    description: DescriptionString | None = None
