"""
Chess Tournament Manager
OpenClassroom Project 4
Function for the controller part of the MVC structure
Main loop of the whole program
"""

from tournament import Tournament
from player_list import PlayerList
import view
from tinydb import TinyDB
from tinydb import Query


# Create the list of players and the tournament as global variables
players = PlayerList()
tournament = Tournament()


def prompt_confirm(question: str) -> bool:
    """Print a question and prompt user for True/False answer

    return: yes/no
    """

    view.print_yes_no_question(question)
    answer = input("")
    if answer == "Y":
        return True
    else:
        return False


def prompt_for_str(prompt: str) -> str:
    """Print a question and prompt user for a string

    return: The string
    """

    view.print_prompt(prompt)

    return input("")


def prompt_for_int(prompt: str) -> int:
    """Print a question and prompt user for an integer

    return: The integer
    """

    # Check conversion errors
    while True:
        view.print_prompt(prompt)
        try:
            answer = input("")
            value = int(answer)
            break
        except ValueError:
            print("Error, integer value expected")

    return value


def prompt_for_int_in_range(prompt: str, min_val: int, max_val: int) -> int:
    """Print a question and prompt for an integer within some range

    return: The integer
    """

    # Check conversion errors
    while True:
        view.print_prompt_for_int_in_range(prompt, min_val, max_val)
        answer = input("")
        try:
            value = int(answer)
            if min_val <= value <= max_val:
                break
            else:
                print("Invalid integer range")
        except ValueError:
            print("Error, integer value expected")

    return value


def prompt_for_match_result() -> int:
    """Asks user to enter a result code for a match (0-3)

    return: 0 = not finished, 1 = white win, 2 = black win, 3 = equality
    """

    view.print_prompt_for_match_result()

    return prompt_for_int_in_range("", 0, 3)


def prompt_for_time_control() -> int:
    """Asks user to enter a result code for a time control (1-3)

    return: 1 = rapid, 2 = blitz, 3 = bullet
    """

    view.print_prompt_for_time_control()

    return prompt_for_int_in_range("", 1, 3)


def print_all_tournaments():
    """Print all tournaments listed in the database

    param tournament_name: name of the tournament
    param print_tournament: False = only return dictionary, no print
    return: None if not found, or the dictionary
    """

    # Open database
    db = TinyDB("ChessDB.json")
    table_tournament = db.table("table_tournament")

    if not table_tournament:
        print("table_tournament does not exist")
        return False

    # Loop and print
    for tour in table_tournament:
        view.print_tournament_infos(tour)

    # Close database
    db.close()

    return


def find_and_print_tournament(tour_name: str, print_tournament: bool) -> dict:
    """Returns a tournament or prints it

    param tournament_name: name of the tournament
    param print_tournament: False = only return dictionary, no print
    return: None if not found, or the dictionary
    """

    tournament_found = {}

    # Open database and find tournament
    db = TinyDB("ChessDB.json")
    table_tournament = db.table("table_tournament")

    if not table_tournament:
        print("table_tournament does not exist")
        return tournament_found

    # Search by tournament name
    for tour in table_tournament:
        if tour["name"] == tour_name:
            if print_tournament:
                view.print_tournament(tour)
            tournament_found = tour

    # Close database
    db.close()

    return tournament_found


def delete_tournament(tour_name: str) -> bool:
    """Delete a tournament in the database

    param tournament_name: its name
    return: True if it was found
    """

    # Open database and find tournament
    db = TinyDB("ChessDB.json")
    table_tournament = db.table("table_tournament")

    if not table_tournament:
        print("table_tournament does not exist")
        return False

    # Search/delete by tournament name
    my_query = Query()
    table_tournament.remove(my_query.name == tour_name)

    # Close database
    db.close()

    return True


def main_loop() -> None:
    """Program main loop: takes input commands and interprets them

    return: Nothing
    """

    # Welcome user and inform him about commands
    view.print_welcome()
    view.print_commands()

    while True:
        command = prompt_for_str("")
        execute_command(command)


