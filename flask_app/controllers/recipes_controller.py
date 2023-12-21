from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

#importacion de modelos

from flask_app.models.users import User
from flask_app.models.recipes import Recipe

#RUTAS
@app.route('/recipes/new')
def recipes_new():
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    return render_template('new.html')

#RUTA PARA DESPLEGAR EL FORMULARIO
@app.route('/recipes/create', methods=['POST'])
def recipes_create():
    if 'user_id' not in session:
        flash('Favor de iniciar sesion','not_in_session')
        return redirect('/')

#Verificar que el usuario 
    if 'user_id' not in session:
        flash('Favor de iniciar sesión','not_in_session')
        return redirect('/')

    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

#RUTA PARA GUARDAR (debemos de revisar que se haya iniciado)
    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/recipes/show/<int:id>')
def recipes_show(id):
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    diccionario = {"id":id}
    recipe = Recipe.get_by_id(diccionario)
    return render_template('show.html', recipe=recipe)

@app.route('/recipes/edit/<int:id>')
def recipes_edit(id):
    if 'user_id' not in session:
        flash('Favor de iniciar sesión','not_in_session')
        return redirect('/')
    
    diccionario = {"id": id}
    recipe = Recipe.get_by_id(diccionario)
    if recipe.user_id != session['user_id']:
        return redirect('/dashboard')
    return render_template('edit.html', recipe=recipe)

@app.route('/recipes/update', methods=['POST'])
def recipes_update():
    if 'user_id' not in session:
        flash('Favor de iniciar sesión','not_in_session')
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/edit/'+request.form['id'])
    
    Recipe.update(request.form)
    return redirect('/dashboard')

@app.route('/recipes/delete/<int:id>')
def recipes_delete(id):
    if 'user_id' not in session:
        flash('Favor de iniciar sesión','not_in_session')
        return redirect('/')
    diccionario = {"id": id}
    Recipe.delete(diccionario)

    return redirect('/dashboard')