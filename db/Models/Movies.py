from pydantic import BaseModel


class Movies(BaseModel):
    id: int
    movie_title: str
    release_date: str
    video_release_date: str
    IMDb_URL: str
    generes: list
    