def prompt_quit() -> None:
    """Prompts user to quit

    return: Nothing
    """

    if prompt_confirm("Unsaved data will be lost - quit anyway?"):
        quit()

    return


def add_player() -> None:
    """Prompts user for infos about a new player to add

    return: Nothing
    """

    first_name = prompt_for_str("Player First Name")
    last_name = prompt_for_str("Player Last Name")

    # Validity checks are done in the player class for most inputs, not here
    birth_day = prompt_for_int("Birth day")
    birth_mon = prompt_for_int_in_range("Birth month", 1, 12)
    birth_year = prompt_for_int_in_range("Birth year", 1900, 2015)
    sex = prompt_for_str("M for Male, F for Female")

    # Max rating = number of players once this one is added
    max_rating = players.get_number_of_players() + 1
    rating = prompt_for_int_in_range("Enter player rank", 1, max_rating)

    # Player will be added if all infos are consistant (except rating from now)
    if not players.add_player(first_name, last_name, birth_day, birth_mon,
                              birth_year, sex, max_rating + 1, 0.0, insertion_sort=True):
        print("Could not add player, check whether your inputs are valid")

    # Rating is patched afterwards (easier to implement this way)
    players.modify_player_rating(first_name, last_name, rating)

    return


def print_players() -> None:
    """Prints the list of players

    return: Nothing
    """

    sort_1 = prompt_for_int_in_range("Order in alphabetical order = 1 / ranking order = 2", 1, 2)
    players.print_list(sort_1, 1)

    return


def del_player() -> None:
    """Chose and delete a player in the list

    return: Nothing
    """

    first_name = prompt_for_str("Player First Name")
    last_name = prompt_for_str("Player Last Name")

    # Ask to confirm before deleting anything
    if prompt_confirm(f"Are you sure you want to delete player {first_name} {last_name}?"):
        if not players.remove_player(first_name, last_name, True):
            print("Could not remove player from list")

    return


def clear_players() -> None:
    """Clear the player list

    return: Nothing
    """

    if prompt_confirm("Are you sure you want to delete the whole player list?"):
        players.clean_list()

    return


def edit_first_name() -> None:
    """Edit player first name

    return: Nothing
    """

    first_name = prompt_for_str("Player First Name")
    last_name = prompt_for_str("Player Last Name")
    new_name = prompt_for_str("New First Name")
    players.modify_player_first_name(first_name, last_name, new_name)

    return


def edit_last_name() -> None:
    """Edit player last name

    return: Nothing
    """

    edit_last_name()
    first_name = prompt_for_str("Player First Name")
    last_name = prompt_for_str("Player Last Name")
    new_name = prompt_for_str("New Last Name")
    players.modify_player_last_name(first_name, last_name, new_name)

    return


def edit_sex() -> None:
    """Edit player sex

    return: Nothing
    """

    first_name = prompt_for_str("Player First Name")
    last_name = prompt_for_str("Player Last Name")
    new_sex = prompt_for_str("New Sex")
    players.modify_player_sex(first_name, last_name, new_sex)

    return


def edit_birthday() -> None:
    """Edit player birthday

    return: Nothing
    """

    first_name = prompt_for_str("Player First Name")
    last_name = prompt_for_str("Player Last Name")
    day = prompt_for_int("Player Birthday - New Day")
    mon = prompt_for_int_in_range("Player Birthday - New Mon", 1, 12)
    year = prompt_for_int_in_range("Player Birthday - New Year", 1900, 2015)
    players.modify_player_birthday(first_name, last_name, day, year, mon)

    return


def edit_rating() -> None:
    """Edit player birthday

    return: Nothing
    """

    first_name = prompt_for_str("Player First Name")
    last_name = prompt_for_str("Player Last Name")
    max_rating = players.get_number_of_players()
    rating = prompt_for_int_in_range("Enter player new rank", 1, max_rating)
    players.modify_player_rating(first_name, last_name, rating)

    return


def save_list() -> None:
    """Save player list in database

    return: Nothing
    """

    # Ask to confirm before overwriting database
    if prompt_confirm("This operation will overwrite the database on the hard drive. Are you sure?"):
        players.save_list()

    return


