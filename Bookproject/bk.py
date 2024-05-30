from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    reviews = db.relationship('Review', backref='book', lazy=True)  # Define relationship here

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

from flask import Flask, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/book_review'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('success'))
        else:
            return render_template('login.html', message='Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/success')
def success():
    return render_template('home.html')


@app.route("/code")
def home():
    books = Book.query.all()  # Change Books to Book
    return render_template('home.html', books=books)


@app.route("/book/<int:book_id>")
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = book.reviews
    return render_template('book_details.html', book=book, reviews=reviews)

@app.route("/book/<int:book_id>/add_review", methods=["POST"])
def add_review(book_id):
    if request.method == "POST":
        content = request.form["content"]
        rating = request.form["rating"]
        
        # Assuming you have validation for content and rating
        
        new_review = Review(content=content, rating=rating, book_id=book_id)
        db.session.add(new_review)
        db.session.commit()
        
        return redirect(url_for("book_details", book_id=book_id))

if __name__ == "__main__":
    app.run(debug=True)
