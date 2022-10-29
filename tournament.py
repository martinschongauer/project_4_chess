"""
Chess Tournament Manager
OpenClassroom Project 4
Class implementing a tournament - following swiss-type rules
"""

from round import Round
from player_list import PlayerList
from player import Player
import view
from tinydb import TinyDB
from tinydb import Query
import copy
import re
import datetime


class Tournament:

    def __init__(self):
        self.players = PlayerList()
        self.current_round = Round()
        self.previous_rounds = []
        self.round_number = 0
        self.max_round = 4
        self.tournament_finished = False
        self.tournament_started = False
        self.time_control = ""
        self.description = ""
        self.name = ""
        self.location = ""
        self.start_date = ""
        self.end_date = ""

    def set_dates(self, start_day: int, start_mon: int, start_year: int,
                  end_day: int, end_mon: int, end_year: int):
        """Sets the start/stop dates for a tournament

        param name: alphanumeric characters + spaces only
        return: False if invalid/incoherent dates
        """

        # Create dates and check validity
        try:
            start_datetime = datetime.datetime(year=start_year, month=start_mon, day=start_day)
            end_datetime = datetime.datetime(year=end_year, month=end_mon, day=end_day)
        except ValueError:
            print("Invalid dates")
            return False

        # Check whether the end date comes after the start date
        if start_datetime.date() > end_datetime.date():
            print("End date must come after start date")
            return False

        # Convert dates in readable format to store them
        self.start_date = start_datetime.strftime("%A, %B the %dth, %Y")
        self.end_date = end_datetime.strftime("%A, %B the %dth, %Y")

        return True

    def set_name(self, name: str):
        """Sets the name of the tournament (<= 25 characters)

        param name: alphanumeric characters + spaces only
        return: False if too long
        """

        # Validity check
        if len(name) > 25:
            print("Tournament name must be 25 characters long at most")
            return False

        pattern = re.compile(r'[^a-zA-Z0-9\s]')
        self.name = re.sub(pattern, '', name)

        return True

    def set_location(self, location: str):
        """Sets the location of the tournament (<= 50 characters)

        return: False if too long
        """

        # Validity check
        if len(location) > 50:
            print("Tournament location must be 50 characters long at most")
            return False

        self.location = location

        return True

    def set_time_control(self, time_control: int) -> bool:
        """Sets the type of time control

        param time_control: 1 = "rapid" / 2 = "blitz" / 3 = "bullet"
        return: False if unknown time_control
        """

        # Test allowed values and translate them
        if time_control == 1:
            self.time_control = "rapid"
        elif time_control == 2:
            self.time_control = "blitz"
        elif time_control == 3:
            self.time_control = "bullet"
        else:
            print("Unknown time control value")
            return False

        return True

    def set_description(self, description: str) -> bool:
        """Sets the description for the tournament

        param time_control:
        return: Always True
        """

        self.description = description

        return True

    def clear_rounds(self) -> bool:
        """Clean all data related to rounds

        return: always True
        """

        # Delete current round
        self.current_round.clear_round()

        # Empty list of played rounds
        self.previous_rounds.clear()

        return True

    def clear_tournament(self) -> bool:
        """Clear all variables to start with a brand-new tournament

        return: always True
        """

        self.description = ""
        self.time_control = ""
        self.name = ""
        self.location = ""
        self.start_date = ""
        self.end_date = ""

        self.players.clean_list()
        self.round_number = 0
        self.tournament_finished = False
        self.tournament_started = False
        self.clear_rounds()

        return True

    def add_player(self, new_player: Player) -> bool:
        """Clear all variables to start with a brand-new tournament

        return: True if successfully added to the list
        """

        return self.players.add_player(new_player.first_name, new_player.last_name, new_player.birth_day,
                                       new_player.birth_mon, new_player.birth_year, new_player.sex, new_player.rating,
                                       0.0, insertion_sort=True)

    def remove_player(self, first_name: str, last_name: str) -> bool:
        """Finds a player by name and remove it from the tournament

        return: True if found and removed, False if he was not there anyway
        """

        self.players.remove_player(first_name, last_name, False)
        return True

    def start_tournament(self) -> bool:
        """Check if all infos are valid to start a tournament -> launch round 1

        return: True if the tournament started
        """

        # Mandatory number of players = 8
        if self.players.get_number_of_players() != 8:
            print("There must be 8 players for a tournament")
            return False

        # A name must be defined
        if not self.name:
            print("The name field for the tournament must not be empty")
            return False

        # Tournament general description field should contain something
        if not self.description:
            print("The description field for the tournament must not be empty")
            return False

        # Tournament location...
        if not self.location:
            print("The location field for the tournament must not be empty")
            return False

        # And finally dates
        if not self.start_date or not self.end_date:
            print("The start/end date fields for the tournament must not be empty")
            return False

        # Tournament time control
        if not self.time_control:
            print("The time control field for the tournament must be specified")
            return False

        # Set these flags
        self.tournament_finished = False
        self.tournament_started = True

        # New rounds
        self.clear_rounds()
        self.round_number = 1

        # New scores -> 0 for everybody + sort players (by rating) for the first round
        self.players.reset_scores()
        self.players.sort_list()

        # Name round, create match list, record launch time and print everything
        self.create_match_list()
        self.current_round.set_name("Round 1")

        # New round can start now
        self.current_round.record_start_time()

        # Inform user and return
        self.print_current_round()
        print("First round started!")
        return True

    def print_players(self, sort_1: int, sort_2: int) -> None:
        """Print the list of players for this tournament

        param sort_1: print in : 1 = alphabetical order / 2 = rank order
        param sort_2: reorder list before leaving (same codes as sort_1)
        return: Nothing
        """

        self.players.print_list(sort_1, sort_2)

        return

    def print_tournament(self) -> None:
        """Print a summary of all round results for this tournament

        return: Nothing
        """

        # Make sure that the tournament is started/validated for this operation
        if not self.tournament_started:
            print("Cannot print tournament if it did not start yet")
            return None

        # Serialize and call view
        serialized_tournament = self.serialize_tournament()
        view.print_tournament(serialized_tournament)

        return

    def next_round(self) -> bool:
        """Get ready for next round (print matches, store previous round...)

        return: False if some matches in this round are not over yet
        """

        # Make sure that the tournament is started/validated for this operation
        if not self.tournament_started:
            print("Cannot go to next round if the tournament did not start yet")
            return False

        if not self.current_round.is_round_over():
            print("Round is not over")
            return False

        # Tournament already over, just print all results (and give the final ratings)
        if self.tournament_finished:
            self.print_tournament()
            return True

        # We can mark this round as finished now and print its results
        self.current_round.record_stop_time()
        print("Round finished - Results:")
        self.print_current_round()

        # Update total scores in player list...
        for match in self.current_round.match_list:
            first_name_1 = match["first_name_1"]
            first_name_2 = match["first_name_2"]
            last_name_1 = match["last_name_1"]
            last_name_2 = match["last_name_2"]
            score_1 = match["score_1"]
            score_2 = match["score_2"]
            self.players.update_player_score(first_name_1, last_name_1, score_1)
            self.players.update_player_score(first_name_2, last_name_2, score_2)

        # And sort the players according to the new results
        self.players.sort_list()

        # Is the tournament finished?
        if self.round_number == self.max_round:
            self.tournament_finished = True
            print("Tournament is over!")
            return True

        # If tournament is not finished, keep a copy of this round
        round_desc = self.current_round.serialize_round()
        self.previous_rounds.append(round_desc)

        # Start with a fresh new current round object
        self.round_number += 1
        self.current_round.clear_round()

        # Generate a new list of matches according to the two new subgroups
        self.create_match_list()
        self.current_round.set_name(f"Round {self.round_number}")

        # New round can start now
        self.current_round.record_start_time()

        # Inform user and return
        print("New round:")
        self.print_current_round()
        return True

    def print_current_round(self) -> None:
        """Print ongoing matches and results

        return: None
        """

        # Make sure that the tournament is started/validated for this operation
        if not self.tournament_started:
            print("Cannot print round if the tournament did not start yet")
            return None

        serialize_round = self.current_round.serialize_round()
        view.print_round(serialize_round)

        return

    def match_already_played(self, first_name_1: str, first_name_2: str, last_name_1: str, last_name_2: str) -> bool:
        """Explores previous rounds to determine if a given match was already played

        param first_name_1: player 1 first name
        param first_name_2: player 2 first name
        param last_name_1: player 1 last name
        param last_name_2: player 2 last name
        return: True if the match has already been played
        """

        # Explore all previous rounds...
        for prev_round in self.previous_rounds:
            # Loop over the list of matches
            for match in prev_round["match_list"]:
                if (match["first_name_1"] == first_name_1 and match["first_name_2"] == first_name_2
                    and match["last_name_1"] == last_name_1 and match["last_name_2"] == last_name_2) or \
                    (match["first_name_1"] == first_name_2 and match["first_name_2"] == first_name_1
                     and match["last_name_1"] == last_name_2 and match["last_name_2"] == last_name_1):
                    return True

        # If we arrived here, the match was not found
        return False

    def create_match_list(self) -> bool:
        """Associate players in both groups to create four matches

        return: Always true in this version
        """

        # Now we can associate players with each others
        for i in range(0, 4, 1):
            first_name_1 = self.players.get_player(i).get_first_name()
            last_name_1 = self.players.get_player(i).get_last_name()

            # Store names for the first possible match we will encounter
            free_first_name_2 = ""
            free_last_name_2 = ""

            for j in range(4, 8, 1):
                first_name_2 = self.players.get_player(j).get_first_name()
                last_name_2 = self.players.get_player(j).get_last_name()

                # Skip if player 2 was already selected for a match during a previous iteration
                if not self.current_round.player_already_busy(first_name_2, last_name_2):
                    # Store the first possible match, in any case
                    if not free_first_name_2:
                        free_first_name_2 = first_name_2
                        free_last_name_2 = last_name_2

                    # We found a match that was not played yet
                    if not self.match_already_played(first_name_1, first_name_2, last_name_1, last_name_2):
                        self.current_round.add_match(first_name_1, first_name_2, last_name_1, last_name_2)
                        break

                # All combinations unsuccessfully tried - take first possibility by default
                if j == 7:
                    self.current_round.add_match(first_name_1, free_first_name_2, last_name_1, free_last_name_2)

        return True

    def set_match_result(self, match_index: int, result_code: int):
        """Set match result (for the current round)

        param match_index: 1-4 (Visible in the list printed in the terminal)
        param result_code: 0-3 (nothing, victory white, victory black, equality)
        return: False if index or code is invalid
        """

        # Make sure that the tournament is started/validated for this operation
        if not self.tournament_started:
            print("Cannot set match result if the tournament did not start yet")
            return None

        # Translate result_code into scores
        if result_code == 0:
            score_1 = 0
            score_2 = 0
        elif result_code == 1:
            score_1 = 1
            score_2 = 0
        elif result_code == 2:
            score_1 = 0
            score_2 = 1
        elif result_code == 3:
            score_1 = 0.5
            score_2 = 0.5
        else:
            print("Invalid result code")
            return False

        return self.current_round.set_match_result(match_index, score_1, score_2)

    def save_tournament(self) -> bool:
        """Saves all tournament data in TinyDB

        return: False if something went wrong
        """

        # Make sure that the tournament is started/validated for this operation
        if not self.tournament_started:
            print("Cannot save if the tournament did not start yet")
            return False

        # If tournament was not launched, save impossible (safer approach)
        if self.round_number == 0:
            print("Cannot save tournament, first round must be launched")
            return False

        # Get infos to store
        serialized_tournament = self.serialize_tournament()

        # Open table in database
        db = TinyDB("ChessDB.json")
        table_tournaments = db.table("table_tournament")

        # Search/delete by tournament name
        my_query = Query()
        table_tournaments.remove(my_query.name == self.name)

        # Overwrite infos
        table_tournaments.insert(serialized_tournament)

        # Close the database
        db.close()

        return True

    def load_tournament(self, serialized_tournament: dict) -> bool:
        """Loads all tournament data from TinyDB

        return: False if something went wrong
        """

        # Database OK, we can safely clean the tournament to overwrite its content
        self.clear_tournament()

        # Retrieve general informations
        self.name = serialized_tournament["name"]
        self.description = serialized_tournament["description"]
        self.round_number = serialized_tournament["round_number"]
        self.max_round = serialized_tournament["max_round"]
        self.time_control = serialized_tournament["time_control"]
        self.location = serialized_tournament["location"]
        self.start_date = serialized_tournament["start_date"]
        self.end_date = serialized_tournament["end_date"]
        self.tournament_finished = serialized_tournament["tournament_finished"]

        # Load current round
        self.current_round.set_name(f"Round {self.round_number}")
        self.current_round.load_round(serialized_tournament["current_round"])

        # Copy the list of finished rounds
        self.previous_rounds = copy.deepcopy(serialized_tournament["round_list"])

        # Load the list of participants from the dedicated table
        for player in serialized_tournament["players"]:
            self.players.add_player(first_name=player['first_name'],
                                    last_name=player['last_name'],
                                    birth_day=player['birth_day'],
                                    birth_mon=player['birth_mon'],
                                    birth_year=player['birth_year'],
                                    sex=player['sex'],
                                    rating=player['rating'],
                                    tournament_score=player['tournament_score'],
                                    insertion_sort=True)

        # This flag is always on for saved tournaments (don't need to save it)
        self.tournament_started = True

        return True

    def serialize_tournament(self) -> dict:
        """Returns a serialized object containing the whole description for a tournament

        return: Dictionary
        """

        # Make sure that the tournament is started/validated for this operation
        if not self.tournament_started:
            print("Cannot serialize if the tournament did not start yet")
            return {}

        # Prepare previous rounds and current round
        round_list = copy.deepcopy(self.previous_rounds)
        current_round_serialized = self.current_round.serialize_round()

        # Create the list of players
        tournament_players = []
        for i in range(8):
            player = self.players.get_player(i)
            serialized_player = player.serialize_player()
            tournament_players.append(serialized_player)

        serialized_tournament = {
            'name': self.name,
            'location': self.location,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'round_number': self.round_number,
            'max_round': self.max_round,
            'time_control': self.time_control,
            'description': self.description,
            'tournament_finished': self.tournament_finished,
            'round_list': round_list,
            'current_round': current_round_serialized,
            'players': tournament_players
        }

        return serialized_tournament