def load_list() -> None:
    """Load player list from database

    return: Nothing
    """

    # Ask to confirm before overwriting the whole list
    if prompt_confirm("This operation will overwrite the players in memory. Continue?"):
        players.load_list(insertion_sort=True)

    return


def tournament_add() -> None:
    """Add player to the current tournament

    return: Nothing
    """

    first_name = prompt_for_str("Player First Name")
    last_name = prompt_for_str("Player Last Name")

    # Find player in the list
    player_index = players.find_player_by_names(first_name, last_name)
    if player_index == -1:
        print("Cannot find player in the list")
        return

    # To add player to the tournament, extract a copy of the player's object from the list
    new_player = players.get_player(player_index)
    tournament.add_player(new_player)

    return


def db_tournament_del() -> None:
    """Delete tournament in database

    return: Nothing
    """

    tour_name = prompt_for_str("Tournament name")
    if prompt_confirm("This operation will permanently erase the tournament. Continue?"):
        delete_tournament(tour_name)

    return


def db_tournament_print() -> None:
    """Print tournament infos

    return: Nothing
    """

    tour_name = prompt_for_str("Tournament name")
    find_and_print_tournament(tour_name, True)

    return


def tournament_del() -> None:
    """Delete a user in current tournament

    return: Nothing
    """

    first_name = prompt_for_str("Player First Name")
    last_name = prompt_for_str("Player Last Name")

    if not tournament.remove_player(first_name, last_name):
        print("User was not found in this tournament")

    return


def tournament_location() -> None:
    """Set the location for the current tournament

    return: Nothing
    """

    tour_location = prompt_for_str("Tournament location")
    tournament.set_location(tour_location)

    return


def tournament_name() -> None:
    """Set the name for the current tournament

    return: Nothing
    """

    tour_name = prompt_for_str("Tournament name")

    if not find_and_print_tournament(tour_name, False):
        tournament.set_name(tour_name)
    else:
        print("Name already used for a previous tournament")

    return


def tournament_dates() -> None:
    """Set the start/end dates for the tournament

    return: Nothing
    """

    start_day = prompt_for_int("Tournament start date - Day")
    start_mon = prompt_for_int_in_range("Tournament start date - Mon", 1, 12)
    start_year = prompt_for_int_in_range("Tournament start date - Year", 1900, 2030)
    end_day = prompt_for_int("Tournament end date - Day")
    end_mon = prompt_for_int_in_range("Tournament end date - Mon", 1, 12)
    end_year = prompt_for_int_in_range("Tournament end date - Year", 1900, 2030)
    tournament.set_dates(start_day, start_mon, start_year, end_day, end_mon, end_year)

    return


def tournament_desc() -> None:
    """Set the description for the tournament

    return: Nothing
    """

    desc = prompt_for_str("Tournament description")
    tournament.set_description(desc)

    return


def tournament_time() -> None:
    """Set the time control for the tournament

    return: Nothing
    """

    time_val = prompt_for_time_control()
    tournament.set_time_control(time_val)

    return


def tournament_players() -> None:
    """Print the player list for the tournament

    return: Nothing
    """

    sort_1 = prompt_for_int_in_range("Order in alphabetical order = 1 / ranking order = 2", 1, 2)
    tournament.print_players(sort_1, 2)

    return


def tournament_save() -> None:
    """Save the current tournament

    return: Nothing
    """

    if prompt_confirm("This operation will overwrite the database on the hard drive. Are you sure?"):
        tournament.save_tournament()

    return


def tournament_clear() -> None:
    """Clear the current tournament

    return: Nothing
    """

    if prompt_confirm("Are you sure you want to delete any information related to this tournament?"):
        tournament.clear_tournament()

    return


def tournament_load() -> None:
    """Load the current tournament from database

    return: Nothing
    """

    if prompt_confirm("This operation will overwrite the tournament in memory. Continue?"):
        tour_name = prompt_for_str("Tournament name")
        serialized_tournament = find_and_print_tournament(tour_name, False)
        if not serialized_tournament:
            print("Could not find tournament")
        else:
            tournament.load_tournament(serialized_tournament)

    return


