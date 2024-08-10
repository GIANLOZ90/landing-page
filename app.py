from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Definizione del modello per l'Utente
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Definizione del modello per la Scheda di Allenamento
class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('workout_plans', lazy=True))

    def __repr__(self):
        return f'<WorkoutPlan {self.name}>'

@app.route('/')
def index():
    return "Flask and SQLAlchemy are working!"

# Rotta per aggiungere dati
@app.route('/add')
def add_data():
    # Verifica se l'utente esiste già
    existing_user = User.query.filter_by(email='john@example.com').first()
    if existing_user is None:
        new_user = User(username='john_doe', email='john@example.com')
        db.session.add(new_user)
        db.session.commit()
    else:
        new_user = existing_user

    # Crea una scheda di allenamento per l'utente
    workout_plan = WorkoutPlan(name='Strength Training', description='A plan for building muscle strength', user_id=new_user.id)
    db.session.add(workout_plan)
    db.session.commit()

    return "Data added!"

# Rotta per visualizzare tutti gli utenti
@app.route('/users')
def users():
    all_users = User.query.all()
    return '<br>'.join([f'ID: {user.id}, Username: {user.username}, Email: {user.email}' for user in all_users])

# Rotta per visualizzare tutte le schede di allenamento
@app.route('/workout_plans')
def workout_plans():
    all_plans = WorkoutPlan.query.all()
    return '<br>'.join([f'ID: {plan.id}, Name: {plan.name}, Description: {plan.description}, User ID: {plan.user_id}' for plan in all_plans])

# Rotta per aggiungere una scheda di allenamento tramite form
@app.route('/add_workout', methods=['POST'])
def add_workout():
    username = request.form['username']
    name = request.form['name']
    description = request.form['description']

    # Trova l'utente corrispondente
    user = User.query.filter_by(username=username).first()
    if user:
        new_workout = WorkoutPlan(name=name, description=description, user_id=user.id)
        db.session.add(new_workout)
        db.session.commit()
        return "Workout plan added!"
    else:
        return "User not found!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea le tabelle nel database
    app.run(debug=True)
import os
from flask import Flask

app = Flask(__name__)

# Definisci qui le tue rotte e logiche

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
