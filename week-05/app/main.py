import uuid
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional

photos_db = []

@strawberry.type
class Photo:
    id: strawberry.ID
    name: str
    url: str

def get_photos() -> List[Photo]:
    return photos_db

def get_photo(id: strawberry.ID) -> Optional[Photo]:
    for photo in photos_db:
        if photo.id == id:
            return photo
    return None

def create_photo(name: str, url: str) -> Photo:
    new_photo = Photo(
        id=strawberry.ID(str(uuid.uuid4())),
        name=name,
        url=url
    )
    photos_db.append(new_photo)
    return new_photo

@strawberry.type
class Query:
    photos: List[Photo] = strawberry.field(resolver=get_photos)
    photo: Optional[Photo] = strawberry.field(resolver=get_photo)

@strawberry.type
class Mutation:
    create_photo: Photo = strawberry.field(resolver=create_photo)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)