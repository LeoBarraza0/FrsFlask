from datetime import datetime
from Login.app import db, bcrypt
from Login.app import login_manager
from flask_login import UserMixin

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def create_product(cls, name, price, stock):
        product = cls(name=name, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        return product

def get_all_products():
    return Product.query.all()

def filtrar():
    return Product.query.filter_by(name="Laptop").all()



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