from fastapi import APIRouter
from fastapi import FastAPI, Path, Query, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from schemas import Game, ChangedGame, User
from utils.jwt_manage import create_token, validate_token
from fastapi.security import HTTPBearer
from data_base.data_base import engine, Base, sesion
from models.models import Games
from fastapi.encoders import jsonable_encoder
from services.game_service import GameService

games_router = APIRouter()

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'Juan@gmail.com' or data['password'] != 'A xd':
            raise HTTPException(status_code=403, detail='Bad email >:(')

@games_router.get('/games', tags=['games'], status_code=200, dependencies=[Depends(JWTBearer())])
def get_games():
    data = GameService().get()
    return JSONResponse(content=data, status_code=200)

@games_router.get('/games/{id}', tags=['game by id'], status_code=200)
def get_game(id:int = Path(ge=1)):
    db = sesion()
    the_game = db.query(Games).filter(Games.id == id).first()
    if the_game:
        return JSONResponse(content=jsonable_encoder(the_game), status_code=200)
    else:
        return JSONResponse(content={'message': 'Game not found'}, status_code=404)

@games_router.get('/games/', tags=['movie by query'], status_code=200)
def get_game_by_name(name:str = Query(default=''), year:int = Query(le=2023, default=''), console:str = Query(default='')):
    db = sesion()
    filtered_games = jsonable_encoder(db.query(Games).all())
    if name:
        filtered_games = tuple(filter(lambda obj: name in obj['name'], filtered_games))
    if year:
        filtered_games = tuple(filter(lambda obj: obj['realized'] == year, filtered_games))
    if console:
        filtered_games = tuple(filter(lambda obj: obj['console'] == console, filtered_games))
    if len(filtered_games) > 0:
        return JSONResponse(content=filtered_games, status_code=200)
    else:
        return JSONResponse(content={'message': 'Game not found'}, status_code=404)

@games_router.post('/games', tags=['game creator'], status_code=201)
def create_game(game:Game):
    game = dict(game)
    data = GameService().create(game)
    return data

@games_router.put('/games/{id}', tags=['modificate game'], status_code=200)
def mofidicate_game(id:int, game:ChangedGame):
    result = GameService().update(id, dict(game))
    return result

@games_router.delete('/games/{id}', tags=['delete game'], status_code=200)
def delete_game(id:int):
    result = GameService().delete(id)
    return result
