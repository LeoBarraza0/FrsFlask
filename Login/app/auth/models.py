from datetime import datetime
from Login.app import db, bcrypt
from Login.app import login_manager
from flask_login import UserMixin

class Producto(db.Model):
    __tablename__ = "producto"

    idProducto = db.Column(db.String(255), primary_key=True)
    Descripcion = db.Column(db.String(255), nullable=False)
    Precio = db.Column(db.Float, nullable=False)
    Nombre = db.Column(db.String(255), nullable=False)
    Stock = db.Column(db.BigInteger, nullable=False)
    Referencia = db.Column(db.String(255), nullable=False)
    Img = db.Column(db.LargeBinary, nullable=False)
    IdProvFK = db.Column(db.Integer, db.ForeignKey('proveedor.idProv'), nullable=False)

class Proveedor(db.Model):
    __tablename__ = "proveedor"

    idProv = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(255), nullable=False)
    Direccion = db.Column(db.String(255), nullable=False)
    Telefono = db.Column(db.String(255), nullable=False)
    Correo = db.Column(db.String(255), nullable=False)
    IdTipoProv = db.Column(db.String(255), db.ForeignKey('tipoproveedor.idTipoProv'), nullable=False)
    Estado = db.Column(db.String(255), nullable=False)

class TipoProveedor(db.Model):
    __tablename__ = "tipoproveedor"

    idTipoProv = db.Column(db.String(255), primary_key=True)
    Nombre = db.Column(db.String(255), nullable=False)

class DetalleTrans(db.Model):
    __tablename__ = "detalletrans"

    idDetTrans = db.Column(db.String(255), primary_key=True)
    IdProduct = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), nullable=False)
    Cantidad = db.Column(db.BigInteger, nullable=False)
    PrecioBruto = db.Column(db.Float, nullable=False)
    Impuesto = db.Column(db.Float, nullable=False)
    Neto = db.Column(db.Float, nullable=False)
    IdTransFK = db.Column(db.Integer, db.ForeignKey('transaccion.IdTransc'), nullable=False)

class Transaccion(db.Model):
    __tablename__ = "transaccion"

    IdTransc = db.Column(db.String(255), primary_key=True)
    Fecha = db.Column(db.DateTime, nullable=False)
    IdCliente = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    Estado = db.Column(db.String(255), nullable=False)
    DirEnvio = db.Column(db.String(255), nullable=False)
    MedioPago = db.Column(db.String(255), nullable=False)

class Opinion(db.Model):
    __tablename__ = "opinion"

    NoCaso = db.Column(db.String(255), primary_key=True)
    Fecha = db.Column(db.DateTime, nullable=False)
    Descripcion = db.Column(db.String(255), nullable=False)
    IdProductoFK = db.Column(db.String(255), db.ForeignKey('producto.idProducto'), nullable=False)
    Calificacion = db.Column(db.BigInteger, nullable=False)

class OpinionCliente(db.Model):
    __tablename__ = "opinion_cliente"

    IdOpcCli = db.Column(db.String(255), primary_key=True)
    IdOpFK = db.Column(db.String(255), db.ForeignKey('opinion.NoCaso'), nullable=False)
    IdClienteFK = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)

# Funciones de ejemplo para interactuar con las tablas
def get_all_products():
    return Producto.query.all()

def filtrar():
    return Producto.query.filter_by(Nombre="Laptop").all()




class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60), unique=True,index=True)
    user_password = db.Column(db.String(80))
    create_date = db.Column(db.DateTime, default=datetime.now)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)
    
    @classmethod
    def create_user(cls, user, email, password):
        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode("utf-8")
        )

        db.session.add(user)
        db.session.commit()
        return user



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))