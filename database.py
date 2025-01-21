import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def establish_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return conn

def get_users():
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM user
    """
    )

    result = cursor.fetchall()
    users = []

    for userID, email, password in result:
        users.append({'userID': userID, 'email': email, 'password': password})

    conn.commit()
    cursor.close()
    conn.close()

    return users

def get_teams():
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM team
    """
    )

    result = cursor.fetchall()
    teams = []

    for userID, teamID, teamName in result:
        teams.append({'userID': userID, 'teamID': teamID, 'teamName': teamName})

    conn.commit()
    cursor.close()
    conn.close()

    return teams

def get_user_teams(userID):
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM team WHERE userID = %s
    """, (userID,)
    )

    result = cursor.fetchall()
    userTeams = []

    for _, teamID, teamName in result:
        userTeams.append({'userID': userID, 'teamID': teamID, 'teamName': teamName})

    conn.commit()
    cursor.close()
    conn.close()

    return userTeams

def get_user_team_name(userID, teamID):
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM team WHERE userID = %s AND teamID = %s
    """, (userID, teamID)
    )

    result = cursor.fetchone()

    team = None
    
    if result:
        team = {'userID': userID, 'teamID': teamID, 'teamName': result[2]}
    else:
        return None

    conn.commit()
    cursor.close()
    conn.close()

    return team['teamName']

def get_games():
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM game
    """
    )

    result = cursor.fetchall()
    games = []

    for userID, gameID, team1ID, team2ID in result:
        games.append({'userID': userID, 'gameID': gameID, 'team1ID': team1ID, 'team2ID': team2ID})

    conn.commit()
    cursor.close()
    conn.close()

    return games

def get_user_games(userID):
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM game WHERE userID = %s
    """, (userID,)
    )

    result = cursor.fetchall()
    userGames = []

    for _, gameID, team1ID, team2ID in result:
        userGames.append({'userID': userID, 'gameID': gameID, 'team1ID': team1ID, 'team2ID': team2ID})

    conn.commit()
    cursor.close()
    conn.close()

    return userGames

def get_scores():
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM score
    """
    )

    result = cursor.fetchall()
    scores = []

    for userID, gameID, teamID, ballNum, runs in result:
        scores.append({'userID': userID, 'gameID': gameID, 'teamID': teamID, 'ballNum': ballNum, 'runs': runs})

    conn.commit()
    cursor.close()
    conn.close()

    return scores

def get_user_game_team_total_runs(userID, gameID, teamID):
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM score WHERE userID = %s AND gameID = %s AND teamID = %s
    """, (userID, gameID, teamID)
    )

    result = cursor.fetchall()
    totalRuns = 0

    for _, _, _, _, runs in result:
        totalRuns += runs

    conn.commit()
    cursor.close()
    conn.close()

    return totalRuns

def get_user_game_team_scores(userID, gameID, teamID):
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM score WHERE userID = %s AND gameID = %s AND teamID = %s
    """, (userID, gameID, teamID)
    )

    result = cursor.fetchall()
    scores = []

    for userID, gameID, teamID, ballNum, runs in result:
        scores.append({'userID': userID, 'gameID': gameID, 'teamID': teamID, 'ballNum': ballNum, 'runs': runs})

    conn.commit()
    cursor.close()
    conn.close()

    return scores

def insert_user(email, password):
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO user (email, password) VALUES (%s, %s)
    """,
    (email, password)
    )

    conn.commit()
    cursor.close()
    conn.close()

def insert_team(userID, teamID, teamName):
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO team (userID, teamID, teamName) VALUES (%s, %s, %s)
    """,
    (userID, teamID, teamName)
    )

    conn.commit()
    cursor.close()
    conn.close()

def insert_game(userID, gameID, team1ID, team2ID):
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO game (userID, gameID, team1ID, team2ID) VALUES (%s, %s, %s, %s)
    """,
    (userID, gameID, team1ID, team2ID)
    )

    conn.commit()
    cursor.close()
    conn.close()

def insert_score(userID, gameID, teamID, ballNum, runs):
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO score (userID, gameID, teamID, ballNum, runs) VALUES (%s, %s, %s, %s, %s)
    """,
    (userID, gameID, teamID, ballNum, runs)
    )

    conn.commit()
    cursor.close()
    conn.close()