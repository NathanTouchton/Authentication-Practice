from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'bka,rc.idaobacgkxapuds'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

#Lines below only required once, when creating DB.
# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
    """Renders homepage."""
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    """This is the registration page. Adds user to database."""
    if request.method == "POST":
        with app.app_context():
            # Creates dictionary from the form data in register.html, and adds it to the database.
            new_user_dict = {
                "email": request.form["email"],
                "password": generate_password_hash(
                    password=request.form["password"],
                    salt_length=16
                ),
                "name": request.form["name"],
            }
            new_user = User(
                email=new_user_dict["email"],
                password=new_user_dict["password"],
                name=new_user_dict["name"],
            )
            db.session.add(new_user)
            db.session.commit()
            session["name"] = new_user_dict["name"]
        return redirect(url_for("secrets"))

    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    # Greets user by name and gives them access to cheat_sheet.pdf
    name = session.get("name")
    return render_template("secrets.html", name=name)


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory(
        directory="static", path="files/cheat_sheet.pdf"
    )
