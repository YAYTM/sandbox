"""
2016 Booth: Testing

@Author: Atulya Ravishankar
@Organization: Student Dormitory Council, Booth Committee
@Chair: David Perry

This file contains the model for the battleship game. It communicates with the 
view by updating a singular JSON 'board' file over the network.

Updates: 
    - 2/25/2016: Started implementing the model
                 Wrote function init_ship()
                 Wrote function init_obstacle()
                 Wrote function get_attribute()
                 Very briefly tested the above three functions
                 Defined the Python classes that we might use
                    - Ship, Battleship, Submarine, Torpedo, Mine, Obstacle
    - 2/26/2016: Removed old Python classes
                 Wrote new Board and Obstacle classes (Obstacle in another file)
                 Wrote initializers for Board
                 Wrote interface methods for board/map handlers
                 Tested major methods and features of Board

"""

import json
import obstacle

class Board(object):

    #### $ PRIVATE BOARD METHODS $ #############################################

    # Initializes the board
    # NOTE: Does not initialize obstacles - see add_obstacle()
    def __init__(self, height, width, depth, \
                      p1_battleship, p1_sub, \
                      p2_battleship, p2_sub):
        # Check validify of arguments
        if (height <= 0 or width <= 0 or depth < 0):
            raise Exception("Invalid height, width or depth!")
        else:
            self.height = height
            self.width = width
            self.depth = depth
        if (not (self.is_valid_position(p1_battleship) and 
                 self.is_valid_position(p1_sub) and 
                 self.is_valid_position(p2_battleship) and 
                 self.is_valid_position(p2_sub))):
            raise Exception("Initial position of one of more ships is invalid!")
        # Initialize board
        self.__init_board_json(height, width, depth)
        # Initialize ships
        self.__init_ship(1, "Battleship", p1_battleship, 100)
        self.__init_ship(1, "Submarine", p1_sub, 100)
        self.__init_ship(2, "Battleship", p2_battleship, 100)
        self.__init_ship(2, "Submarine", p2_sub, 100)

    # Initializes a JSON-encoded string of the board
    def __init_board_json(self, height, width, depth):
        self.board = json.dumps({
            u"board_height": height,
            u"board_width": width,
            u"board_depth": depth,
            u"team1_battleship": [],
            u"team1_battleship_health": 0,
            u"team1_submarine": [],
            u"team1_submarine_health": 0,
            u"team2_battleship": [],
            u"team2_battleship_health": 0,
            u"team2_submarine": [],
            u"team2_submarine_health": 0,
            u"obstacles": [],
            u"sunk_ships": []
        })

    # Initializes obstacles on both boards. 
    # 'positions' is a 3D vector in the form [row, col, depth]
    def __init_obstacle_on_board(self, unique_id, position, obstacle_type):
        board = json.loads(self.board)
        new_obstacle = obstacle.Obstacle(unique_id, obstacle_type, position)
        # Board is not a standard type, so we must make JSON recognize it
        d = { '__class__':new_obstacle.__class__.__name__,
              '__module__':new_obstacle.__module__,
            }
        d.update(new_obstacle.__dict__)
        board["obstacles"].append(d)
        self.board = json.dumps(board)

    # Adds information about a ship to the board
    def __init_ship(self, team, ship_type, position, health):
        old_board = json.loads(self.board)
        if (team == 1 and ship_type == "Battleship"):
            old_board["team1_battleship"] = position
            old_board["team1_battleship_health"] = health
        elif (team == 1 and ship_type == "Submarine"):
            old_board["team1_submarine"] = position
            old_board["team1_submarine_health"] = health
        elif (team == 2 and ship_type == "Battleship"):
            old_board["team2_battleship"] = position
            old_board["team2_battleship_health"] = health
        elif (team == 2 and ship_type == "Submarine"):
            old_board["team2_submarine"] = position
            old_board["team2_submarine_health"] = health
        else:
            raise Exception("You are trying to initialize an invalid ship")
        self.board = json.dumps(old_board)

    # Prints board out nicely, for debugging
    def __str__(self):
        board = json.loads(self.board)
        return json.dumps(board, sort_keys = True, indent = 4, \
                                                      separators = (',', ': '))

    #### $ PUBLIC BOARD/MAP INTERFACE FUNCTIONS $ ##############################

    # Returns a JSON-encoded string of the board
    # NOTE: Map handler should use this method to read the board
    def current_board(self):
        return self.board

    # Returns the board's dimensions in the form [height, width, depth]
    def board_dimensions(self):
        return [self.height, self.width, self.depth]

    # Returns true is 'position' is a valid position on the board
    # 'position' is a 3D corrdinate in the form [row, col, depth]
    def is_valid_position(self, position):
        [row, col, depth] = position
        return ((0 <= row < self.height) and 
               (0 <= col < self.width) and 
               (0 <= depth < self.depth))

    # Adds a specified obstacle to the board
    def add_obstacle(self, unique_id, position, obstacle_type):
        if (self.location_occupied(position)):
            raise Exception("position is already occupied")
        self.__init_obstacle_on_board(unique_id, position, obstacle_type)

    # Returns an array [name, health] with the ship's name and health
    def ship_name_and_health(self, team, ship_type):
        if (team == 1 and ship_type == "Battleship"):
            name = "team1_battleship"
            health = "team1_battleship_health"
        elif (team == 1 and ship_type == "Submarine"):
            name = "team1_submarine"
            health = "team1_submarine_health"
        elif (team == 2 and ship_type == "Battleship"):
            name = "team2_battleship"
            health = "team2_battleship_health"
        elif (team == 2 and ship_type == "Submarine"):
            name = "team2_submarine"
            health = "team2_submarine_health"
        else:
            raise Exception("This ship doesn't exist!")
        return [name, health]

    # Returns the position of the specified ship
    def ship_position(self, team, ship_type):
        board = json.loads(self.board)
        name = self.ship_name_and_health(team, ship_type)[0]
        return board[name]

    # Returns a specified attribute in self.board
    # Both arguments must be strings
    def get_attribute(self, attribute):
        json_obj = json.loads(self.board)
        if (attribute not in json_obj.keys()): # invalid attribute
            raise Exception("Invalid attribute") 
        else:
            return json_obj[attribute]

    # Given an obstacle's id, returns its position. 
    # Will throw an error if no such obstacle exists
    def get_obstacle_position(self, unique_id):
        board = json.loads(self.board)
        for obstacle in board["obstacles"]:
            if obstacle["id"] == unique_id:
                return obstacle["position"]
        raise Exception("No obstacle with id = %d found." %(unique_id))

    # Returns True is obstacle with id = unique_id exists, False otherwise
    def obstacle_exists(self, unique_id):
        board = json.loads(self.board)
        for obstacle in board["obstacles"]:
            if obstacle["id"] == unique_id:
                return True
        return False    

    # Returns a dict that contains only the attributes stated in 'args'
    # 'args' is a list containing attributes (as strings)
    def expose(self, args):
        board_to_read = json.loads(self.board)
        visible_keys = dict()
        for key in board_to_read.keys():
            if (key in args):
                visible_keys[key] = board_to_read[key]
        return visible_keys

    # Deals damage to a ship when it has been hit
    def hit_ship(self, victim_team, ship_type, damage):
        board = json.loads(self.board)
        [ship, health] = self.ship_name_and_health(victim_team, ship_type)
        current_health = board[health]
        new_health = max(current_health - damage, 0)
        board[health] = new_health
        if (new_health == 0):   # Ship is sunk
            board["sunk_ships"].append(ship)
        self.board = json.dumps(board)

    # Returns True if the given ship has been sunk
    def ship_is_sunk(self, victim_team, ship_type):
        board = json.loads(self.board)
        ship = self.ship_name_and_health(victim_team, ship_type)[0]
        return (ship in board["sunk_ships"])

    # Moves ship on the board
    # 'new_location' is a 3D vector [row, col, depth]
    # 'new_location' must be different from current location
    def move_ship(self, moving_team, ship_type, new_location):
        if (not self.is_valid_position(new_location)):
            raise Exception("new_location is not a valid location on the board")
        if (self.location_occupied(new_location)):
            raise Exception("new_location is already occupied")
        board = json.loads(self.board)
        ship = self.ship_name_and_health(moving_team, ship_type)[0]
        if (board[ship] == new_location):
            raise Exception("Current location and destination must differ")
        board[ship] = new_location
        self.board = json.dumps(board)

    # Returns True if there is any object at 'location'
    def location_occupied(self, location):
        if (not self.is_valid_position(location)):
            raise Exception("This is not a valid location on the board")
        board = json.loads(self.board)
        # Check ships
        ships = ["team1_battleship", "team1_submarine", \
                 "team2_battleship", "team2_submarine"]
        for ship in ships:
            if (board[ship] == location):
                return True
        for obstacle in board["obstacles"]:
            if (obstacle["position"] == location):
                return True
        return False
    
    # Destroys an obstacle when it has been hit, removes it from 'obstacles'
    def destroy_obstacle(self, location):
        if not (self.is_valid_position(location) and self.location_occupied(location)):
            raise Exception("Invalid or empty location")
        board = json.loads(self.board)
        obstacles = board["obstacles"]
        index = 0;
        found_obstacle = False
        for obstacle in obstacles:
            if (obstacle["position"] == location):
                found_obstacle = True
                board["obstacles"].pop(index)
                break
            index += 1
        if (not found_obstacle):
            raise Exception("No such obstacle exists")
        self.board = json.dumps(board)
