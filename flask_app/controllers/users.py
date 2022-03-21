from flask import render_template, redirect, session, request, flash
from flask_app import app
# DON'T FORGET TO IMPORT REMAINDER OF MODELS!!!
from flask_app.models.user import User
from flask_app.models.thought import Thought
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/thoughts')
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.add(data)

    return redirect('/thoughts')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid login credentials","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid login credentials","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/thoughts')

# @app.route('/thoughts')
# def thoughts():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         'id': session['user_id']
#     }

#     user_data = {
#         'user_id':session['user_id']
#     }

#     user = User.get_by_id(data)
#     # one_thought = Thought.get_one(user_data)
#     # thoughts = Thought.get_thought_and_user()
#     get_all_likes = Thought.get_all_likes(data)
#     thoughts = Thought.show_all_thoughts()
    
#     return render_template("thoughts.html",user=user,thoughts=thoughts,get_all_likes=get_all_likes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')