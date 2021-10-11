from recipes_app import app
from recipes_app.controllers import users_controller, recipes_controllers


if __name__ == '__main__':
    app.run(debug=True)