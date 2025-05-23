from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

# Хранилище турниров и участников: { tournament_id: {name, fee, games, points, participants: []} }
tournaments = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-tournament', methods=['GET', 'POST'])
def create_tournament():
    if request.method == 'POST':
        tournament_name = request.form['tournament_name']
        tournament_fee = request.form['tournament_fee']
        tournament_games = request.form['tournament_games']
        points_for_place = request.form['points_for_place']

        tournament_id = str(uuid.uuid4())
        tournaments[tournament_id] = {
            'name': tournament_name,
            'fee': tournament_fee,
            'games': tournament_games,
            'points': points_for_place,
            'participants': []
        }

        return redirect(url_for('tournament', tournament_id=tournament_id))

    return render_template('create-tournament.html')

@app.route('/tournament/<tournament_id>', methods=['GET', 'POST'])
def tournament(tournament_id):
    tournament = tournaments.get(tournament_id)
    if not tournament:
        return "Турнир не найден", 404

    if request.method == 'POST':
        nickname = request.form.get('nickname')
        if nickname and nickname not in tournament['participants']:
            tournament['participants'].append(nickname)

    return render_template(
        'tournament.html',
        name=tournament['name'],
        fee=tournament['fee'],
        games=tournament['games'],
        points=tournament['points'],
        participants=tournament['participants']
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
