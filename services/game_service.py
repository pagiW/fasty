from models.models import Games
from data_base.data_base import sesion
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

class GameService:
    def __init__(self) -> None:
        self.db = sesion()

    def get(self):
        result = self.db.query(Games).all()
        return jsonable_encoder(result)
    def create(self, data: dict):
        data_games = jsonable_encoder(self.db.query(Games).all())
        names = map(lambda obj: obj['name'], data_games)
        if data['name'] in names:
            return JSONResponse(content={'message': 'Game already used'}, status_code=400)
        new_data = Games(**data)
        self.db.add(new_data)
        self.db.commit()
        return JSONResponse(content=data, status_code=201)

    def update(self, id: int, game: dict):
        my_game = self.db.query(Games).filter(Games.id == id).first()

        if not my_game:
            return JSONResponse(content={'message': 'Game Not Found'}, status_code=404)
        if game['name']:
            my_game.name = game['name']
        if game['console']:
            my_game.console = game['console']
        if game['realized']:
            my_game.realized = game['realized']
        self.db.commit()
        show_game = self.db.query(Games).filter(Games.id == id).first()
        return JSONResponse(content=jsonable_encoder(show_game), status_code=200)

    def delete(self, id: int):
        my_game = self.db.query(Games).filter(Games.id == id).first()
        if not my_game:
            return JSONResponse(content={'message': 'Game Not Found'}, status_code=404)

        self.db.delete(my_game)
        self.db.commit()
        return JSONResponse(content={'message': 'Game Deleted'}, status_code=200)