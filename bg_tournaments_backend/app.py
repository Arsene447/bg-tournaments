from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель турнира
class Tournament(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID
    name = db.Column(db.String(100), nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    games = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    participants = db.relationship('Participant', backref='tournament', cascade="all, delete-orphan")

# Модель участника
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False)
    tournament_id = db.Column(db.String(36), db.ForeignKey('tournament.id'), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-tournament', methods=['GET', 'POST'])
def create_tournament():
    if request.method == 'POST':
        tournament_id = str(uuid.uuid4())
        new_tournament = Tournament(
            id=tournament_id,
            name=request.form['tournament_name'],
            fee=int(request.form['tournament_fee']),
            games=int(request.form['tournament_games']),
            points=int(request.form['points_for_place'])
        )
        db.session.add(new_tournament)
        db.session.commit()
        return redirect(url_for('tournament', tournament_id=tournament_id))

    return render_template('create-tournament.html')

@app.route('/tournament/<tournament_id>', methods=['GET', 'POST'])
def tournament(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)

    if request.method == 'POST':
        nickname = request.form.get('nickname')
        if nickname and not Participant.query.filter_by(nickname=nickname, tournament_id=tournament_id).first():
            new_participant = Participant(nickname=nickname, tournament_id=tournament_id)
            db.session.add(new_participant)
            db.session.commit()

    participants = [p.nickname for p in tournament.participants]
    return render_template(
        'tournament.html',
        name=tournament.name,
        fee=tournament.fee,
        games=tournament.games,
        points=tournament.points,
        participants=participants
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
