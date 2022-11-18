from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, comment, mechanic

# create a regular expression object that we'll use later   
class Game:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.year = data['year']
        self.bgg_id = data['bgg_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def delete( cls, data ):
        query = "DELETE FROM boardgames where ID = %(id)s;"
        return connectToMySQL('meeple').query_db(query, data)

    # class method to save our user to the database
    @classmethod
    def save( cls, data ):
        query = "INSERT INTO boardgames ( name, year, bgg_id ) SELECT %(name)s, %(year)s, %(bgg_id)s WHERE NOT EXISTS (SELECT name, year, bgg_id FROM boardgames WHERE name=%(name)s AND year=%(year)s AND bgg_id=%(bgg_id)s);"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('meeple').query_db(query, data)

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM boardgames;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('meeple').query_db(query)
        # Create an empty list to append our instances of users
        games = []
        # Iterate over the db results and create instances of users with cls.
        for one_game in results:
            games.append( cls(one_game) )
        return games

    @classmethod
    def get_info_from_id(cls, data):
        query = "SELECT * FROM boardgames WHERE id = %(id)s;"
        results = connectToMySQL('meeple').query_db(query, data)
        game = cls(results[0])
        return game
    
    @classmethod
    def get_id_from_name(cls, data):
        query = "SELECT id FROM boardgames WHERE name = %(name)s;"
        results = connectToMySQL('meeple').query_db(query, data)
        return results[0]

    @classmethod
    def edit_game(cls, data):
        query = "UPDATE boardgames SET name = %(name)s, year = %(year)s, bgg_id = %(bgg_id)s, WHERE id = %(id)s;"
        return connectToMySQL('meeple').query_db(query, data)

    @classmethod
    def get_fav_games(cls, data):
        query = "SELECT name FROM boardgames JOIN game_favorites ON game_favorites.boardgame_id = boardgames.id JOIN users ON users.id = game_favorites.user_id WHERE user_id = %(id)s ORDER BY boardgames.name ASC;"
        results = connectToMySQL('meeple').query_db(query, data)
        print(results)
        return results

    @classmethod
    def add_fav_game(cls, data):
        query = "INSERT INTO game_favorites ( user_id, boardgame_id ) SELECT %(user_id)s, %(boardgame_id)s WHERE NOT EXISTS (SELECT user_id, boardgame_id FROM game_favorites WHERE user_id = %(user_id)s AND boardgame_id = %(boardgame_id)s);"
        return connectToMySQL('meeple').query_db(query, data)

    @classmethod
    def get_anticipated_games(cls, data):
        query = "SELECT name FROM boardgames JOIN anticipated_games ON anticipated_games.boardgame_id = boardgames.id JOIN users ON users.id = anticipated_games.user_id WHERE user_id = %(id)s ORDER BY boardgames.name ASC;"
        results = connectToMySQL('meeple').query_db(query, data)
        print(results)
        return results

    @classmethod
    def add_anticipated_game(cls, data):
        query = "INSERT INTO anticipated_games ( user_id, boardgame_id ) SELECT %(user_id)s, %(boardgame_id)s WHERE NOT EXISTS (SELECT user_id, boardgame_id FROM anticipated_games WHERE user_id = %(user_id)s AND boardgame_id = %(boardgame_id)s);"
        return connectToMySQL('meeple').query_db(query, data)