from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

        return redirect(url_for(
            'tournament',
            name=tournament_name,
            fee=tournament_fee,
            games=tournament_games,
            points=points_for_place
        ))

    return render_template('create-tournament.html')

@app.route('/tournament')
def tournament():
    name = request.args.get('name')
    fee = request.args.get('fee')
    games = request.args.get('games')
    points = request.args.get('points')
    return render_template('tournament.html', name=name, fee=fee, games=games, points=points)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
