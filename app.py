import os, random
from flask_bcrypt import Bcrypt
from flask import Flask, session, abort, redirect, render_template, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from pymysql import NULL
from src.repositories.pet_repository import pet_repository_singleton, User, Pet

app = Flask(__name__)


db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CLEARDB_DATABASE_URL', 'sqlite:///test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'abc123')

bcrypt = Bcrypt(app)
db.init_app(app)


@app.route("/")
def index():
    # ToDo:  Find a better way check for user being logged in
    return render_template('index.html', home_link=True)


@app.route('/browse')
def browse():
    pet_type = request.args.get('pettype')
    if(pet_type == 'All'):
        all_pets = pet_repository_singleton.get_all_pets()
    else:
        all_pets = pet_repository_singleton.get_pets_by_type(pet_type)

    return render_template('browse.html', browse_link=True, data=all_pets, query=pet_type)

@app.route('/my_listings')
def listings():
    
    my_pets = pet_repository_singleton.get_my_listings(session['user'].get('user_id'))
    
    return render_template('my_listings.html', acct_link=True, data=my_pets)


@app.post('/account')
def account():
    
    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')
    user_age = request.form.get('user_age', 1)
    user_gender = request.form.get('user_gender', '')
    user_email_address = request.form.get('user_email_address', '')

    result = pet_repository_singleton.update_user(
    session['user'].get('user_id'), first_name, last_name, user_age, user_gender, user_email_address)

    created_user = pet_repository_singleton.get_user(session['user'].get('user_id'))

    return render_template('account.html', acct_link=True, data=created_user)

@app.route('/edit_account')
def view_account():
    user_id = session['user'].get('user_id')
    single_user = pet_repository_singleton.get_user(user_id)
    return render_template('account.html', acct_link=True, data=single_user)


# @app.route('/petfinder')
# def petfinder():
#    return render_template('petfinder.html', adopt_link=True)

@app.route('/faq')
def faq():
    return render_template('faq.html', faq_link=True)

@app.route('/aboutus')
def about():
    return render_template('aboutus.html', about_link=True)


@app.get('/petpost')
def petpost():
    return render_template('petpost.html', post_link=True)

@app.post('/postpet')
def savepet():
    pet_name = request.form.get('pet_name', '')
    pet_type = request.form.get('pet_type', '')
    pet_gender = request.form.get('pet_gender', '')
    pet_age = request.form.get('pet_age')
    pet_breed = request.form.get('pet_breed', '')
    pet_health = request.form.get('pet_health', '')
    pet_training = request.form.get('pet_training', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    pet_about = request.form.get('pet_about', '')
    pet_owner = session['user'].get('user_id')
    # Get thie image from the form

    image = request.files['photo']

    if image:
        # save the image to the satic folder
        rnd_num = str(random.randrange(0,100,3))
        new_filename = str(session['user'].get('user_id')) + '_' + rnd_num + '_' + image.filename
        image.save(os.path.join('./static', new_filename))
        # write the image file to the database
        photo = new_filename
    else:
        photo = ''

    created_pet = pet_repository_singleton.create_pet(
        pet_name, pet_age, pet_gender, pet_type, pet_breed, pet_health, pet_training, city, state, pet_about, pet_owner, photo)
    
    my_pets = pet_repository_singleton.get_my_listings(session['user'].get('user_id'))
    
    return render_template('my_listings.html', post_link=True, data=my_pets)


@app.post('/postcomment')
def postcomment():
    comment_content = request.form.get('comment_content', '')
    pet_id = session.get('pet_id')
    owner = session['user'].get('user_id')

    comment = pet_repository_singleton.create_comment(owner,comment_content,pet_id)

    single_pet = pet_repository_singleton.get_pet(pet_id)
    comments = pet_repository_singleton.get_comments(pet_id)

    return render_template('petview.html',post_link=True, data=single_pet,comments=comments)


@app.post('/editpet')
def editpet():
    pet_name = request.form.get('pet_name', '')
    pet_type = request.form.get('pet_type', '')
    pet_gender = request.form.get('pet_gender', '')
    pet_age = int(request.form.get('pet_age',''))
    pet_breed = request.form.get('pet_breed', '')
    pet_health = request.form.get('pet_health', '')
    pet_training = request.form.get('pet_training', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    pet_about = request.form.get('pet_about', '')

    pet_id = session.get('pet_id')

    pet_repository_singleton.update_pet(pet_id, pet_name, pet_age, pet_gender, pet_type, pet_breed, pet_health, pet_training, city, state, pet_about)

    single_pet = pet_repository_singleton.get_pet(pet_id)
    comments = pet_repository_singleton.get_comments(pet_id)

    return render_template('petview.html',browse_link=True, data=single_pet,comments=comments)


@app.post('/remove')
def deletepet():
    pet_id = session.get('pet_id')
    pet_repository_singleton.delete_pet(pet_id)
    return render_template('index.html',home_link=True)



@app.route('/petview/<int:pet_id>')
def petview(pet_id):
    session['pet_id'] = pet_id
    single_pet = pet_repository_singleton.get_pet(pet_id)
    comments = pet_repository_singleton.get_comments(pet_id)
    return render_template('petview.html', browse_link=True, data=single_pet,comments=comments)


@app.route('/login')
def login():
    return render_template('login.html')


@app.post('/login')
def loginuser():
    username = request.form.get('user_username', '')
    password = request.form.get('user_password', '')

    if username == '' or password == '':
        abort(400)

    existing_user = User.query.filter_by(user_username=username).first()

    if not existing_user or existing_user.user_id == 0:
        return redirect('/login')

    if not bcrypt.check_password_hash(existing_user.user_password, password):
        return redirect('/login')

    session['user'] = {
        'username': username,
        'user_id': existing_user.user_id,
        'user_email': existing_user.user_email_address,
        'first_name': existing_user.first_name
    }
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.post('/reguser')
def reguser():

    user_username = request.form.get('user_username', '')
    user_password = request.form.get('user_password', '')
    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')
    user_age = request.form.get('user_age', 0, type=int)
    user_gender = request.form.get('user_gender', '')
    user_email_address = request.form.get('user_email_address', '')

    # ToDo: Need to add better validation and handle exceptions.
    if user_username == '' or user_password == '':
        abort(400)

    hashed_password = bcrypt.generate_password_hash(
        user_password).decode('utf-8')

    created_user = pet_repository_singleton.create_user(
        user_username, hashed_password, first_name, last_name, user_age, user_gender, user_email_address)
    return redirect('/login')

@app.route("/external-sources")
def external_sources():
    # ToDo:  Find a better way check for user being logged in
    return render_template('external-sources.html', ext_link=True)

@app.post("/editcomment")
def edit_comment():
    comment_id = request.form.get('comment_id')
    comment_content = request.form.get('comment_content')
    pet_repository_singleton.update_comment(comment_content, comment_id)
    return redirect('/petview/' + str(session.get('pet_id')))

@app.route("/deletecomment")
def delete_comment():
    cid = request.args.get('cid')
    uid = session['user'].get('user_id')
    pet_repository_singleton.delete_comment(cid, uid)
    return redirect('/petview/' + str(session.get('pet_id')))

@app.route("/deactivate")
def deactivate():
    #delete all pets
    results = pet_repository_singleton.get_my_listings(session['user'].get('user_id'))
    for pet in results:
        pet_repository_singleton.delete_pet(pet.pet_id)

    #delete user
    pet_repository_singleton.delete_user(session['user'].get('user_id'))
    session.clear()
    return render_template('index.html', home_link=True)
