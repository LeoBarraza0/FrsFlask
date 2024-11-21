from flask import Flask, render_template 
from Login.app import create_app, db 
from Login.app.auth.models import User 

app = create_app("prod") 
print(f"Carpeta estática por defecto: {app.static_folder}")

with app.app_context(): 
    db.create_all() 
    if not User.query.filter_by(user_name="test").first():
        User.create_user( 
            user="test", 
            email="test-testing@test.com", 
            password="test**123" 
            )
        
@app.route('/') 
def menuprod(): 
    return render_template('menuprod.html') 

if __name__ == '__main__': app.run(debug=True)