"""
Chess Tournament Manager
OpenClassroom Project 4
Class implementing a player list (8 for a tournament, but undefined number in general)
"""

from player import Player
from tinydb import TinyDB
import copy


class PlayerList:

    def __init__(self):
        self.players = []

    def get_number_of_players(self) -> int:
        """Returns the number of players in the list

        return: integer value, potentially 0
        """

        return len(self.players)

    def clean_list(self) -> bool:
        """Delete all players in the list

        return: True in any case
        """

        # Sweep through the list
        while self.get_number_of_players() != 0:
            del self.players[0]

        return True

    def print_list(self, sort_1: int, sort_2: int) -> bool:
        """Print all players in the list in a readable format

        param sort_1: print in : 1 = alphabetical order / 2 = rank order
        param sort_2: reorder list before leaving (same codes as sort_1)
        return: True in any case
        """

        # Sort in alphabetical order before printing?
        if sort_1 == 1:
            self.sort_list_alpha()
        else:
            self.sort_list()

        # Print list elements one by one
        for player in self.players:
            player.print_player()

        # Sort before leaving
        if sort_2 == 1:
            self.sort_list_alpha()
        else:
            self.sort_list()

        return True

    def reset_scores(self) -> bool:
        """Initialize all player scores to 0

        return: True in any case
        """
        for player in self.players:
            player.tournament_score = 0

        return True

    def save_list(self) -> bool:
        """Save players in a database

        param db_name: name for output file
        param table_name: name for the table where data are stored
        return: True in any case in this version
        """

        # Open database and reset the table of tables
        db = TinyDB("ChessDB.json")
        table = db.table("table_players")
        table.truncate()

        # Serialize and add players one by one
        for player in self.players:
            serialized_player = player.serialize_player()
            table.insert(serialized_player)

        # Done
        db.close()
        return True

    def load_list(self, insertion_sort: bool) -> bool:
        """Load players from database

        param db_name: name for output file
        param table_name: name for the table where data are stored
        param insertion_sort: do we sort players by alphabetical order?
        return: True if no I/O exception was caught
        """

        # Open database and test I/O error (or empty database)
        db = TinyDB("ChessDB.json")
        serialized_players = db.table("table_players")
        if not serialized_players:
            print("Could not load players in database")
            return False

        # Start with a new clean list
        self.clean_list()

        # Convert back serialized players and add them
        for player in serialized_players:
            self.add_player(first_name=player['first_name'],
                            last_name=player['last_name'],
                            birth_day=player['birth_day'],
                            birth_mon=player['birth_mon'],
                            birth_year=player['birth_year'],
                            sex=player['sex'],
                            rating=player['rating'],
                            tournament_score=player['tournament_score'],
                            insertion_sort=insertion_sort)

        # Done
        db.close()
        return True

    def find_player_by_names(self, first_name: str, last_name: str) -> int:
        """Returns the index of a player corresponding

        param first_name: first name
        param last_name: last name
        return: index or -1 if not found
        """

        # Loop through the list and check names
        for i in range(self.get_number_of_players()):
            if self.players[i].is_player(first_name=first_name, last_name=last_name):
                return i

        return -1

    def update_ratings(self, upper_rank: int, lower_rank: int, increase: bool) -> bool:
        """Increments or decrements ranks in player list to "patch" it when a player is removed/modified

        param upper_rank: patch < this rank
        param lower_rank: patch > this rank
        param increase: True for ++, False for --
        return: always True
        """

        # Sweep through all players and patch...
        for player in self.players:
            rank = player.get_rating()
            if upper_rank >= rank >= lower_rank:
                if increase:
                    rank += 1
                else:
                    rank -= 1
                player.set_rating(rating=rank)

        return True

    def add_player(self, first_name: str, last_name: str, birth_day: int, birth_mon: int,
                   birth_year: int, sex: str, rating: int, tournament_score: float,
                   insertion_sort: bool) -> bool:
        """Create a new player and add it in the list

        param first_name: < 25 letters, non alpha characters will be filtered
        param last_name: same as first name
        param birth_day: no comment
        param birth_mon: no comment
        param birth_year: no comment
        param sex: "M" or "F"
        param rating: rank (integer)
        param tournament_score: default=0, current score if a tournament is ongoing
        param insertion_sort: True = respect alphabetical order while inserting
        return: false if any inconsistency is found in parameters
        """

        new_player = Player()

        if not new_player.set_first_name(first_name) \
                or not new_player.set_last_name(last_name) \
                or not new_player.set_birthday(birth_day, birth_year, birth_mon) \
                or not new_player.set_sex(sex) \
                or not new_player.set_tournament_score(tournament_score) \
                or not new_player.set_rating(rating):
            return False

        # First player in the list, easy
        if not self.players:
            self.players.append(new_player)
            return True

        # Else, insert name and maintain alphabetical order (insertion sort)
        complete_name = new_player.complete_name()
        player_index = 0

        for player in self.players:

            # Detect whether this name already exists
            if player.complete_name() == complete_name:
                print("Player name already used")
                return False

            # Detect whether we reach the first string < in alphabetical order: insertion position
            if player.complete_name() > complete_name and insertion_sort:
                self.players.insert(player_index, new_player)
                break

            # Count players
            player_index += 1

            # Last one was reached, append() is used (either no insertion sort or last in alphabetical order)
            if player_index == self.get_number_of_players():
                self.players.append(new_player)
                break

        return True

    def remove_player(self, first_name: str, last_name: str, patch_ranks: bool) -> bool:
        """Remove a player from the list (if he exists...)

        param first_name: first name...
        param last_name: last name...
        param patch_ranks: adjust the rank of the other players after deletion?
        return: True if he was found and removed
        """

        # Does this user exist in our list?
        index = self.find_player_by_names(first_name, last_name)
        if index == -1:
            print("User not found")
            return False

        # Found it, delete and increase rank of all players who were behind him (if required)
        rank = self.players[index].get_rating()
        if patch_ranks:
            self.update_ratings(upper_rank=self.get_number_of_players(), lower_rank=rank, increase=False)
        del self.players[index]

        return True

    def update_player_score(self, first_name: str, last_name: str, points: float) -> bool:
        """Update a player score

        param first_name: first name...
        param last_name: last name...
        param points: 0, 0.5 or 1 to be added to the total score
        return: True if no mistake was encountered (invalid score or unknown user)
        """

        # Find user
        index = self.find_player_by_names(first_name, last_name)
        if index == -1:
            print("User not found")
            return False

        # Update score
        return self.players[index].increase_tournament_score(points=points)

    def modify_player_sex(self, first_name: str, last_name: str, sex: str) -> bool:
        """Update a player's sex

        param first_name: first name...
        param last_name: last name...
        param sex: "M" or "F"
        return: True if no mistake was encountered
        """

        # Find user
        index = self.find_player_by_names(first_name, last_name)
        if index == -1:
            print("User not found - cannot change player sex")
            return False

        return self.players[index].set_sex(sex)

    def modify_player_birthday(self, first_name: str, last_name: str, day: int, year: int, mon: int) -> bool:
        """Update a player's birthday

        param first_name: first name...
        param last_name: last name...
        param day: valid month day
        param year: year
        param mon: 1-12
        return: True if no mistake was encountered
        """

        # Find user
        index = self.find_player_by_names(first_name, last_name)
        if index == -1:
            print("User not found - cannot change player birthday")
            return False

        return self.players[index].set_birthday(day, year, mon)

    def modify_player_first_name(self, first_name: str, last_name: str, new_name: str) -> bool:
        """Update a player's first name

        param first_name: first name...
        param last_name: last name...
        param new_name: new name...
        return: True if no mistake was encountered
        """

        # Find user
        index = self.find_player_by_names(first_name, last_name)
        if index == -1:
            print("User not found - cannot change player first name")
            return False

        return self.players[index].set_first_name(new_name)

    def modify_player_last_name(self, first_name: str, last_name: str, new_name: str) -> bool:
        """Update a player's last name

        param first_name: first name...
        param last_name: last name...
        param new_name: new name...
        return: True if no mistake was encountered
        """

        # Find user
        index = self.find_player_by_names(first_name, last_name)
        if index == -1:
            print("User not found - cannot change player last name")
            return False

        return self.players[index].set_last_name(new_name)

    def modify_player_rating(self, first_name: str, last_name: str, new_rating: int) -> bool:
        """Update a player rating (if he exists...) and correct all the ratings accordingly

        param first_name: first name...
        param last_name: last name...
        param rating: new value, must be > 0 and < number of players, of course
        return: True if no mistake was encountered
        """

        if new_rating < 1 or new_rating > self.get_number_of_players():
            print("Invalid rating, must be > 0 and < number of players")
            return False

        # Find user
        index = self.find_player_by_names(first_name, last_name)
        if index == -1:
            print("User not found - cannot change player rating")
            return False

        # Retrieve the current rating for the player to be modified
        current_rating = self.players[index].get_rating()

        # Trivial case, nothing to do
        if current_rating == new_rating:
            return True

        # Next case: player gets a better rating, we need to downgrade a set of players
        if current_rating < new_rating:
            self.update_ratings(upper_rank=new_rating, lower_rank=current_rating, increase=False)

        # Last case: player is downgraded, some other players must be upgraded
        else:
            self.update_ratings(upper_rank=current_rating, lower_rank=new_rating, increase=True)

        # Last operation: modify the player itself
        self.players[index].set_rating(rating=new_rating)

        return True

    def sort_list(self) -> bool:
        """Sort player list by tournament_score, and rating when scores are equal

        return: Always True
        """

        """This will point the last unsorted player (+1)
            The best player found among this part of the list will be moved to the end.
            Thus current_pos will be decreased until all players have been moved to eof list.
            And we finally get best player in position 0, and so on...
        """
        current_pos = self.get_number_of_players()

        # Main loop - leave it when the remaining players are reduced to nothing
        while current_pos > 0:
            # Init "best player" stats with the first one, for instance
            best_rank = self.players[0].get_rating()
            best_score = self.players[0].get_tournament_score()
            best_index = 0

            # Explore all remaining players
            for i in range(current_pos):
                player_rank = self.players[i].get_rating()
                player_score = self.players[i].get_tournament_score()

                # Better score found, or same score but better rating -> update our "best player"
                if player_score > best_score or (player_score == best_score and player_rank < best_rank):
                    best_rank = player_rank
                    best_score = player_score
                    best_index = i

            # Now we know who is the best -> move it to the end
            tmp_player = self.players.pop(best_index)
            self.players.append(tmp_player)

            # Loop goes on with one less player
            current_pos -= 1

        return True

    def sort_list_alpha(self) -> bool:
        """Sort player list in alphabetical order

        return: Always True
        """

        # Same algorithm as in the previous method, but simpler
        current_pos = self.get_number_of_players()

        # Main loop
        while current_pos > 0:
            best_index = 0
            lowest_complete_name = self.players[0].complete_name()

            # Explore all remaining players
            for i in range(current_pos):
                complete_name = self.players[i].complete_name()

                # "Lower" name found, update
                if complete_name < lowest_complete_name:
                    lowest_complete_name = complete_name
                    best_index = i

            # Now we know who is the best -> move it to the end
            tmp_player = self.players.pop(best_index)
            self.players.append(tmp_player)

            # Loop goes on with one less player
            current_pos -= 1

        return True

    def get_player(self, index: int) -> Player:
        """Retrieve a copy of a player object from the list (by index)

        param index: index
        return: Player
        """

        return copy.deepcopy(self.players[index])
