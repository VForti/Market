from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from settings import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///shop.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    image = db.Column(db.LargeBinary)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary)
    title = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route('/')
@app.route('/home')
def index():
    categorys = Category.query.order_by(Category.name).all()
    return render_template('index.html', data=categorys)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create/item', methods=['POST','GET'])
def create_item():
    return render_template('create_item.html')

@app.route('/create/category', methods=['POST','GET'])
def create_category():
    errors = []
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']


        image.save('static/img')

        category = Category(name=name, image=image)


        try:
            db.session.add(category)
            db.session.commit()
            return redirect('/')

        except:
            """"Помилка"""
    else:
        return render_template('create_category.html')

if __name__ == '__main__':
    app.run(debug=True)
