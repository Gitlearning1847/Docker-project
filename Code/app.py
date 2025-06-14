from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ✅ Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///site.db')  # fallback for local testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ✅ Create a user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed in real app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query', '')
    return render_template('search.html', query=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')  # you'd hash and check this
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return f"Welcome {username}"
        else:
            return "Invalid login"
    return render_template('login.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create tables on startup (dev only)
    app.run(host='0.0.0.0', port=5000, debug=True)
