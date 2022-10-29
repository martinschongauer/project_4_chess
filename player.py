"""
Chess Tournament Manager
OpenClassroom Project 4
Class implementing a player
"""

import re
import datetime
import view


class Player:

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.birth_day = 1
        self.birth_mon = 1
        self.birth_year = 1900
        self.sex = "M"
        self.rating = 0
        self.tournament_score = 0

    def complete_name(self) -> str:
        """Returns last_name first_name
        """

        return self.last_name + " " + self.first_name

    def is_player(self, first_name, last_name) -> bool:
        """Check whether this player bears a given name

        param first_name: first name
        param last_name: last name
        return: True or False
        """

        # Compare both names with the provided ones
        if self.first_name == first_name and self.last_name == last_name:
            return True

        return False

    def print_player(self) -> None:
        """Print infos about a player in the terminal

        return: None
        """

        view.print_player(self.first_name, self.last_name, self.birth_year, self.birth_mon, self.birth_day,
                          self.sex, self.rating, self.tournament_score)

        return

    def serialize_player(self) -> dict:
        """Turn player infos into a dictionary fitted for database purposes

        return: A dictionary containing player infos
        """

        # Translate everything in a dictionary
        serialized_player = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_day': self.birth_day,
            'birth_mon': self.birth_mon,
            'birth_year': self.birth_year,
            'sex': self.sex,
            'rating': self.rating,
            'tournament_score': self.tournament_score
        }

        return serialized_player

    @staticmethod
    def format_name(name: str) -> str:
        """Formats a given string as a name: only letters, single spaces, first letter for each word capitalized

        param name: Input name
        return: Formatted name
        """

        # First filter pass: eliminate forbidden characters (including hyphens) and excessive spaces
        pattern = re.compile(r'[^a-zA-Z\s]')
        filtered_name = re.sub(pattern, '', name)
        pattern = re.compile(r'\s+')
        filtered_name = re.sub(pattern, ' ', filtered_name).strip()

        # Enforce capital letters at beginning of "words" and remove them elsewhere
        filtered_name = filtered_name.lower()
        filtered_name = filtered_name.title()

        return filtered_name

    def set_first_name(self, name: str) -> bool:
        """Sets player first name (and filters it if not properly formatted)

        param self: This player
        param name: string containing the name: contains letters and hyphens
        return: True if name could be added (len < 25 or empty)
        """

        # Check size consistency
        if len(name) < 1 or len(name) > 25:
            print("First name length invalid")
            return False

        # Everything OK
        self.first_name = self.format_name(name)
        return True

    def set_last_name(self, name: str) -> bool:
        """Sets player last name (and filters it if not properly formatted)

        param self: This player
        param name: string containing the name: contains letters and hyphens
        return: True if name could be added (len < 25 or empty)
        """

        # Check size consistency
        if len(name) < 1 or len(name) > 25:
            print("Last name length invalid")
            return False

        # Everything OK
        self.last_name = self.format_name(name)
        return True

    def get_first_name(self) -> str:
        """Retrieve first name for this player

        return: string containing the first name
        """

        return self.first_name

    def get_last_name(self) -> str:
        """Retrieve last name for this player

        return: string containing the last name
        """

        return self.last_name

    def set_birthday(self, day: int, year: int, mon: int) -> bool:
        """Sets player birthday with basic consistency check

        param self: This player
        param day: 1-29, 30 or 31 depending on the month
        param year: between 1900 and 2015 to be reasonable, could be modified
        param mon: 1-12 of course
        return: True if valid birthday
        """

        # Check date validity
        if year < 1900 or year > 2015:
            print("Invalid year")
            return False

        try:
            new_date = datetime.datetime(year=year, month=mon, day=day)
        except ValueError:
            print("Invalid date")
            return False

        # Everything OK
        self.birth_day = new_date.day
        self.birth_mon = new_date.month
        self.birth_year = new_date.year

        return True

    def set_sex(self, sex: str) -> bool:
        """Sets player sex

        param self: This player
        param sex: "M" or "F"
        return: True if valid sex
        """

        if sex != "M" and sex != "F":
            print("Invalid sex")
            return False

        self.sex = sex
        return True

    def set_rating(self, rating: int) -> bool:
        """Sets player rating

        param self: This player
        param rating: positive number
        return: True if valid rating
        """

        if rating < 1:
            print("Invalid rating")
            return False

        self.rating = rating
        return True

    def set_tournament_score(self, tournament_score: float) -> bool:
        """Set player score for a tournament

        param self: This player
        param tournament_score: float value, > 0 and multiple of 0.5
        return: True if valid score
        """

        # Score must be positive
        if tournament_score < 0.0:
            return False

        # And a multiple of 0.5
        if not (tournament_score*2.0).is_integer():
            return False

        # It's OK, fill the field
        self.tournament_score = tournament_score

        return True

    def increase_tournament_score(self, points: float) -> bool:
        """Update player score during a tournament (+0.5, +1)

        param self: This player
        param points: 0, 1/2 or 1 to add
        return: True if valid score
        """

        if points != 0 and points != 0.5 and points != 1:
            print("Invalid score")
            return False

        self.tournament_score += points
        return True

    def get_rating(self) -> int:
        """Retrieve user rating - necessary for tournament organization, among others

        return: True if valid birthday
        """

        return self.rating

    def get_tournament_score(self) -> int:
        """Retrieve user tournament score - necessary for tournament organization, among others

        return: True if valid birthday
        """

        return self.tournament_score
