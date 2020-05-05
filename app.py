from flask import Flask, request,  jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from flask_cors import CORS 
from flask_heroku import Heroku 
from environs import Env 
import os 

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),unique=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    def __init__(self, title, content, image_url):
        self.title = title
        self.content = content
        self.image_url = image_url

class BlogSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content', 'image_url')       


blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class AdminSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password')   

admin_schema = AdminSchema()
admin_schemas = AdminSchema(many=True)




if __name__ == '__main__':
    app.run(debug=True)