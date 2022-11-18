from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, boardgame, mechanic
 
class Comment:
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.recipient_id = data['recipient_id']

    @classmethod
    def delete( cls, data ):
        query = "DELETE FROM comments where ID = %(id)s;"
        return connectToMySQL('meeple').query_db(query, data)

    @classmethod
    def save( cls, data ):
        query = "INSERT INTO comments ( content, user_id, recipient_id, created_at, updated_at ) VALUES (%(content)s, %(user_id)s, %(recipient_id)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('meeple').query_db(query, data)

    @classmethod
    def get_comments( cls, data ):
        query = "SELECT * from comments WHERE recipient_id = %(id)s;"
        results = connectToMySQL('meeple').query_db(query, data)
        replies = []
        # Iterate over the db results and create instances of users with cls.
        for one_reply in results:
            replies.append( cls(one_reply) )
        return replies

class Reply:
    def __init__( self, data ):
        self.id = data ['id']
        self.comment_id = data['comment_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def delete( cls, data ):
        query = "DELETE FROM replies where ID = %(id)s;"
        return connectToMySQL('meeple').query_db(query, data)

    @classmethod
    def save( cls, data ):
        query = "INSERT INTO replies ( content, user_id, comment_id, created_at, edited_at ) VALUES %(content)s, %(user_id)s, %(comment_id)s, NOW(), NOW();"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('meeple').query_db(query, data)

    @classmethod
    def get_replies( cls, data ):
        query = "SELECT * from comments WHERE recipient_id = %(id)s;"
        results = connectToMySQL('meeple').query_db(query, data)
        replies = []
        # Iterate over the db results and create instances of users with cls.
        for one_reply in results:
            replies.append( cls(one_reply) )
        return replies

    