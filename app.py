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

    def __init__(self, username, password):
        self.username = username
        self.password = password 

class AdminSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password')   

admin_schema = AdminSchema()
admin_schemas = AdminSchema(many=True)


@app.route ("/", methods=["GET"])
def home():
    return "<h1> Blog API </h1>"

# GET 
@app.route("/blogs", methods=["GET"])
def get_blogs():
    all_blogs = Blog.query.all()
    result = blogs_schema.dump(all_blogs)
    return jsonify(result)

@app.route("/admins", methods=["GET"])
def get_admins():
    all_admins = Admin.query.all()
    result = admin_schemas.dump(all_admins)
    return jsonify(result)

# POST 
@app.route("/add-blog", methods=["POST"])
def add_blog():
    title = request.json["title"]
    content = request.json["content"]
    image_url = request.json["image_url"]

    new_blog = Blog(title, content, image_url)

    db.session.add(new_blog)
    db.session.commit()

    blog = Blog.query.get(new_blog.id)
    return blog_schema.jsonify(blog)

@app.route("/add-admin", methods=["POST"])
def add_admin():
    username = request.json["username"]
    password = request.json["password"]
    

    new_admin = Admin(username, password)

    db.session.add(new_admin)
    db.session.commit()

    admin = Admin.query.get(new_admin.id)
    return admin_schema.jsonify(admin)
 
if __name__ == '__main__':
    app.run(debug=True)