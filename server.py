from flask_app import app # import app to run instance
# import controllers
from flask_app.controllers import users, posts, comments

if __name__ == '__main__':
    app.run(debug = True, port = 5001)