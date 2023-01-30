from fastapi import FastAPI
from routers import auth, users, clients, backlinks
from dependencies.dependencies import *


app = FastAPI()

origins =['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, tags=['Auth'])
app.include_router(clients.router, tags=['Clients'])
app.include_router(users.router, tags=['Users'])
app.include_router(backlinks.router, tags=['Backlinks'])

