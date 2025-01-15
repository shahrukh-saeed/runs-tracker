from flask import Flask, request, render_template
from database import *

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login/confirm', methods=['POST'])
def login_confirm():
    email = request.form.get('email')
    password = request.form.get('password')

    users = get_users()
    
    for user in users:
        if user['email'] == email and user['password'] == password:
            userID = user['userID']
            userGames = get_user_games(userID)
            return render_template('dashboard.html', userID=userID, get_user_game_team_total_runs=get_user_game_team_total_runs,
                                   get_user_team_name=get_user_team_name, userGames=userGames)

    return render_template('login.html', error=True)

@app.route('/create-account')
def create_account():
    return render_template('create-account.html')

@app.route('/create-account/confirm', methods=['POST'])
def create_account_confirm():
    email = request.form.get('email')
    password = request.form.get('password')

    insert_user(email, password)

    return render_template('login.html')

@app.route('/dashboard/view-user-game', methods=['POST'])
def view_user_game():
    userID = request.form.get('userID')
    gameID = request.form.get('gameID')
    team1ID = request.form.get('team1ID')
    team2ID = request.form.get('team2ID')

    team1Name = get_user_team_name(userID, team1ID)
    team2Name = get_user_team_name(userID, team2ID)

    team1Scores = get_user_game_team_scores(userID, gameID, team1ID)
    team1totalRuns = get_user_game_team_total_runs(userID, gameID, team1ID)

    team2Scores = get_user_game_team_scores(userID, gameID, team2ID)
    team2totalRuns = get_user_game_team_total_runs(userID, gameID, team2ID)

    return render_template('view-user-game.html', gameID=gameID, team1Name=team1Name, team2Name=team2Name, team1Scores=team1Scores, team1totalRuns=team1totalRuns, team2Scores=team2Scores,
                           team2totalRuns=team2totalRuns)

@app.route('/dashboard/new-game', methods=['POST'])
def new_game():
    userID = request.form.get('userID')
    lastGameID = get_games()[-1]['gameID']

    newGameID = int(lastGameID) + 1

    return render_template('new-game.html', userID=userID, newGameID=newGameID)

@app.route('/dashboard/new-game/confirm', methods=['POST'])
def new_game_confirm():
    userID = request.form.get('userID')
    gameID = request.form.get('gameID')
    team1ID = request.form.get('team1ID')
    team2ID = request.form.get('team2ID')

    team1Name = get_user_team_name(userID, team1ID)
    team2Name = get_user_team_name(userID, team2ID)

    if team1Name != None and team2Name != None:
        insert_game(userID, gameID, team1ID, team2ID)
    else:
        if team1Name == None:
            return render_template('new-game.html', error=True, errMsg='Team 1 ID is invalid', userID=userID, newGameID=gameID)
        elif team2Name == None:
            return render_template('new-game.html', error=True, errMsg='Team 2 ID is invalid', userID=userID, newGameID=gameID)
    
    return get_user_games(userID)

if __name__ == '__main__':
    app.run(debug=True)
