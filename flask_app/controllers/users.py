from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, which is made by invoking the function Bcrypt with our app as an argument
from flask_app.models.user import User
from flask_app.models.boardgame import Game
from flask_app.models.comment import Comment 
from flask_app.models.mechanic import Mechanic

@app.route('/')         
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    print(request.form["email"])
    # see if the username provided exists in the database
    data = { 
        "email" : request.form["email"] 
    }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    print(session['user_id'])
    return redirect('/dashboard')

@app.route('/create', methods=['POST'])
def create():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "location": request.form['location'],
        "birthday": request.form['birthday'],
        "password": pw_hash
    }
    if not User.validate(request.form):
        return redirect('/')
    User.save(data)
    flash("Profile created, please login to start connecting!")
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    print(session['user_id'])
    data = {
        "id": session['user_id']
    }
    id=session['user_id']
    user = User.get_info_from_id(data)
    mechanics = Mechanic.get_fav_mechanics(data)
    games = Game.get_fav_games(data)
    ant_games = Game.get_anticipated_games(data)
    friends = User.get_friend_info(data)
    comments = Comment.get_comments(data)
    return render_template("dashboard.html", user=user, comments=comments, id=id, mechanics=mechanics, games=games, ant_games=ant_games, friends=friends)

@app.route('/edit_user')
def edit_user():
    print(session['user_id'])
    data = {
        "id": session['user_id']
    }
    id=session['user_id']
    user = User.get_info_from_id(data)
    return render_template("edit.html", user=user)

@app.route('/edit', methods=["POST"])
def edit():
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "location": request.form['location'],
        "birthday": request.form['birthday'],
        "about": request.form['about'],
        "id": session['user_id']
    }
    if not User.validate_edit(request.form):
        return redirect('/edit_user')
    User.update_user(data)
    return redirect('/dashboard')

@app.route('/mechanics')
def mechanics():
    mechanics = Mechanic.get_all()
    return render_template("mechanics.html", mechanics=mechanics)

@app.route('/add_mechanic', methods=["POST"])
def add_mechanic():
    data = {
        "mechanic_id": request.form['mechanic_id'],
        "user_id": session['user_id']
    }
    Mechanic.add_fav_mechanic(data)
    flash("Added!")
    return redirect('/mechanics')

@app.route('/games')
def add_games():
    return render_template("games.html")

@app.route('/add_game', methods=["POST"])
def add_game():
    data = {
        "name": request.form['name'],
        "year": request.form['year'],
        "bgg_id": request.form['bgg_id']
    }
    Game.save(data)
    boardgame_id = Game.get_id_from_name(data)
    data = {
        "boardgame_id": boardgame_id['id'],
        "user_id": session['user_id']
    }
    Game.add_fav_game(data)
    flash("Added!")
    return redirect('/games')

@app.route('/anticipated_games')
def add_anticipated_games():
    return render_template("a_games.html")

@app.route('/add_anticipated_game', methods=["POST"])
def add_ant_game():
    data = {
        "name": request.form['name'],
        "year": request.form['year'],
        "bgg_id": request.form['bgg_id']
    }
    Game.save(data)
    boardgame_id = Game.get_id_from_name(data)
    data = {
        "boardgame_id": boardgame_id['id'],
        "user_id": session['user_id']
    }
    Game.add_anticipated_game(data)
    flash("Added!")
    return redirect('/anticipated_games')

@app.route('/logout')
def logout():
    session.clear()
    print("session cleared")
    return redirect('/')

@app.route('/map')
def map_view():
    return "Placeholder"

@app.route('/add_friend')
def add_friend():
    users = User.get_all()
    session_id = session['user_id']
    data = { "id": session['user_id']}
    friends = User.get_friend_info(data)
    dict={}
    dict[session['user_id']] = 1
    for i in range (len(friends)):
        dict[friends[i]['friend_id']] = 1 
    return render_template("friend.html", users=users, session_id=session_id, dict=dict, friends=friends)

@app.route('/add_a_friend', methods=["POST"])
def add_a_friend():
    data = {
        "friend_id": request.form['friend_id'],
        "user_id": session['user_id']
    }
    User.add_friend(data)
    flash("Added")
    return redirect('/add_friend')

@app.route('/profile/<id>')
def view_profile(id):
    data = { "id": id }
    user = User.get_info_from_id(data)
    mechanics = Mechanic.get_fav_mechanics(data)
    games = Game.get_fav_games(data)
    ant_games = Game.get_anticipated_games(data)
    friends = User.get_friend_info(data)
    comments = Comment.get_comments(data)
    return render_template("profile.html", user=user, comments=comments, id=id, mechanics=mechanics, games=games, ant_games=ant_games, friends=friends)

@app.route('/add_comment', methods=["POST"])
def add_comment():
    user_id = session['user_id']
    recipient_id = request.form['recipient_id']
    data={
        "user_id": user_id,
        "content": request.form['content'],
        "recipient_id": recipient_id
    }
    Comment.save(data)
    if user_id == recipient_id:
        return redirect('/dashboard')
    else:
        return redirect('/profile/'+recipient_id)

