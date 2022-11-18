from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, comment, boardgame
  
class Mechanic:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM mechanics ORDER BY name ASC;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('meeple').query_db(query)
        # Create an empty list to append our instances of users
        mechanics = []
        # Iterate over the db results and create instances of users with cls.
        for one_mechanic in results:
            mechanics.append( cls(one_mechanic) )
        return mechanics

    @classmethod
    def get_fav_mechanics(cls, data):
        query = "SELECT name FROM mechanics JOIN mechanic_favorites ON mechanic_favorites.mechanic_id = mechanics.id JOIN users ON users.id = mechanic_favorites.user_id WHERE user_id = %(id)s ORDER BY mechanics.name ASC;"
        results = connectToMySQL('meeple').query_db(query, data)
        print(results)
        return results

    @classmethod
    def add_fav_mechanic(cls, data):
        query = "INSERT INTO mechanic_favorites ( user_id, mechanic_id ) SELECT %(user_id)s, %(mechanic_id)s WHERE NOT EXISTS (SELECT user_id, mechanic_id FROM mechanic_favorites WHERE user_id = %(user_id)s AND mechanic_id = %(mechanic_id)s);"
        return connectToMySQL('meeple').query_db(query, data)
