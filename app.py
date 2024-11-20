from flask import Flask, render_template
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
    app.run(debug=True)
