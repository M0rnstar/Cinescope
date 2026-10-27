import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
)


class MovieLocation(str, Enum):
    MSK = "MSK"
    SPB = "SPB"


class GenreResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: StrictStr = Field(min_length=1)


class MovieResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: StrictInt = Field(gt=0)
    name: StrictStr = Field(min_length=1)
    price: StrictInt = Field(gt=0)
    description: StrictStr = Field(min_length=1)
    imageUrl: StrictStr | None
    location: MovieLocation
    published: StrictBool
    genreId: StrictInt = Field(gt=0)
    genre: GenreResponse
    createdAt: datetime.datetime
    rating: StrictInt | StrictFloat = Field(ge=0)


class ReviewUserResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fullName: StrictStr = Field(min_length=1)


class MovieReviewResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    userId: StrictStr = Field(min_length=1)
    rating: StrictInt | StrictFloat = Field(ge=0, le=5)
    text: StrictStr
    hidden: StrictBool
    createdAt: datetime.datetime
    user: ReviewUserResponse


class MovieDetailsResponse(MovieResponse):
    reviews: list[MovieReviewResponse]


class MoviesResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    movies: list[MovieResponse]
    count: StrictInt = Field(ge=0)
    page: StrictInt = Field(gt=0)
    pageSize: StrictInt = Field(gt=0)
    pageCount: StrictInt = Field(ge=0)
