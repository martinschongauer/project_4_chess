"""
Chess Tournament Manager
OpenClassroom Project 4
Functions for the view part of the MVC structure
"""


def print_welcome() -> None:
    """Print welcome lines

    return: None
    """

    print("")
    print(" --------------------------------- ")
    print("  PYTHON CHESS TOURNAMENT MANAGER ")
    print(" --------------------------------- ")
    print("")

    return


def print_commands() -> None:
    """Print help system

    return: None
    """

    print("List of commands:")
    print("help: print this list of commands")
    print("quit: leave Python Chess Tournament Manager")
    print("players_print: prints the whole list of players and their infos")
    print("player_add: create a new player to add to the list")
    print("player_del: remove player from the list")
    print("players_clear: delete the whole list of players")
    print("players_save: saves the whole list of players with TinyDB")
    print("players_load: loads the whole list of players with TinyDB")
    print("edit_first_name: change first name for a player")
    print("edit_last_name: change last name for a player")
    print("edit_sex: change sex for a player")
    print("edit_birthday: change birth date for a player")
    print("edit_rating: change rank for a player")
    print("db_tournament_print: find and print a tournament in the database")
    print("db_tournament_print_all: list an print tournaments in the database")
    print("db_tournament_del: delete tournament in database")
    print("tournament_add: adds a player to the list of participants for the tournament")
    print("tournament_del: remove a player from the list of participants for the tournament")
    print("tournament_name: define name for the tournament")
    print("tournament_location: define name for the tournament")
    print("tournament_dates: set start/end dates for the tournament")
    print("tournament_desc: add general remarks/description to the tournament")
    print("tournament_time: rapid, blitz or bullet?")
    print("tournament_players: print tournament players")
    print("tournament_print: print tournament infos (previous rounds + sorted participants)")
    print("tournament_start: check if tournament is OK and launch first round")
    print("tournament_clear: deletes tournament infos and reinitialize everything")
    print("tournament_save: save tournament data in database")
    print("tournament_load: load tournament data from database")
    print("round_print: prints infos about current round (the four matches)")
    print("round_match_result: declares/overwrites results for an ongoing match")
    print("round_next: launch next round if all matches are finished for this one")

    return


def print_yes_no_question(question: str) -> None:
    """Print a question and prompt user for True/False answer

    return: Nothing
    """

    # Default answer will always be no (safer for delicate operations)
    print(f"{question} (Y/n): ", end="")

    return


def print_prompt(prompt: str) -> None:
    """Print a question and prompt user for an integer

    return: Nothing
    """

    # Check conversion errors
    print(f"{prompt} >> ", end="")

    return


def print_prompt_for_int_in_range(prompt: str, min_val: int, max_val: int) -> None:
    """Print a question and prompt for an integer within some range

    return: Nothing
    """

    print(f"{prompt} ({min_val}-{max_val}) >> ", end="")

    return


def print_prompt_for_match_result() -> None:
    """Asks user to enter a result code for a match (0-3)

    return: None
    """

    print("Please enter match result")
    print("0 = not finished")
    print("1 = white win")
    print("2 = black win")
    print("3 = equality")

    return


def print_prompt_for_time_control() -> None:
    """Asks user to enter a code for the time control (1-3)

    return: None
    """

    print("Please enter time control code")
    print("1 = rapid")
    print("2 = blitz")
    print("3 = bullet")

    return


def print_match(match: dict, i: int) -> None:
    """Prints well-formatted infos about a match contained in a dictionary

    return: None
    """

    print(f"MATCH {i} : {match['first_name_1']} {match['last_name_1']} - "
          f"{match['color_1']} - {match['score_1']} VS "
          f"{match['score_2']} - {match['color_2']} - "
          f"{match['first_name_2']} {match['last_name_2']}"
          )

    return


def print_player(first_name: str, last_name: str, birth_year: int, birth_mon: int, birth_day: int,
                 sex: str, rating: int, tournament_score: float) -> None:
    """Called by a Player object to print its content

    return: None
    """

    # Print everything with some spaces for visual comfort
    print(f"First name: {first_name}")
    print(f"Last name: {last_name}")
    print(f"{birth_year}/{birth_mon}/{birth_day}")
    if sex == "M":
        print("Male")
    else:
        print("Female")
    print(f"Rank: {rating}")
    print(f"Current tournament score: {tournament_score}")
    print("")

    return


def print_round(round_desc: dict):
    """Print content of a round

    return: Nothing
    """

    # Print general infos about the round
    print(f"\n{round_desc['round_name']}")
    if round_desc["round_started"]:
        print_datetime(round_desc["date_start"], "Round start date/time")
    else:
        print("Round did not start yet")
    if round_desc["round_finished"]:
        print_datetime(round_desc["date_stop"], "Round finished date/time")
    else:
        print("Round is not over")

    # Sweep through the list of matches...
    for i in range(len(round_desc["match_list"])):
        match = round_desc["match_list"][i]
        print_match(match, i)

    # Newline in the end
    print("")

    return True


def print_tournament_infos(tournament: dict) -> None:
    """Called to print general-purpose infos about a tournament

    param tournament: serialized tournament (dictionary)
    return: None
    """

    print(f"Tournament name: {tournament['name']}")
    print(f"Tournament description: {tournament['description']}")
    print(f"Tournament time control: {tournament['time_control']}")
    print(f"Tournament location: {tournament['location']}")
    print(f"Tournament start date: {tournament['start_date']}")
    print(f"Tournament end date: {tournament['end_date']}")

    if tournament['tournament_finished']:
        print("Tournament status: Finished\n")
    else:
        print("Tournament status: Not finished\n")

    return


def print_tournament(tournament: dict) -> None:
    """Called to print all infos about a tournament

    param tournament: serialized tournament (dictionary)
    return: None
    """

    # Print a header with general infos (name, etc...)
    print_tournament_infos(tournament)

    # Print players
    for player in tournament["players"]:
        print_player(player["first_name"], player["last_name"], player["birth_year"], player["birth_mon"],
                     player["birth_day"], player["sex"], player["rating"], player["tournament_score"])

    # Print previous rounds
    for round_desc in tournament["round_list"]:
        print_round(round_desc)

    # Current round
    print_round(tournament["current_round"])

    return


def print_datetime(date: str, prefix: str) -> None:
    """Print a nicely formatted date and time

    param date: string with the formatted date
    param prefix: string to be printed before the date
    return: Nothing
    """

    print(f"{prefix} : {date}")

    return
