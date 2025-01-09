from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    links = db.relationship('Link', backref='category', lazy=True)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

@app.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@app.route('/add_link', methods=['GET', 'POST'])
def add_link():
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        description = request.form['description']
        category_id = request.form['category']
        new_link = Link(title=title, url=url, description=description, category_id=category_id)
        db.session.add(new_link)
        db.session.commit()
        flash('Link added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_link.html', categories=categories)

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_category.html')

@app.route('/move_link/<int:link_id>', methods=['POST'])
def move_link(link_id):
    link = Link.query.get_or_404(link_id)
    new_category_id = request.form['category']
    link.category_id = new_category_id
    db.session.commit()
    flash('Link moved successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit_link/<int:link_id>', methods=['GET', 'POST'])
def edit_link(link_id):
    link = Link.query.get_or_404(link_id)
    categories = Category.query.all()
    if request.method == 'POST':
        link.title = request.form['title']
        link.url = request.form['url']
        link.description = request.form['description']
        link.category_id = request.form['category']
        db.session.commit()
        flash('Link updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_link.html', link=link, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
