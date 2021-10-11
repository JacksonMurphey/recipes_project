from recipes_app import app
from flask import redirect, render_template, request, session, flash
from recipes_app.models.user import User
from recipes_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt 


bcrypt = Bcrypt(app)

# initial page for user registration and login. 
@app.route('/')
def dashboard():
    return render_template('login_registration.html')



@app.route('/user/register', methods=['POST'])
def register_user():

    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }
    user_id = User.save(data)
    session['user_id'] = user_id    #this returns a number
    return redirect('/dashboard')


@app.route('/user/login', methods=['POST'])
def login_user():
    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        'email' :  request.form['email']
    }
    user = User.get_one_by_email(data)
    session['user_id'] = user.id    #this returns an object
    return redirect('/dashboard')



##################### ONLY LOGGED IN USER'S ROUTES BELOW ###############

@app.route('/dashboard')
def dash_user():
    if not 'user_id' in session: 
        flash('Must be logged in')
        return redirect('/')
    
    data = {'id': session['user_id']}
    user = User.get_user_recipes(data)

    recipes = Recipe.other_user_recipe(data)
    
    
    return render_template('user_dash.html', recipes=recipes,user=user)



@app.route('/user/logout')
def logout_user():
    session.pop('user_id')
    return redirect('/')

