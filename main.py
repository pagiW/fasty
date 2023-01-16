from fastapi import FastAPI, Path, Query, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from schemas import Game, ChangedGame, User
from utils.jwt_manage import create_token, validate_token
from fastapi.security import HTTPBearer
from data_base.data_base import engine, Base, sesion
from models.models import Games
from fastapi.encoders import jsonable_encoder
from middleware.errorHandler import ErrorHandler
from routes.games_router import games_router
import uvicorn
import decouple
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = 'Florez app'
app.version = '1.0.0'

origin = [
    decouple.config('URL1')
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandler)
app.include_router(games_router)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def run():
    return HTMLResponse('<h1>Florez app</h1>\n<h2>Aplicación pequeña</h2>')

@app.post('/login', tags=['auth'], status_code=201)
def login(user: User):
    if user.email == 'Juan@gmail.com' and user.password == 'A xd':
        return create_token(dict(user))
    return JSONResponse(content=dict(user), status_code=201)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=decouple.config('PORT'))