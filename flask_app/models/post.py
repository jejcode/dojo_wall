from flask_app.config.mysqlconnection import connectToMySQL # module to connect to DB
from flask_app.models import user, comment
from flask import flash

class Post:
    DB = 'coding_dojo_wall_schema'
    def __init__(self, data) -> None:
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None
        self.comments = []

    def search_for_comment(self, data):
        for comment in self.comments:
            if comment.id == data['id']:
                return True
        return False

        
    
    # class methods to manage instances and all_posts
    @classmethod
    def search_for_post(cls, data):
        for item in cls.all_posts: # search all_posts for this instance
            if item.id == data['id']: # if it exists, return it's index
                return item.index
        return -1 # otherwise return -1
    # CRUD
    # CREATE
    @classmethod
    def save_post(cls, data): # save post to new db row
        query = """INSERT INTO posts (content, user_id)
                VALUES (%(post)s, %(user_id)s)"""
        return connectToMySQL(cls.DB).query_db(query, data) # row id of new record will be returned
    # READ
    @classmethod
    def get_all_post_data(cls, data):
        query = """SELECT * FROM posts
                LEFT JOIN comments ON posts.id = comments.post_id
                LEFT JOIN users ON posts.user_id = users.id
                LEFT JOIN users AS commenters ON commenter_id = commenters.id
                ORDER BY posts.id DESC, comments.id;"""
        results = connectToMySQL(cls.DB).query_db(query)
        users_hash = {}
        all_posts = []
        for db_row in results:
            # create instance of post if it doesn't already exist
            if len(all_posts) <= 0 or all_posts[-1].id != db_row['id']:
                current_row_post = {
                    'id': db_row['id'],
                    'content': db_row['content'],
                    'created_at': db_row['created_at'],
                    'updated_at': db_row['updated_at']
                }
                this_post = cls(current_row_post)
                all_posts.append(this_post)
            else:
                this_post = all_posts[len(all_posts) - 1] # if post already exists, this_post is the same as the last on in the list

            # create instance of post author (if not already in existence)
            if db_row['users.id'] not in users_hash:
                current_row_user = {
                    'id': db_row['users.id'],
                    'first_name': db_row['first_name'],
                    'last_name': db_row['last_name'],
                    'email': db_row['email'],
                    'password': db_row['password'],
                    'created_at': db_row['users.created_at'],
                    'updated_at': db_row['users.updated_at']
                }
                current_user = user.User(current_row_user)
                users_hash[db_row['users.id']] = current_user
            # link post and user
            this_user = users_hash[db_row['users.id']]
            this_user.posts.append(this_post)
            this_post.owner = this_user
            # create instance of comment (if it exists)
            if db_row['comments.id']:
                current_row_comment = {
                    'id': db_row['comments.id'],
                    'comment': db_row['comment'],
                    'created_at': db_row['comments.created_at'],
                    'updated_at': db_row['comments.updated_at'],
                }
                this_comment = comment.Comment(current_row_comment)
                # link comment and post
                this_comment.post = this_post
                this_post.comments.append(this_comment)
                # add commenter to hash (if they don't exist
                if db_row['commenters.id'] not in users_hash:
                    current_row_commenter = {
                        'id': db_row['commenters.id'],
                        'first_name': db_row['commenters.first_name'],
                        'last_name': db_row['commenters.last_name'],
                        'email': db_row['commenters.email'],
                        'password': db_row['commenters.password'],
                        'created_at': db_row['commenters.created_at'],
                        'updated_at': db_row['commenters.updated_at']
                    }
                    # create instance of comment owner (if not already created)
                    users_hash[db_row['commenters.id']] = user.User(current_row_commenter)
                # link comment and comment owner
                this_comment.commenter = users_hash[db_row['commenters.id']]
                users_hash[db_row['commenters.id']].comments.append(this_comment)
        # return all_posts
        return {
            'user': users_hash[data] if data in users_hash else False,
            'posts': all_posts
        }
    # DELETE
    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts where id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_post(data): # posts must not be blank
        is_valid = True
        if len(data['post']) <= 0:
            flash('* Post must not be blank', 'posts')
            is_valid = False
        return is_valid