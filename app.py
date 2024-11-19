from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Inicializar la app Flask
app = Flask(__name__)

# Habilitar CORS
CORS(app)

# Configuración de la base de datos (SQLite en este caso)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'  # Cambia según tu motor de base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de extensiones
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Modelo de la tabla "productos"
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    precio = db.Column(db.Float, nullable=False)

# Esquema para serialización/deserialización
class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto

# Instancias del esquema
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

# Crear la base de datos
with app.app_context():
    db.create_all()

# Rutas de la API
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.json
    nuevo_producto = Producto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion', ''),  # Descripción opcional
        precio=data['precio']
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    return producto_schema.jsonify(nuevo_producto), 201

@app.route('/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return productos_schema.jsonify(productos)

@app.route('/productos/<nombre>', methods=['GET'])
def obtener_producto_por_nombre(nombre):
    producto = Producto.query.filter_by(nombre=nombre).first()
    if producto:
        return producto_schema.jsonify(producto)
    return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.json
    producto.nombre = data.get('nombre', producto.nombre)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio = data.get('precio', producto.precio)
    db.session.commit()
    return producto_schema.jsonify(producto)

@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    db.session.delete(producto)
    db.session.commit()
    return jsonify({"message": "Producto eliminado exitosamente"}), 200

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('menuprod.html')

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
