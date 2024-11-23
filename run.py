from flask import Flask, render_template 
from Login.app import create_app, db 
from Login.app.auth.models import User 
from flask import Flask, send_from_directory


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
@app.route('/static/compra/product.json')
def serve_product_json():
    return send_from_directory('static/compra', 'product.json')

if __name__ == '__main__': app.run(debug=True)