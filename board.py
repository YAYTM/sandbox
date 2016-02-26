"""
2016 Booth: Board Class (and some testing)

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
                 Started interface methods for Board that Map uses
                 Wrote preliminary tests for Board/Obstacle
"""

import json
import obstacle

################################################################################
############################## Board class #####################################

class Board(object):

	# Initializes game
	def __init__(self, height, width, \
		                 p1_battleship, p1_sub, p2_battleship, p2_sub):
		# Initialize board
		self.init_board_json(height, width)
		# Initialize ships
		self.init_ship(1, "Battleship", p1_battleship, 100)
		self.init_ship(1, "Submarine", p1_sub, 100)
		self.init_ship(2, "Battleship", p2_battleship, 100)
		self.init_ship(2, "Submarine", p2_sub, 100)
		# Initialize obstacles
		self.init_obstacle_on_board(1, "Dolphin", [5, 6, 4])
		self.init_obstacle_on_board(2, "Iceberg", [10, 10, 0])

	# Initializes a JSON-encoded string of the board
	def init_board_json(self, height, width):
		self.board = json.dumps({
			u"board_height": height,
			u"board_width": width,
			u"team1_battleship": [],
			u"team1_battleship_health": 0,
			u"team1_submarine": [],
			u"team1_submarine_health": 0,
			u"team2_battleship": [],
			u"team2_battleship_health": 0,
			u"team2_submarine": [],
			u"team2_submarine_health": 0,
			u"obstacles": []
		})

	# Initializes obstacles on both boards. 
	# 'positions' is a 3D vector in the form [row, col, depth]
	def init_obstacle_on_board(self, unique_id, obstacle_type, positions):
		board = json.loads(self.board)
		new_obstacle = obstacle.Obstacle(unique_id, obstacle_type, positions)
		# Board is not a standard type, so we must make JSON recognize it
		d = { '__class__':new_obstacle.__class__.__name__,
		      '__module__':new_obstacle.__module__,
		    }
		d.update(new_obstacle.__dict__)
		board["obstacles"].append(d)
		self.board = json.dumps(board)

	# Adds information about a ship to the board
	def init_ship(self, team, ship_type, position, health):
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

	# Returns a specified attribute in a specified json object
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
	def hit_ship(self, victim_team, ship_type):
		pass

	# Moves ship on the board
	# 'new_location' is a 3D vector [row, col, depth]
	def move_ship(self, moving_team, ship_type, new_location):
		pass

	# Destroys an obstacle when it has been hit
	def hit_obstacle(self, location):
		pass

################################################################################
################################################################################

################################################################################
################################# Testing ######################################

def test():
	print "Starting tests..."
	print

	B = Board(20, 20, [1, 1, 0], [3, 4, 5], [10, 12, 0], [15, 15, 2])
	print "Successfuly initialized board (by visual inspection):"
	print B
	print

	print "Checking obstacle_exists()...",
	assert(B.obstacle_exists(1))
	assert(B.obstacle_exists(2))
	assert(not B.obstacle_exists(42))
	assert(not B.obstacle_exists(-6))
	print "works as expected"
	print

	print "Checking get_attribute() and get_obstacle_position()..."
	print "Team 1 Battleship location:",B.get_attribute("team1_battleship")
	print "Team 2 Battleship health:",B.get_attribute("team2_battleship_health")
	print "Obstacle (ID = 1) position:", B.get_obstacle_position(1)
	print "Obstacle (ID = 2) position:", B.get_obstacle_position(2)
	print

	print "Starting tests to check argument formatting errors..."
	try:
		B.get_attribute("Invalid attribute")
		print "Failed to catch invalid attribute"
	except:
		print "Caught invalid attribute"
	
	try:
		B.init_ship(1, "Invalid ship", [0, 0.5, -2], -4)
		print "Failed to catch invalid ship initialization"
	except:
		print "Caught invalid ship initialization"

	try:
		B.get_obstacle_position(42)
		print "Failed to catch invalid obstacle ID"
	except:
		print "Caught invalid obstacle ID"

	print

	print "Checking 'expose' correctness (by visual inspection)..."
	print ("Expect only 'board_height', 'team1_submarine' and \
'team2_battleship_health':"), \
B.expose(["board_height", "team1_submarine", "team2_battleship_health"])
	print "Expect only 'obstacles':", B.expose(["obstacles"])
	print "Expect only 'team2_battleship':", B.expose(["team2_battleship"])
	print "Expect nothing:", B.expose([])
	print

	print "Testing hit_ship()..."
	print "WARNING: Tests not written yet"
	print

	print "Testing move_ship()..."
	print "WARNING: Tests not written yet"
	print

	print "Testing hit_obstacle..."
	print "WARNING: Tests not written yet"
	print

	print "All tests ran to completion successfuly."

################################################################################
################################################################################

def main():
	test()

main()
