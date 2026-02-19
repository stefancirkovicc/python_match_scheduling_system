import pymysql
from datetime import datetime


# Funkcija za povezivanje sa bazom
def connect_to_database():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Mozdabek15",  # Promeni prema tvojoj MySQL šifri
        database="python"
    )


# Dohvatanje naziva tima po ID-ju
def get_team_name_by_id(team_id):
    con = connect_to_database()
    cursor = con.cursor()

    # Proveri upit i rezultat
    cursor.execute("SELECT name FROM teams WHERE id = %s", (team_id,))
    result = cursor.fetchone()
    con.close()

    # Dodaj debug ispis za praćenje
    return result[0] if result else "Nepoznat tim"


# Dohvatanje svih utakmica sa imenima timova
def get_all_games():
    con = connect_to_database()
    cursor = con.cursor()

    # Dohvati sve utakmice sa ID-jevima
    cursor.execute("SELECT id, team_a_id, team_b_id, home_team_id, match_date FROM games")
    games = cursor.fetchall()
    con.close()

    # Prevedi ID-jeve u nazive
    games_with_names = []
    for game in games:
        game_id = game[0]
        team_a_name = get_team_name_by_id(game[1])
        team_b_name = get_team_name_by_id(game[2])
        home_team_name = get_team_name_by_id(game[3])
        match_date = game[4]
        games_with_names.append((game_id, team_a_name, team_b_name, home_team_name, match_date))

    return games_with_names


# Zakazivanje nove utakmice
def schedule_match(team_a, team_b, home_team, match_date):
    con = connect_to_database()
    cursor = con.cursor()

    # Dodaj timove ako ne postoje
    cursor.execute("SELECT id FROM teams WHERE name = %s", (team_a,))
    team_a_id = cursor.fetchone()
    if not team_a_id:
        cursor.execute("INSERT INTO teams (name) VALUES (%s)", (team_a,))
        con.commit()
        team_a_id = cursor.lastrowid
    else:
        team_a_id = team_a_id[0]

    cursor.execute("SELECT id FROM teams WHERE name = %s", (team_b,))
    team_b_id = cursor.fetchone()
    if not team_b_id:
        cursor.execute("INSERT INTO teams (name) VALUES (%s)", (team_b,))
        con.commit()
        team_b_id = cursor.lastrowid
    else:
        team_b_id = team_b_id[0]

    # Odredi ID domaćina
    home_team_id = team_a_id if home_team == "Tim A" else team_b_id

    cursor.execute(
        "INSERT INTO games (team_a_id, team_b_id, home_team_id, match_date) VALUES (%s, %s, %s, %s)",
        (team_a_id, team_b_id, home_team_id, match_date)
    )
    con.commit()
    con.close()
    print("Game successfully added!")

def previous_games():
    games = get_all_games()
    print("Previous games:")
    for game in games:
        if game[4] < datetime.now():
            print(f"{game[1]} vs {game[2]}, host: {game[3]}, date: {game[4]}")

def upcoming_games():
    games = get_all_games()
    print("Upcoming games:")
    for game in games:
        if game[4] >= datetime.now():
            print(f"{game[1]} vs {game[2]}, host: {game[3]}, date: {game[4]}")



while True:
    print("\nOpcije:")
    print("1. Zakazivanje nove utakmice")
    print("2. Prikaz prethodnih utakmica")
    print("3. Prikaz nadolazećih utakmica")
    print("4. Izlaz")

    choice = input("Izaberite opciju: ")

    if choice == "1":
        team_a = input("Unesite naziv Tima A: ")
        team_b = input("Unesite naziv Tima B: ")
        home_team = input("Koji tim je domaćin? (Tim A / Tim B): ")
        match_date = input("Unesite datum i vreme utakmice (YYYY-MM-DD HH:MM:SS): ")

        schedule_match(team_a, team_b, home_team, match_date)

    elif choice == "2":
        previous_games()
    elif choice == "3":
        upcoming_games()
    elif choice == "4":
        print("Izlaz iz programa.")
        break
    else:
        print("Nepoznata opcija. Pokušajte ponovo.")

























































































































































































def schedule_match(team_a, team_b, home_team, match_date):
    con = connect_to_database()
    cursor = con.cursor()

    # Dodaj timove ako ne postoje
    cursor.execute("SELECT id FROM teams WHERE name = %s", (team_a,))
    team_a_id = cursor.fetchone()
    if not team_a_id:
        cursor.execute("INSERT INTO teams (name) VALUES (%s)", (team_a,))
        con.commit()
        team_a_id = cursor.lastrowid
    else:
        team_a_id = team_a_id[0]

    cursor.execute("SELECT id FROM teams WHERE name = %s", (team_b,))
    team_b_id = cursor.fetchone()
    if not team_b_id:
        cursor.execute("INSERT INTO teams (name) VALUES (%s)", (team_b,))
        con.commit()
        team_b_id = cursor.lastrowid
    else:
        team_b_id = team_b_id[0]


home_team_id = team_a_id if home_team == "Tim A" else team_b_id

    cursor.execute(
        "INSERT INTO games (team_a_id, team_b_id, home_team_id, match_date) VALUES (%s, %s, %s, %s)",
        (team_a_id, team_b_id, home_team_id, match_date)
    )
    con.commit()
    con.close()
    print("Game successfully added!")

def previous_games():
    games = get_all_games()
    print("Previous games:")
    for game in games:
        if game[4] < datetime.now():
            print(f"{game[1]} vs {game[2]}, host: {game[3]}, date: {game[4]}")

def upcoming_games():
    games = get_all_games()
    print("Upcoming games:")
    for game in games:
        if game[4] >= datetime.now():
            print(f"{game[1]} vs {game[2]}, host: {game[3]}, date: {game[4]}")





















