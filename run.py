'''
#from flask import Flask, render_template
from flask_cors import CORS

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)

# Ruta para renderizar el índice
@app.route('/')
def index():
    return render_template('menuprod.html')

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)#
'''
from venv import create
from login.app import create_app, db
from login.app.auth.models import User


flask_scrapy_app =  create_app("prod")
with flask_scrapy_app.app_context():
    db.create_all()
    if not User.query.filter_by(user_name="test").first():
        User.create_user(
            user="test",
            email="test-testing@test.com",
            password="test**123"
        )
flask_scrapy_app.run()
