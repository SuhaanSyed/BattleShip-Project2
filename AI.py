import random
from interfaces import interface_headers as IH

class AI:
    def __init__(self,  difficulty: str, num_ships: int):
        """
        Initialize the AI with the specified difficulty level.
        """
        self.difficulty = difficulty
        self.num_ships = num_ships
        self.board = [[0 for _ in range(IH.NUMBER_OF_COLS)] for _ in range(IH.NUMBER_OF_ROWS)]
        self.opponent_board = [[0 for _ in range(IH.NUMBER_OF_COLS)] for _ in range(IH.NUMBER_OF_ROWS)]
        self.last_hit = None
        self.possible_targets = []


    def place_ships(self):
        ships_placed = 0


        for ship_length in range(1,self.num_ships+1):
            # Randomly determine ship length (you can modify this logic to have fixed-length ships)

            # Randomly choose direction: 0 for horizontal, 1 for vertical
            direction = random.choice([0, 1])

            if direction == 0:  # Horizontal placement
                row = random.randint(0, IH.NUMBER_OF_ROWS - 1)
                col = random.randint(0, IH.NUMBER_OF_COLS - ship_length)  # Ensure ship fits horizontally
            else:  # Vertical placement
                row = random.randint(0, IH.NUMBER_OF_ROWS - ship_length)
                col = random.randint(0, IH.NUMBER_OF_COLS - 1)  # Ensure ship fits vertically

            # Check if the space is free to place the ship
            can_place = True
            for i in range(ship_length):
                if direction == 0:  # Horizontal
                    if self.board[row][col + i] != 0:  # Check if space is occupied
                        can_place = False
                        break
                else:  # Vertical
                    if self.board[row + i][col] != 0:  # Check if space is occupied
                        can_place = False
                        break

            # Place the ship if it's a valid placement
            if can_place:
                for i in range(ship_length):
                    if direction == 0:  # Horizontal
                        self.board[row][col + i] = 1  # Mark ship's position
                    else:  # Vertical
                        self.board[row + i][col] = 1  # Mark ship's position
                ships_placed += 1
            # Implement ship placement logic here
        self.print_board()
    
    def print_board(self):
        """
        Print the current state of the board.
        """
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print()  # Add an empty line for better readability

    def make_attack(self):
        """
        Make an attack based on the difficulty level.
        """
        if self.difficulty == "Easy":
            return self._easy_attack()
        elif self.difficulty == "Medium":
            return self._medium_attack()
        elif self.difficulty == "Hard":
            return self._hard_attack()

    def _easy_attack(self):
        """
        Easy difficulty: Fire randomly every turn.
        """
        while True:
            row = random.randint(0, IH.NUMBER_OF_ROWS - 1)
            col = random.randint(0, IH.NUMBER_OF_COLS - 1)
            if self.opponent_board[row][col] == 0:
                return (row, col)

    def _medium_attack(self):
        """
        Medium difficulty: Fire randomly until it hits a ship, then fire in orthogonally adjacent spaces.
        """
        if self.possible_targets:
            return self.possible_targets.pop(0)
        elif self.last_hit:
            row, col = self.last_hit
            self.possible_targets = self._get_adjacent_coords((row, col))
            return self.possible_targets.pop(0)
        else:
            return self._easy_attack()

    def _hard_attack(self):
        """
        Hard difficulty: Knows where all ships are and lands a hit every turn.
        """
        for row in range(IH.NUMBER_OF_ROWS):
            for col in range(IH.NUMBER_OF_COLS):
                if self.opponent_board[row][col] == 0:
                    return (row, col)

    def update_opponent_board(self, coord, result):
        """
        Update the opponent's board with the result of the attack.
        """
        row, col = coord
        #col = self.convert_letter_to_col(col)
        self.opponent_board[row][col] = result
        if result == IH.CoordStateType.COORD_STATE_HIT:
            self.last_hit = coord
            self.possible_targets.extend(self._get_adjacent_coords(coord))
    

    def update_ai_board(self, coord, result):
        """
        Update the ai's board with the result of the attack.
        """
        row, col = coord
        col = self.convert_letter_to_col(col)
        self.board[row][col] = result
    

    def check_ship_at(self, coordinates):
        """
        Check if there is a ship at the given coordinates on the AI's board.

        :param coordinates: A tuple (row, col) representing the coordinates to check.
        :return: "Hit" if there is a ship at the given coordinates, "Miss" otherwise.
        """
        row, col = coordinates

        if self.board[row][col] == 1:
            return 1
        else:
            return 0

        return "Hit" if self.board[row][col] == 1 else "Miss"


    def _get_adjacent_coords(self, coord):
        """
        Get orthogonally adjacent coordinates.
        """
        row, col = coord
        adjacent_coords = []
        if row > 0:
            adjacent_coords.append((row - 1, col))
        if row < IH.NUMBER_OF_ROWS - 1:
            adjacent_coords.append((row + 1, col))
        if col > 0:
            adjacent_coords.append((row, col - 1))
        if col < IH.NUMBER_OF_COLS - 1:
            adjacent_coords.append((row, col + 1))
        return adjacent_coords
    
    def ships_are_alive(self):
        """
        Check if the AI has any ships left.
        Returns True if there are any ships (1's) remaining on the board, False otherwise.
        """
        for row in self.board:
            if 1 in row:  # If there is a '1' anywhere, the AI still has ships
                return True
        return False
    
    def is_valid_coord(self, coord):
        """
        Check if the given coordinate is within the valid range of the board.
        
        :param coord: A tuple (row, col) representing the coordinate.
        :return: True if the coordinate is within bounds, False otherwise.
        """
        row, col = coord
        return 0 <= row < IH.NUMBER_OF_ROWS and 0 <= col < IH.NUMBER_OF_COLS
    
    def get_coord(self, coord, is_opponent=False):
        """
        Get the state of a given coordinate from the board (or opponent's board).
        
        :param coord: A tuple (row, col) representing the coordinate.
        :param is_opponent: If True, check the opponent's board; otherwise, check the AI's board.
        :return: The state at the given coordinate (e.g., 0 for empty, 1 for ship, etc.).
        """
        row, col = coord
        if is_opponent:
            return self.opponent_board[row][col]
        return self.board[row][col]
    
    def update_coord(self, coord, value, is_opponent=False):
        """
        Update the state of a given coordinate on the board (or opponent's board).
        
        :param coord: A tuple (row, col) representing the coordinate.
        :param value: The value to set at the given coordinate (e.g., 1 for ship, 0 for empty, etc.).
        :param is_opponent: If True, update the opponent's board; otherwise, update the AI's board.
        """
        row, col = coord
        if is_opponent:
            self.opponent_board[row][col] = value
        else:
            self.board[row][col] = value

    def convert_col_to_letter(self, coord):
        """
        Convert a column index (0-9) to a letter (A-J).
        
        :param col: Integer column index (0-9)
        :return: Corresponding letter (A-J) or an error message if out of range
        """
        row, col = coord
        if 0 <= col <= 9:
            return row, chr(ord('A') + col)  # Convert to letter (A=0, B=1, ..., J=9)
        else:
            raise ValueError("Column index must be between 0 and 9.")

    def convert_letter_to_col(self, letter):
        """
        Convert a letter (A-J) to a column index (0-9).
        
        :param letter: Character representing the column (A-J)
        :return: Corresponding column index (0-9) or an error message if out of range
        """
        if letter in "ABCDEFGHIJ":
            return ord(letter) - ord('A')  # Convert letter to column index
        else:
            raise ValueError("Letter must be between A and J.")

