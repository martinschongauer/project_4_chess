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
        answer = input(f"")
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
    for tournament in table_tournament:
        view.print_tournament_infos(tournament)

    # Close database
    db.close()

    return


def find_and_print_tournament(tournament_name: str, print_tournament: bool) -> dict:
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
    for tournament in table_tournament:
        if tournament["name"] == tournament_name:
            if print_tournament:
                view.print_tournament(tournament)
            tournament_found = tournament

    # Close database
    db.close()

    return tournament_found


def delete_tournament(tournament_name: str) -> bool:
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
    table_tournament.remove(my_query.name == tournament_name)

    # Close database
    db.close()

    return True


def main_loop() -> None:
    """Program main loop: takes input commands and interprets them

    return: Nothing
    """

    # Create the list of players and the tournament we are going to work with
    players = PlayerList()
    tournament = Tournament()

    # Welcome user and inform him about commands
    view.print_welcome()
    view.print_commands()

    # DEBUG: configure a tournament for the tests
    players.load_list(insertion_sort=True)
    tournament.set_name("my_first_tournament")
    tournament.set_location("Paris")
    tournament.set_dates(10, 10, 2022, 11, 10, 2022)
    tournament.set_description("tournament created for debug purposes")
    tournament.set_time_control(2)

    for i in range(8):
        new_player = players.get_player(i)
        tournament.add_player(new_player)

    while True:
        command = prompt_for_str("")

        # Asking for help system
        if command == "help":
            view.print_commands()

        # Asking to quit - user must confirm
        elif command == "quit":
            if prompt_confirm("Unsaved data will be lost - quit anyway?"):
                break

        # Print all players
        elif command == "print_players":
            sort_1 = prompt_for_int_in_range("Order in alphabetical order = 1 / ranking order = 2", 1, 2)
            players.print_list(sort_1, 1)

        # Add player
        elif command == "add_player":
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
                                      birth_year, sex, max_rating+1, 0.0, insertion_sort=True):
                print("Could not add player, check whether your inputs are valid")

            # Rating is patched afterwards (easier to implement this way)
            players.modify_player_rating(first_name, last_name, rating)

        # Remove player
        elif command == "del_player":
            first_name = prompt_for_str("Player First Name")
            last_name = prompt_for_str("Player Last Name")

            # Ask to confirm before deleting anything
            if prompt_confirm(f"Are you sure you want to delete player {first_name} {last_name}?"):
                if not players.remove_player(first_name, last_name, True):
                    print("Could not remove player from list")

        # Clear all players
        elif command == "clear_players":
            # Confirm before such a delicate operation
            if prompt_confirm(f"Are you sure you want to delete the whole player list?"):
                players.clean_list()

        # Edit an existing player's first name
        elif command == "edit_first_name":
            first_name = prompt_for_str("Player First Name")
            last_name = prompt_for_str("Player Last Name")
            new_name = prompt_for_str("New First Name")
            players.modify_player_first_name(first_name, last_name, new_name)

        # Edit an existing player's last name
        elif command == "edit_last_name":
            first_name = prompt_for_str("Player First Name")
            last_name = prompt_for_str("Player Last Name")
            new_name = prompt_for_str("New Last Name")
            players.modify_player_last_name(first_name, last_name, new_name)

        # Edit an existing player's last name
        elif command == "edit_sex":
            first_name = prompt_for_str("Player First Name")
            last_name = prompt_for_str("Player Last Name")
            new_sex = prompt_for_str("New Sex")
            players.modify_player_sex(first_name, last_name, new_sex)

        # Edit an existing player's last name
        elif command == "edit_birthday":
            first_name = prompt_for_str("Player First Name")
            last_name = prompt_for_str("Player Last Name")
            day = prompt_for_int("Player Birthday - New Day")
            mon = prompt_for_int_in_range("Player Birthday - New Mon", 1, 12)
            year = prompt_for_int_in_range("Player Birthday - New Year", 1900, 2015)
            players.modify_player_birthday(first_name, last_name, day, year, mon)

        # Edit an existing player's last name
        elif command == "edit_rating":
            first_name = prompt_for_str("Player First Name")
            last_name = prompt_for_str("Player Last Name")
            max_rating = players.get_number_of_players()
            rating = prompt_for_int_in_range("Enter player new rank", 1, max_rating)
            players.modify_player_rating(first_name, last_name, rating)

        # Save all players in the database
        elif command == "save_list":
            # Ask to confirm before overwriting database
            if prompt_confirm(f"This operation will overwrite the database on the hard drive. Are you sure?"):
                players.save_list()

        # Load all players from the database
        elif command == "load_list":
            # Ask to confirm before overwriting the whole list
            if prompt_confirm(f"This operation will overwrite the players in memory. Continue?"):
                players.load_list(insertion_sort=True)

        # Add a player from the list to the tournament
        elif command == "tournament_add":
            first_name = prompt_for_str("Player First Name")
            last_name = prompt_for_str("Player Last Name")

            # Find player in the list
            player_index = players.find_player_by_names(first_name, last_name)
            if player_index == -1:
                print("Cannot find player in the list")
                continue

            # To add player to the tournament, extract a copy of the player's object from the list
            new_player = players.get_player(player_index)
            tournament.add_player(new_player)

        # Remove a player from the tournament
        elif command == "tournament_del":
            first_name = prompt_for_str("Player First Name")
            last_name = prompt_for_str("Player Last Name")
            if not tournament.remove_player(first_name, last_name):
                print("User was not found in this tournament")

        # Find a tournament by name and print its content
        elif command == "db_tournament_print":
            tournament_name = prompt_for_str("Tournament name")
            find_and_print_tournament(tournament_name, True)

        # Print general infos about all tournaments in the database
        elif command == "db_tournament_print_all":
            print_all_tournaments()

        # Find a tournament by name and delete it
        elif command == "db_tournament_del":
            tournament_name = prompt_for_str("Tournament name")
            delete_tournament(tournament_name)

        # Add tournament name (if name is not already used for a previous tournament)
        elif command == "tournament_name":
            tournament_name = prompt_for_str("Tournament name")
            if not find_and_print_tournament(tournament_name, False):
                tournament.set_name(tournament_name)
            else:
                print("Name already used for a previous tournament")

        # Add tournament location
        elif command == "tournament_location":
            tournament_location = prompt_for_str("Tournament location")
            tournament.set_location(tournament_location)

        # Add tournament dates
        elif command == "tournament_dates":
            start_day = prompt_for_int("Tournament start date - Day")
            start_mon = prompt_for_int_in_range("Tournament start date - Mon", 1, 12)
            start_year = prompt_for_int_in_range("Tournament start date - Year", 1900, 2030)
            end_day = prompt_for_int("Tournament end date - Day")
            end_mon = prompt_for_int_in_range("Tournament end date - Mon", 1, 12)
            end_year = prompt_for_int_in_range("Tournament end date - Year", 1900, 2030)
            tournament.set_dates(start_day, start_mon, start_year, end_day, end_mon, end_year)

        # Add tournament description
        elif command == "tournament_desc":
            desc = prompt_for_str("Tournament description")
            tournament.set_description(desc)

        # Add tournament time control
        elif command == "tournament_time":
            time_val = prompt_for_time_control()
            tournament.set_time_control(time_val)

        # Print all tournament infos
        elif command == "tournament_print":
            tournament.print_tournament()

        # Print all players (always reorder in rank order after printing)
        elif command == "tournament_players":
            sort_1 = prompt_for_int_in_range("Order in alphabetical order = 1 / ranking order = 2", 1, 2)
            tournament.print_players(sort_1, 2)

        # Start tournament
        elif command == "tournament_start":
            tournament.start_tournament()

        # Clear the whole tournament
        elif command == "tournament_clear":
            if prompt_confirm(f"Are you sure you want to delete any information related to this tournament?"):
                tournament.clear_tournament()

        # Save tournament infos
        elif command == "tournament_save":
            if prompt_confirm(f"This operation will overwrite the database on the hard drive. Are you sure?"):
                tournament.save_tournament()

        # Load tournament infos
        elif command == "tournament_load":
            if prompt_confirm(f"This operation will overwrite the tournament in memory. Continue?"):
                tournament_name = prompt_for_str("Tournament name")
                serialized_tournament = find_and_print_tournament(tournament_name, False)
                if not serialized_tournament:
                    print("Could not find tournament")
                else:
                    tournament.load_tournament(serialized_tournament)

        # Remove tournament infos from database
        elif command == "tournament_remove":
            if prompt_confirm(f"This operation will permanently erase the tournament. Continue?"):
                tournament_name = prompt_for_str("Tournament name")
                delete_tournament(tournament_name)

        # Print matches and their results for the ongoing round
        elif command == "round_print":
            tournament.print_current_round()

        # Modify match results for the current round
        elif command == "match_result":
            match_nbr = prompt_for_int("Enter match number")
            result_code = prompt_for_match_result()
            tournament.set_match_result(match_nbr, result_code)

        # Finish this round and start next one
        elif command == "round_next":
            tournament.next_round()

        # Default: unknown command
        else:
            print("Unknown command")

    # End of loop
    return
