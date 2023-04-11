from flask import Flask # import flask to run create an app
app = Flask(__name__) # create instance of Flask called app
app.secret_key = "I want to learn how to make strong secret keys."