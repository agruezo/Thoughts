from flask_app import app
# DON'T FORGET TO IMPORT ALL YOUR CONTROLLERS!!!
from flask_app.controllers import thoughts, users

if __name__ == '__main__':
    app.run(debug=True)

    