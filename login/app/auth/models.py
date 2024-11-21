from datetime import datetime
from app import db, bcrypt
from app import login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(60), unique=True,index=True)
    user_password = db.Column(db.String(80))

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)
    
    @classmethod
    def create_user(cls, user, email, password):
        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode("utf-8")
        )

        db.session.add(user)
        db.session.commit("Se ha agregado un usuario")
        return user



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))