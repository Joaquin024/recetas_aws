from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked_made = data['date_cooked_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.first_name = data ['first_name'] #Nombre de la persona que creó la receta

        #VALIDA la receta
    @staticmethod
    def validate_recipe(form):
        is_valid = True

        if len(form['name']) < 3:
            flash('El nombre de la receta debe tener al menos 3 caracteres', 'recipe')
            is_valid = False

        if len(form['description']) < 3:
            flash('la descripcion debe tener al menos 3 caracteres', 'recipe')
            is_valid = False

        if len(form['instructions']) < 3:
            flash('las instrucciones debe tener al menos 3 caracteres', 'recipe')
            is_valid = False

        if form['date_cooked_made'] == "":
            flash('ingrese una fecha valida', 'recipe')
            is_valid = False

        return is_valid
        
        #Guarda la receta
    @classmethod
    def save(cls, form):
        query = "INSERT INTO recipes (name, description, instructions, date_cooked_made, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked_made)s, %(under_30)s, %(user_id)s)"
        result = connectToMySQL('recetas').query_db(query, form)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT recipes.*, users.first_name FROM recipes JOIN users ON user_id = users.id"
        results = connectToMySQL('recetas').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe)) #1.- cls(recipe) crea la instancia con la info del diccionario. 2.- Agregamos la instancia a la lista de recetas
        return recipes
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT recipes.*, users.first_name FROM recipes JOIN users ON user_id = users.id WHERE recipes.id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, data)
        recipe = cls(result[0])
        return recipe
    
    @classmethod
    def update(cls, form):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked_made=%(date_cooked_made)s, under_30=%(under_30)s WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, form)
        return result
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, data)
        return result