def match_result() -> None:
    """Set the result for a match

    return: Nothing
    """

    match_nbr = prompt_for_int("Enter match number")
    result_code = prompt_for_match_result()
    tournament.set_match_result(match_nbr, result_code)

    return


def process_edit_commands(command: str) -> None:
    """Execute commands starting with edit prefix

    param command: the command
    return: Nothing
    """

    # Edit an existing player's first name
    if command == "edit_first_name":
        edit_first_name()

    # Edit an existing player's last name
    elif command == "edit_last_name":
        edit_last_name()

    # Edit an existing player's last name
    elif command == "edit_sex":
        edit_sex()

    # Edit an existing player's last name
    elif command == "edit_birthday":
        edit_birthday()

    # Edit an existing player's last name
    elif command == "edit_rating":
        edit_rating()

    return


def process_player_commands(command: str) -> None:
    """Execute commands starting with player(s) prefix

    param command: the command
    return: Nothing
    """

    # Print all players
    if command == "players_print":
        print_players()

    # Add player
    elif command == "player_add":
        add_player()

    # Remove player
    elif command == "player_del":
        del_player()

    # Clear all players
    elif command == "players_clear":
        clear_players()

    # Save all players in the database
    elif command == "players_save":
        save_list()

    # Load all players from the database
    elif command == "players_load":
        load_list()

    return


def process_db_tournament_commands(command: str) -> None:
    """Execute commands starting with tournament prefix

    param command: the command
    return: Nothing
    """

    # Find a tournament by name and print its content
    if command == "db_tournament_print":
        db_tournament_print()

    # Print general infos about all tournaments in the database
    elif command == "db_tournament_print_all":
        print_all_tournaments()

    # Find a tournament by name and delete it
    elif command == "db_tournament_del":
        db_tournament_del()

    return


def process_tournament_commands(command: str) -> None:
    """Execute commands starting with tournament prefix

    param command: the command
    return: Nothing
    """

    # Self-explanatory commands - won't be all commented
    if command == "tournament_add":
        tournament_add()
    elif command == "tournament_del":
        tournament_del()
    elif command == "tournament_name":
        tournament_name()
    elif command == "tournament_location":
        tournament_location()
    elif command == "tournament_dates":
        tournament_dates()
    elif command == "tournament_desc":
        tournament_desc()
    elif command == "tournament_time":
        tournament_time()
    elif command == "tournament_print":
        tournament.print_tournament()
    elif command == "tournament_players":
        tournament_players()
    elif command == "tournament_start":
        tournament.start_tournament()
    elif command == "tournament_clear":
        tournament_clear()
    elif command == "tournament_save":
        tournament_save()
    elif command == "tournament_load":
        tournament_load()

    return


def process_round_commands(command: str) -> None:
    """Execute commands starting with round prefix

    param command: the command
    return: Nothing
    """

    # Print matches and their results for the ongoing round
    if command == "round_print":
        tournament.print_current_round()

    # Modify match results for the current round
    elif command == "round_match_result":
        match_result()

    # Finish this round and start next one
    elif command == "round_next":
        tournament.next_round()

    return


def execute_command(command: str) -> None:
    """Interprets a command entered by a user

    param command: the command
    return: Nothing
    """

    # Asking for help system
    if command == "help":
        view.print_commands()
        return

    # Asking to quit - user must confirm
    elif command == "quit":
        prompt_quit()
        return

    # Execute commands related to players
    if command.startswith("player"):
        process_player_commands(command)

    # Execute commands related to the edition of parameters
    elif command.startswith("edit"):
        process_edit_commands(command)

    # Execute commands related to tournaments
    elif command.startswith("tournament"):
        process_tournament_commands(command)

    # Execute commands related to tournaments in database
    elif command.startswith("db_tournament"):
        process_db_tournament_commands(command)

    # Execute commands related to tournaments in database
    elif command.startswith("round"):
        process_round_commands(command)

    # Default: unknown command
    else:
        print("Unknown command")

    return
