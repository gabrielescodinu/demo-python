from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Sostituisci 'username', 'password', 'hostname' e 'dbname' con i valori corretti
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/school_nodejs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Crea l'istanza di SQLAlchemy
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def hello():
    return render_template('index.html', message='Ciao, benvenuto nella mia web app!')


@app.route('/about')
def about():
    return 'Questa è la pagina About!'


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Qui potresti inviare l'email utilizzando un servizio come SendGrid, Mailgun, etc.

    return redirect(url_for('email_sent'))


@app.route('/email_sent')
def email_sent():
    return 'Email inviata con successo!'


@app.route('/create_user/<username>/<email>')
def create_user(username, email):
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return f'Utente creato con successo: {new_user}'


if __name__ == '__main__':
    app.run(debug=True)
