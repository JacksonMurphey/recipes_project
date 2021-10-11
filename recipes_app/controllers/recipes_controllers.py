from recipes_app import app
from flask import redirect, render_template, request, session, flash
from recipes_app.models.recipe import Recipe
from recipes_app.models.user import User

@app.route('/recipe/new')
def recipe_new():
    if not 'user_id' in session: 
        flash('Must be logged in')
        return redirect('/')
    data = {'id': session['user_id']}
    user = User.get_one_user(data)
    return render_template('recipe_new.html', user=user)

@app.route('/recipe/create', methods=['POST'])
def recipe_create():
    if not 'user_id' in session: 
        flash('Must be logged in')
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under_thirty' : request.form['under_thirty'],
        'user_id' : request.form['user_id'],
    }
    Recipe.save(data)
    
    return redirect('/dashboard')

@app.route('/recipe/<int:recipe_id>')
def recipe_show(recipe_id):
    if not 'user_id' in session: 
        flash('Must be logged in')
        return redirect('/')
    data = {
        'id': recipe_id,
    }
    id = {'id': session['user_id']}
    user = User.get_one_user(id)
    recipe = Recipe.get_one_recipe(data)
    return render_template('recipe_show.html', recipe=recipe, user=user)
    
@app.route('/recipe/<int:recipe_id>/edit')
def recipe_edit(recipe_id):
    if not 'user_id' in session: 
        flash('Must be logged in')
        return redirect('/')
    data = {
        'id': recipe_id,
    
    }
    recipe = Recipe.get_one_recipe(data)
    
    return render_template('recipe_edit.html', recipe=recipe, user=session['user_id'])

@app.route('/recipe/<int:recipe_id>/update', methods=['POST'])
def recipe_update(recipe_id):
    if not 'user_id' in session: 
        flash('Must be logged in')
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipe/{recipe_id}/edit')
    data = {
        'id': recipe_id,
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under_thirty' : request.form['under_thirty'],
        'user_id' : request.form['user_id'],
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipe/<int:recipe_id>/destroy')
def recipe_destroy(recipe_id):
    data = {
        'id': recipe_id,
    }
    Recipe.delete(data)
    return redirect('/dashboard')