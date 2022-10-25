"""
Chess Tournament Manager
OpenClassroom Project 4
Class implementing a round (4 rounds = 1 tournament)
"""

import random
import datetime
import copy


class Round:

    def __init__(self):
        self.round_name = ""
        self.match_list = []
        self.date_start = "None"
        self.date_stop = "None"
        self.round_started = False
        self.round_finished = False

    def set_name(self, name: str) -> bool:
        """Set the name for a round

        param name: the name for this round
        return: always True
        """

        self.round_name = name
        return True

    def get_name(self) -> str:
        """Retrieve the name of this round

        return: string containing the name
        """

        return self.round_name

    def player_already_busy(self, first_name: str, last_name: str) -> bool:
        """Check whether a player took part to a match in this round

        param first_name: player first name
        param last_name: player last name
        return: True if player was found
        """

        # Loop over the list of matches
        for i in range(len(self.match_list)):
            match = self.match_list[i]
            if (match["first_name_1"] == first_name and match["last_name_1"] == last_name) or \
                    (match["first_name_2"] == first_name and match["last_name_2"] == last_name):
                return True

        return False

    def add_match(self, first_name_1, first_name_2, last_name_1, last_name_2) -> bool:
        """Add a new match between two players (chose colors randomly)

        param first_name_1: first name for the first player
        param first_name_2: first name for the second player
        param last_name_1: last name for the first player
        param last_name_2: last name for the second player
        return: True if OK, False if match already exists
        """

        # Chose who will be player 1 (white) vs 2 (black)
        random_0_1 = random.randint(0, 1)
        match = {
            "color_1": "white",
            "color_2": "black",
            "score_1": 0,
            "score_2": 0
        }

        # Add names as white or black, depending on the random value
        if random_0_1 == 0:
            match["first_name_1"] = first_name_1
            match["first_name_2"] = first_name_2
            match["last_name_1"] = last_name_1
            match["last_name_2"] = last_name_2
        else:
            match["first_name_1"] = first_name_2
            match["first_name_2"] = first_name_1
            match["last_name_1"] = last_name_2
            match["last_name_2"] = last_name_1

        # Done, add to list and return
        self.match_list.append(match)
        return True

    def clear_round(self) -> bool:
        """Clear match list

        return: Always True
        """

        self.round_name = ""
        self.match_list = []
        self.date_start = "None"
        self.date_stop = "None"
        self.round_started = False
        self.round_finished = False
        self.match_list.clear()

        return True

    def is_round_over(self) -> bool:
        """Check whether round is over (all matches have non-zero scores)

        return: True/False
        """

        # Sweep through list and look for a single match still not finished
        for match in self.match_list:
            if match['score_1'] + match['score_2'] == 0:
                return False

        return True

    def record_start_time(self) -> None:
        """Get datetime for the round start

         return: Nothing
         """

        datetime_start = datetime.datetime.now()
        self.date_start = datetime_start.strftime(f"%H:%M:%S on %A, %B the %dth, %Y")
        self.round_started = True

        return

    def record_stop_time(self) -> None:
        """Get datetime for the round stop

        return: Nothing
        """

        datetime_stop = datetime.datetime.now()
        self.date_stop = datetime_stop.strftime(f"%H:%M:%S on %A, %B the %dth, %Y")
        self.round_finished = True

        return

    def get_match(self, match_index: int) -> dict:
        """Print

        param match_index: which match to modify in the table
        return: True if OK - False = out-of-range index or invalid score (win, lose or equality)
        """

        return self.match_list[match_index]

    def set_match_result(self, match_index: int, score_1: float, score_2: float) -> bool:
        """Modify match results

        param match_index: which match to modify in the table
        return: True if OK - False = out-of-range index or invalid score (win, lose or equality)
        """

        # Check consistency
        if match_index < 0 or match_index >= len(self.match_list):
            print("Invalid index in match list")
            return False

        # Scores = 0, 1/2 ou 1 et leur somme vaut 0 (match en cours) ou 1 (victoire - match nul)
        if (score_1 != 0 and score_1 != 1/2 and score_1 != 1) or \
                (score_2 != 0 and score_2 != 1 / 2 and score_2 != 1) or \
                (score_2 + score_1 != 0 and score_2 + score_1 != 1):
            print("Invalid scores")
            return False

        # Update
        self.match_list[match_index]["score_1"] = score_1
        self.match_list[match_index]["score_2"] = score_2

        return True

    def serialize_round(self) -> dict:
        """Save round in a database

        return: Dictionary containing a round description
        """

        # Serialization of data
        serialized_round = {
            'round_name': self.round_name,
            'date_start': self.date_start,
            'date_stop': self.date_stop,
            'round_started': self.round_started,
            'round_finished': self.round_finished,
            'match_list': copy.deepcopy(self.match_list)
        }

        return serialized_round

    def load_round(self, serialized_round: dict) -> bool:
        """Load round from a database document

        param serialized_round: dictionary representing the round
        return: True if no I/O exception was caught
        """

        self.round_name = serialized_round["round_name"]
        self.date_start = serialized_round["date_start"]
        self.date_stop = serialized_round["date_stop"]
        self.round_started = serialized_round["round_started"]
        self.round_finished = serialized_round["round_finished"]

        # Start with a new clean list of matches and add them one by one
        self.match_list.clear()
        for match in serialized_round["match_list"]:
            self.match_list.append(match)

        return True
