from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configurar la conexión a la base de datos MySQL en XAMPP
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bdsoftware_web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Modelo de la tabla "productos"
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)

# Esquema para serialización
class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

# Ruta base para mostrar index.html
@app.route('/')
def index():
    return render_template('menuprod.html')

# Rutas para el CRUD
@app.route('/productos', methods=['POST'])
def crear_producto():
    try:
        data = request.json
        nuevo_producto = Producto(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=data['precio']
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return producto_schema.jsonify(nuevo_producto), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        productos = Producto.query.all()
        return productos_schema.jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return jsonify({"error": "La ruta solicitada no existe"}), 404

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
