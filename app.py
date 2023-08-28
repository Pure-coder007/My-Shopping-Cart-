from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

import cloudinary
import cloudinary.uploader

cloudinary.config( 
  cloud_name = "duyoxldib", 
  api_key = "778871683257166", 
  api_secret = "NM2WHVuvMytyfnVziuzRScXrrNk" 
)




app = Flask(__name__)
# app.secret_key = os.environ.get("SECRET_KEY", "dikekiyuioiu907967p9[pk]#$%^")  # Use an environment variable for the secret key


# db = SQLAlchemy(app)
# with app.app_context():
#     db.create_all()

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# SQLite Configuration

DB_PATH = os.environ.get('SQLITE_DB_PATH', 'sqlite:///mydatabase.db')  # Default SQLite path
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.config['SECRET_KEY'] = '1e04deb868b1640f313bbb8c680f3d49'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # price = db.Column(db.Float(100), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)

    
    

@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", items=all_data[::-1])

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        new_item = Data(name=name,  quantity=quantity)
        
        
    if 'image' in request.files:
        image = request.files['image']
        if image:
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result['url']
            new_item.image_url = image_url   
        
        
        if not name or not quantity:
            flash("Please enter all fields!")
            return redirect(url_for('Index'))
        
    # if 'image' in request.files:
    #     image = request.files['image']
    #     if image:
    #         upload_result = cloudinary.uploader.upload(image)
    #         image_url = upload_result['url']
    #         new_item.image_url = image_url   
        
        

        db.session.add(new_item)
        db.session.commit()

        flash("Item Added To Cart")
        return redirect(url_for('Index'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        item = Data.query.get(request.form.get('id'))
        
        if not item:
            flash("item not found!")
            return redirect(url_for('Index'))

        item.name = request.form['name']
        # item.price = request.form['price']
        item.quantity = request.form['quantity']
        db.session.commit()

        flash("Item Updated Successfully")
        return redirect(url_for('Index'))

@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete(id):
    item = Data.query.get(id)
    if not item:
        flash("Item not found!")
        return redirect(url_for('Index'))

    db.session.delete(item)
    db.session.commit()
    flash("Item Deleted Successfully")
    return redirect(url_for('Index'))

if __name__ == "__main__":
    with  app.app_context():
        db.create_all()
    app.run(debug=True)
