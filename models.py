from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, nullable=False,primary_key=True)
    user_username = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    user_gender = db.Column(db.String, nullable=False)
    user_email_address = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'User({self.user_id},{self.user_password}, {self.user_username}, {self.first_name}, {self.last_name},{self.user_age}, {self.user_gender}, {self.user_email_address})'

    def __init__(self, user_username , user_password, first_name, last_name, user_age,user_gender,user_email_address):
        self.user_username = user_username
        self.user_password = user_password
        self.first_name = first_name
        self.last_name = last_name
        self.user_age = user_age
        self.user_gender = user_gender
        self.user_email_address = user_email_address

class Pet(db.Model):

    __tablename__ = 'pet'

    pet_id = db.Column(db.Integer, nullable=False,primary_key=True)
    pet_name = db.Column(db.String, nullable=False)
    pet_age = db.Column(db.Integer, nullable=False)
    pet_gender = db.Column(db.String, nullable=False)
    pet_type = db.Column(db.String, nullable=False)
    pet_breed = db.Column(db.String, nullable=False)
    pet_health = db.Column(db.String, nullable=False)
    pet_training = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    pet_about = db.Column(db.String, nullable=False)
    pet_owner = db.Column(db.Integer,db.ForeignKey('user.user_id'), nullable=False)
    owner= db.relationship('User',backref='pets',lazy=True)
    photo = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'Pet({self.pet_id},{self.pet_name}, {self.pet_age}, {self.pet_gender}, {self.pet_type}, {self.pet_breed}, {self.pet_health}, {self.pet_training}, {self.city}, {self.state}, {self.pet_about}, {self.pet_owner}, {self.photo} )'

    def __init__(self,pet_name, pet_age, pet_gender, pet_type, pet_breed, pet_health , pet_training , city, state, pet_about, pet_owner, photo):
        self.pet_name = pet_name
        self.pet_age = pet_age
        self.pet_gender = pet_gender
        self.pet_type = pet_type
        self.pet_breed = pet_breed
        self.pet_health = pet_health
        self.pet_training = pet_training
        self.city = city
        self.state = state
        self.pet_about = pet_about
        self.pet_owner = pet_owner
        self.photo = photo


class Comment(db.Model):

    __tablename__ = 'comment'

    comment_id = db.Column(db.Integer, nullable=False,primary_key=True)
    comment_content = db.Column(db.String, nullable=False)
    author_id= db.Column(db.Integer,db.ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('pet.pet_id'), nullable=False)
    #post = db.relationship('Pet',backref='posts_comments',lazy=True)
    #author = db.relationship('User', backref='user_comment',lazy=True)

    def __repr__(self):
        return f'Comment({self.comment_id },{self.author_id},{self.comment_content} {self.post_id})'

    def __init__(self, comment_content, author_id, post_id):
        self.comment_content = comment_content
        self.author_id = author_id
        self.post_id = post_id
    
    