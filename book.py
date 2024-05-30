from flask import Flask, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for
from flask import Flask,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bk_review'
db = SQLAlchemy(app)

class Registrations(db.Model):
	
    sno = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(70),nullable=False)
    contactno=db.Column(db.String(12),nullable=False)
    country=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(20),nullable=False)
   
class Book(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    reviews = db.relationship('Review', backref='book', lazy=True)
    img_file = db.Column(db.String(255),nullable=True)


class Review(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), db.ForeignKey('book.slug'), nullable=False)
    img_file = db.Column(db.String(255),nullable=True)
    review = db.Column(db.Text, nullable=False)

# @app.route("/")
# def hello_world():
#     return render_template("login.html")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = Registrations.query.filter_by(name=name, password=password).first()
        if user:
            return redirect(url_for('bookzone'))
        else:
            return render_template('login.html', message='Invalid credentials. Please try again.')
    return render_template('login.html')

# @app.route('/success')
# def success():
#     return render_template('home.html')

@app.route("/bookzone")
def bookzone():
    # Retrieve all reviews
    reviews = Review.query.all()
    
    # Create a set to store unique book slugs
    unique_book_slugs = set()
    
    # Filter out duplicate books and store their slugs in the set
    unique_reviews = []
    for review in reviews:
        if review.book.slug not in unique_book_slugs:
            unique_reviews.append(review)
            unique_book_slugs.add(review.book.slug)
    
    return render_template("home.html", reviews=unique_reviews)



# @app.route("/review_page/<string:review_slug>", methods=['GET','POST'])
# def review(review_slug):
#     review = Review.query.filter_by(slug=review_slug).first()
#     return render_template('review.html', review=review)

# @app.route("/book/<int:book_id>")
# def book_details(book_id):
#     book = Book.query.get_or_404(book_id)
#     reviews = book.reviews
#     return render_template('book_details.html', book=book, reviews=reviews)

@app.route("/review_page/<string:review_slug>", methods=['GET','POST'])
def review(review_slug):
    book = Book.query.filter_by(slug=review_slug).first_or_404()
    reviews = book.reviews
    review = Review.query.filter_by(slug=review_slug).first_or_404()  # Fetch review based on slug
    return render_template('review.html', book=book, reviews=reviews, review=review)  # Pass review to template



@app.route("/review_page/<string:review_slug>/add_review", methods=["POST"])
def add_review(review_slug):
    if request.method == "POST":
        name = request.form["name"]
        review_text = request.form["review"]
        img_file = request.form.get("img_file")  # Assuming img_file is part of the form
        
        # Check if img_file is None and provide a default value
        if img_file is None:
            img_file = "default.jpg"  # Provide a default image file name
        
        # Assuming you have validation for content and rating
        
        new_review = Review(name=name, review=review_text, slug=review_slug, img_file=img_file)
        db.session.add(new_review)
        db.session.commit()
        
        return redirect(url_for("review", review_slug=review_slug))


@app.route("/about")
def About():
    return render_template("about.html")

# @app.route("/login", methods=['POST','GET'])
# def login():
#     if request.method == 'POST':
#         if request.form['email'] == 'jayesh@h.com':

#             return render_template("about.html")
#         else:
#             print("Yooo")
#             return render_template("home.html")
#     else:
#         return render_template("/about.html")

@app.route("/signup", methods=['POST','GET'])
def register():
    if request.method=='POST':
        name = request.form.get('name')
        phone = request.form.get('contact')
        country = request.form.get('country')
        email = request.form.get('email')
        password = request.form.get('password')
        user = Registrations(name=name, contactno=phone, country=country, email=email, password=password)
        db.session.add(user)
        db.session.commit()
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
