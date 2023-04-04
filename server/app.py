#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#this could be a formatting thing in json.  yes, a config that has json responses print on seperate lines
#with indentation
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():

    #retrieve all games sorted by title.  uses SQL Alchemy's ORM to retrieve all Game objs from db, sorted by their title attribute
    # Game is a model that reps a table in the db
    # Game.query  creates a query obj that allows us to interact with the Game table
    # order_by(Game.title) is a method that sorts the query results by the title column in ascending order
    # .all() executes the query and retrieves all Game objs that match the query criteria 

    # games_by_title = Game.query.order_by(Game.title).all()

    #this limits the returned result to be 10
    first_10_games = Game.query.limit(10).all()
    games =[]
    #query results have to be reformatted as dictionaries for jsonify to work its magic.  __dict__ attribute cannot be used here bc
    #SQL Alchemy records have attributes that are nonstandard python objs
    for game in first_10_games:
        game_dict ={
            "title":game.title, 
            "genre":game.genre, 
            "platform":game.platform, 
            "price":game.price,
        }
        games.append(game_dict)


    response = make_response(
        #jsonify is a method in Flask that serializes its arguments as JSON and returns a Response object.  it can accept
        #lists or dictionaries as arguments.  unfortunately it will not accept models as args
        jsonify(games), 200, {"Content-Type": "application/json"}
    )

    return response

#getting one game by using params 
@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    #this replaces the actual defining of the game dictionary 
    game_dict = game.to_dict()

    #this is only necessary when we aren't using serialization to stringify json documents 
    # game_dict = {
    #     "title": game.title,
    #     "genre": game.genre,
    #     "platform": game.platform,
    #     "price": game.price,
    # }

    response = make_response(
        game_dict, 200
    )
    response.headers["Content-Type"] = "application/json"

    return response 

if __name__ == '__main__':
    app.run(port=5555, debug=True)