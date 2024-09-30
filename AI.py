import random
from interfaces import interface_headers as IH
import game_model as GM

class AI:
    def __init__(self,  difficulty: str, num_ships: int, player_type: IH.PlayerTypeEnum):
        """
        This Python function initializes an AI with specified difficulty level, number of ships, and player
        type.
        
        :param difficulty: The `difficulty` parameter in the `__init__` method is a string that represents
        the specified difficulty level for the AI. It could be something like "easy", "medium", or "hard"
        depending on the game or application you are working on
        :type difficulty: str
        :param num_ships: The `num_ships` parameter in the `__init__` method represents the number of ships
        that will be used in the game. It is an integer value that determines the initial number of ships
        for the AI player
        :type num_ships: int
        :param player_type: The `player_type` parameter in the `__init__` method is of type
        `IH.PlayerTypeEnum`. It is used to specify the type of player, either `PLAYER_TYPE_HOST` or
        `PLAYER_TYPE_JOIN`. The code snippet you provided sets the `ai_type` attribute based on the value
        :type player_type: IH.PlayerTypeEnum
        """
        """
        Initialize the AI with the specified difficulty level.
        """
        self.difficulty = difficulty
        self.num_ships = num_ships
        self.possible_targets = []
        self.ai_type = IH.PlayerTypeEnum.PLAYER_TYPE_HOST if player_type == IH.PlayerTypeEnum.PLAYER_TYPE_JOIN else IH.PlayerTypeEnum.PLAYER_TYPE_JOIN

    def place_ships(self, model: GM.GameModel, player_type: IH.PlayerTypeEnum):
        """
        The `place_ships` function randomly places ships on the game board while ensuring valid placements.
        
        :param model: The `model` parameter in the `place_ships` method is of type `GM.GameModel`. This
        parameter likely represents the game model or board on which the ships are being placed. It is used
        to interact with the game state, such as checking if a coordinate is valid or updating the state
        :type model: GM.GameModel
        :param player_type: The `player_type` parameter in the `place_ships` method is of type
        `IH.PlayerTypeEnum`. This parameter is used to determine the type of player for which the ships are
        being placed. It helps in customizing the ship placement logic based on whether the player is a
        human player or an
        :type player_type: IH.PlayerTypeEnum
        """
        ships_placed = 0

        for ship_length in range(1,self.num_ships + 1):
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
            start_coordinate = ( row, col )
            direction = "H" if direction == 0 else "V"
            boat_coords = IH.boat_coords(start_coordinate, direction, ship_length)
            # If we find that at least one of the coordinates
            # is not a valid coordinate, we will trigger the error
            # state in the presenter
            for coord in boat_coords:
                if not model.is_valid_coord( self.ai_type, coord, IH.GameEventType.GAME_EVENT_PLACE_SHIPS ):
                    can_place = False
                    break

            # Place the ship if it's a valid placement
            if can_place:
                for coord in boat_coords:
                    new_state = { IH.GAME_COORD_TYPE_ID_INDEX : ship_length, IH.GAME_COORD_TYPE_STATE_INDEX: IH.CoordStateType.COORD_STATE_BASE }
                model.update_coord( self.ai_type, coord, new_state )
                ships_placed += 1
            # Implement ship placement logic here

    def make_attack(self, model: GM.GameModel, player_type: IH.PlayerTypeEnum):
        """
        The function `make_attack` selects the appropriate attack method based on the difficulty level
        specified.
        
        :param model: The `model` parameter in the `make_attack` method refers to an instance of the
        `GameModel` class. This parameter likely contains information about the game state, such as player
        positions, scores, and other relevant data needed to make an attack in the game
        :type model: GM.GameModel
        :param player_type: PlayerTypeEnum is an enumeration that represents the type of player, such as
        Human or AI. It helps differentiate between different types of players in the game
        :type player_type: IH.PlayerTypeEnum
        :return: The `make_attack` method returns the result of the attack based on the difficulty level. It
        calls different attack methods (`_easy_attack`, `_medium_attack`, `_hard_attack`) based on the
        difficulty level ("Easy", "Medium", "Hard") and returns the result of the corresponding attack
        method.
        """
        """
        Make an attack based on the difficulty level.
        """
        if self.difficulty == "Easy":
            return self._easy_attack(model, player_type)
        elif self.difficulty == "Medium":
            return self._medium_attack(model, player_type)
        elif self.difficulty == "Hard":
            return self._hard_attack(model, player_type)

    def _easy_attack(self, model: GM.GameModel, player_type: IH.PlayerTypeEnum):
        """
        The `_easy_attack` function implements a strategy for easy difficulty where the player fires
        randomly every turn.
        
        :param model: The `model` parameter is an instance of the `GameModel` class, which likely represents
        the game state or model of the game being played. It is used within the `_easy_attack` method to
        determine valid coordinates for the attack based on the current game state
        :type model: GM.GameModel
        :param player_type: Player type can be either PlayerTypeEnum.PLAYER_ONE or
        PlayerTypeEnum.PLAYER_TWO, indicating which player is making the attack
        :type player_type: IH.PlayerTypeEnum
        :return: The `_easy_attack` function returns a tuple containing the randomly generated row and
        column coordinates for the attack.
        """
        """
        Easy difficulty: Fire randomly every turn.
        """
        while True:
            row = random.randint(0, IH.NUMBER_OF_ROWS - 1)
            col = random.randint(0, IH.NUMBER_OF_COLS - 1)
            if model.is_valid_coord(player_type, (row, col), IH.GameEventType.GAME_EVENT_MAKE_ATTACK):
                return (row, col)

    def _medium_attack(self, model: GM.GameModel, player_type: IH.PlayerTypeEnum):
        """
        This function implements a medium difficulty attack strategy in a Battleship game by firing randomly
        until hitting a ship, then targeting orthogonally adjacent spaces.
        
        :param model: The `model` parameter in the `_medium_attack` method is an instance of the `GameModel`
        class. It is used to interact with the game model, such as checking coordinates, getting cell
        information, and updating cell states during the game
        :type model: GM.GameModel
        :param player_type: Player type is an enumeration that specifies the type of player in the game. It
        could be either a human player or a computer player
        :type player_type: IH.PlayerTypeEnum
        :return: The `_medium_attack` method returns the coordinates of the attack that will be made in the
        game.
        """
        """
        Medium difficulty: Fire randomly until it hits a ship, then fire in orthogonally adjacent spaces.
        """
        if self.possible_targets:
            coords = self.possible_targets.pop(0)
        else:
            coords = self._easy_attack(model, player_type)
        # If there is a ship at the attack coordinates, and it is not hit already,
        # add all adjacent coordinates to the possible targets
        if model.is_valid_coord(player_type, coords, IH.GameEventType.GAME_EVENT_MAKE_ATTACK):
            cell = model.get_coord(player_type, coords)
            if cell[IH.GAME_COORD_TYPE_ID_INDEX] > IH.BASE_CELL and cell[IH.GAME_COORD_TYPE_STATE_INDEX] != IH.CoordStateType.COORD_STATE_HIT:
                cell[IH.GAME_COORD_TYPE_STATE_INDEX] = IH.CoordStateType.COORD_STATE_HIT
                self.possible_targets.extend(self._get_adjacent_coords(coords))
        return coords

    def _hard_attack(self, model: GM.GameModel, player_type: IH.PlayerTypeEnum):
        """
        This function represents a hard difficulty level AI that knows the location of all ships and lands a
        hit every turn.
        
        :param model: The `model` parameter is an instance of the `GameModel` class, which likely contains
        information about the game state such as the positions of ships and previous attacks
        :type model: GM.GameModel
        :param player_type: Player type is an enumeration that specifies the type of player, such as human
        or computer player
        :type player_type: IH.PlayerTypeEnum
        :return: The `_hard_attack` method is returning a tuple containing the coordinates `(row, col)`
        where the AI player wants to make an attack.
        """
        """
        Hard difficulty: Knows where all ships are and lands a hit every turn.
        """
        for row in range(IH.NUMBER_OF_ROWS):
            for col in range(IH.NUMBER_OF_COLS):
                if model.get_coord(player_type, (row, col))[IH.GAME_COORD_TYPE_ID_INDEX] > IH.BASE_CELL and model.is_valid_coord(player_type, (row, col), IH.GameEventType.GAME_EVENT_MAKE_ATTACK):
                    return (row, col)

    def _get_adjacent_coords(self, coord):
        """
        The `_get_adjacent_coords` function returns a list of orthogonally adjacent coordinates based on the
        input coordinate.
        
        :param coord: The `_get_adjacent_coords` method takes a coordinate `coord` as input, which is a
        tuple containing the row and column values of a position on a grid. The method then calculates and
        returns a list of orthogonally adjacent coordinates to the input coordinate within the grid
        :return: The function `_get_adjacent_coords` returns a list of orthogonally adjacent coordinates
        based on the input coordinate `coord`.
        """
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
