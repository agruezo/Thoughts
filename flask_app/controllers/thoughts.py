from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.thought import Thought
from flask_app.models.user import User

@app.route('/thoughts')
def thoughts():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    user_data = {
        'user_id':session['user_id']
    }

    user = User.get_by_id(data)
    get_all_likes = Thought.get_all_likes(data)
    thoughts = Thought.show_all_thoughts()
    
    return render_template("thoughts.html",user=user,thoughts=thoughts,get_all_likes=get_all_likes)

@app.route('/create/thought',methods=['POST'])
def create_thought():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Thought.validate_thought(request.form):
        return redirect('/thoughts')
    data = {
        "thought": request.form["thought"],
        "thought": request.form["thought"],
        "thought": request.form["thought"],
        "user_id": session["user_id"]
    }
    Thought.create_thought(data)
    return redirect('/thoughts')

@app.route('/edit/<int:id>')
def edit_thought(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }

    edit=Thought.get_one(data)
    
    return render_template("edit.html",edit=edit)

@app.route('/delete/thought/<int:id>')
def delete_pie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id,
        "thought_id": id
    }
    Thought.destroy_thought(data)
    return redirect('/thoughts')

@app.route('/update/thought/<int:id>',methods=['POST'])
def update_thought(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Thought.validate_thought(request.form):
        return redirect(f'/edit/{id}')
    
    data = {
        "thought": request.form["thought"],
        "thought": request.form["thought"],
        "thought": request.form["thought"],
        "id": id
    }
    
    Thought.update_thought(data)
    return redirect('/thoughts')

@app.route('/all_thoughts')
def show_thoughts():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    # user = User.get_by_id(data)
    thoughts = Thought.show_all_thoughts()
    return render_template('all_thoughts.html',thoughts=thoughts)

@app.route('/users/<int:id>')
def show_thought(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id":id
    }
    user_data = {
        "id":session.get('user_id')
    }

    thought_by_user_data = {
        "id":id
    }
    
    thoughts=Thought.get_one(data)
    user=User.get_by_id(user_data)
    user2=User.get_by_id(thought_by_user_data)
    
    return render_template("users.html", thoughts=thoughts, user = user, user2=user2)

@app.route('/add_like/<int:id>')
def user_like(id):
    user_data = {
        "user_id": session['user_id'],
        "thought_id": id
        }
    # data = {
    #     "id":session['user_id']
    # }
    Thought.like(user_data)
    # Thought.get_all_likes(data)
    return redirect('/thoughts') 

@app.route('/remove_like/<int:id>')
def user_unlike(id):
    user_data = {
        "user_id": session['user_id'],
        "thought_id": id
        }
    # data = {
    #     "id":session['user_id']
    # }
    Thought.unlike(user_data)
    
    return redirect('/thoughts')






