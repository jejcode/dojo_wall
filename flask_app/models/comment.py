from flask_app.config.mysqlconnection import connectToMySQL # module to connect to DB
from flask_app.models import user
from flask import flash # needed for validation

class Comment:
    DB = 'coding_dojo_wall_schema'
    def __init__(self, data) -> None:
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.update_at = data['updated_at']
        self.post = None
        self.commenter = None
        pass
    
    # CRUD
    # CREATE
    @classmethod
    def save(cls, data):
        query = """INSERT INTO comments (comment, post_id, commenter_id)
                VALUES (%(comment)s, %(post_id)s, %(user_id)s)"""
        new_comment = connectToMySQL(cls.DB).query_db(query, data)
        return new_comment
    
    @staticmethod
    def validate_comment(data):
        is_valid = True
        if len(data['comment']) <= 0:
            flash('* Comment must contain at least 1 character', 'comments')
            is_valid = False
        return is_valid