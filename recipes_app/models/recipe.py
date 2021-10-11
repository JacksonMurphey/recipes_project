
from recipes_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
from recipes_app.models import user

class Recipe:
    db_name = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_thirty = data['under_thirty']
        self.user = None
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, date_made, under_thirty, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_thirty)s, %(user_id)s, NOW(), NOW());'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_one_recipe(cls, data):
        query = 'SELECT * FROM recipes WHERE recipes.id = %(id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if not results: 
            return False
        else:
            return cls(results[0])

    @classmethod
    def get_all_recipes(cls):
        query = 'SELECT * FROM recipes;'
        results = connectToMySQL(cls.db_name).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_thirty = %(under_thirty)s, updated_at = NOW() WHERE recipes.id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_recipe_user(cls, data): 
        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data) # this always returns a list of dicts 
        recipe = cls(results[0])
        users_data = { 
            'id' : results[0]['users.id'], 
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at'],
        } 
        recipe.user = user.User(users_data)
        return recipe

    @classmethod
    def other_user_recipe(cls,data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE users.id != %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        recipes = []
        if results == None:
            pass
        else:
            for row in results:
                recipes.append(cls(row))
        return recipes
    


    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM recipes WHERE recipes.id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 4:
            flash('Recipe Name must be at least 4 characters', 'recipe')
            is_valid = False
        if len(data['description']) < 4:
            flash('Description must be at least 4 characters', 'recipe')
            is_valid = False
        if len(data['instructions']) < 4:
            flash('Instructions must be at least 4 characters', 'recipe')
            is_valid = False
        if data['date_made'] == "":
            is_valid = False
            flash("Please enter a date","recipe")
        # if  data['under_thirty'] == "":
        #     flash('You must select Yes or No, for over/under 30minutes', 'recipe')
        #     is_valid = False
        return is_valid 