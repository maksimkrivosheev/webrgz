from flask import Flask, render_template, request, make_response, redirect, session, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iniciativa.db'
db = SQLAlchemy(app)


class Iniciativa(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(300), nullable=False)
        text = db.Column(db.Text, nullable=False)

def start():
    if 'username' in session:
        return redirect('/index.html')
    else:
        return render_template("login.html")


@app.route('/index.html')
def main():
    if 'username' in session:
        return render_template("index.html")
    else:
        return "Войдите, чтобы просмотреть"

users = {
    'zxc': generate_password_hash('zxc'),
    'zxc': generate_password_hash('zxc')
}

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect('/')
        else:
            return "Пароль не верный", 401
    else:
        return render_template("login.html")


def require_login(func):
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        else:
            return abort(401, description="Успешно")
    return wrapper


@app.route('/index')
@app.route('/')
def index():
        return render_template('index.html')



@app.route('/posts')
def posts():
        posts = Iniciativa.query.all()
        return render_template('posts.html', posts=posts)


@app.route('/about')
def about():
        return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
        if request.method == 'POST':
                title = request.form['title']
                text = request.form['text']

                inic = Iniciativa(title=title, text=text)

                try:
                        db.session.add(inic)
                        db.session.commit()
                        return redirect('/')
                except:
                        return "При добавлении инициативы произошла какая-то ошибка!"

        return render_template('create.html')


if __name__ == 'main':
        app.run(debug=True)