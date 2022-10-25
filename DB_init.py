"""
Chess Tournament Manager
OpenClassroom Project 4
Sample codes to manipulate TinyDB
"""

from tinydb import TinyDB


def add_player(first_name: str, last_name: str, birth_day: int, birth_mon: int, birth_year: int,
               sex: str, rating: int, tournament_score: float, table):
    """Insert a player in the database - few error controls, for debug purposes only

    :return: Nothing
    """

    serialized_player = {
        'first_name': first_name,
        'last_name': last_name,
        'birth_day': birth_day,
        'birth_mon': birth_mon,
        'birth_year': birth_year,
        'sex': sex,
        'rating': rating,
        'tournament_score': tournament_score
    }

    table.insert(serialized_player)

    return


def add_test_players():
    """Create a list of 8 players to test the database

    :return: Nothing
    """

    # Open database
    db = TinyDB("ChessDB.json")
    table_players = db.table("table_players")

    add_player("A", "B", 1, 5, 1968, "M", 2, 0.0, table_players)
    add_player("C", "D", 12, 2, 1992, "F", 3, 0.0, table_players)
    add_player("E", "F", 17, 6, 1997, "M", 5, 0.0, table_players)
    add_player("G", "H", 21, 12, 1984, "F", 8, 0.0, table_players)
    add_player("I", "J", 3, 11, 1975, "M", 7, 0.0, table_players)
    add_player("K", "L", 5, 9, 2002, "F", 1, 0.0, table_players)
    add_player("M", "N", 29, 11, 1962, "M", 4, 0.0, table_players)
    add_player("O", "P", 4, 8, 1972, "F", 6, 0.0, table_players)

    # Close database
    db.close()

    return


def create_tables():
    """Create output DB with two tables

    :return: Nothing
    """

    # Open database
    db = TinyDB("ChessDB.json")

    # Drop existing table to clean everything
    db.drop_table("table_tournaments")
    db.drop_table("table_players")

    # Create fresh tables
    db.table("table_tournaments")
    db.table("table_players")

    # Close database
    db.close()

    return
