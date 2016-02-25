"""
2016 Booth: Battleship Model

@Author(s): Atulya Ravishankar
@Organization: Student Dormitory Council, Booth Committee
@Chair: David Perry

This file contains the model for the battleship game. It communicates with the 
view by sending and receiving JSON files over the network.

Updates: 
    - 2/25/2016: Started implementing the model
                 Wrote function init_ship()
                 Wrote function init_obstacle()
                 Wrote function get_attribute()
                 Very briefly tested the above three functions
                 Defined the Python classes that we might use
                    - Ship, Battleship, Submarine, Torpedo, Mine, Obstacle
"""


"""
I need to know how the board is going to work...
"""

import os
import string
import math
import json

#### $ BEGIN INITIALIZER FUNCTIONS $ ###########################################

# Initializes a ship in a given position for a given team (see ship_schema.json)
# team: integer, 
# id: integer, 
# ship_type: string "battleship"/"submarine", 
# weapon_type: string "mine"/"torpedo", 
# position: list [x, y]
# Returns a JSON-encoded string
def init_ship(team, unique_id, ship_type, weapon_type, position):
	json_obj = {
		u"id": unique_id,
		u"object_type": "ship",
		u"team": team,
		u"ship_type": ship_type,
		u"weapon_type": weapon_type,
		u"current_health": 100,
		u"position": position
	}
	return json.dumps(json_obj)

# Initializes an obstacle
# Returns a JSON-encoted string
def init_obstacle(unique_id, position):
	json_obj = {
		u"object_type": "obstacle",
		u"id": unique_id,
		u"position": position
	}
	return json.dumps(json_obj);

def init_board(team):
	pass

#### $ END INITIALIZER FUNCTIONS $ #############################################

#### $ BEGIN ATTRIBUTE VIEWING/EDITING FUNCTIONS $ #############################

# Returns a specified attribute in a specified json object
# Both arguments must be strings
def get_attribute(json_string, attribute):
	json_obj = json.loads(json_string)
	if (attribute not in json_obj.keys()): # invalid attribute
		raise Exception("Invalid attribute")
	else:
		return json_obj[attribute]

#### $ END ATTRIBUTE VIEWING/EDITING FUNCTIONS $ ###############################

################################################################################
################################# Classes ######################################
################################################################################

##### $ BEGIN SHIP CLASSES $ ###################################################

class Ship(object):

	# Ship constructor
	def __init__(self):
		pass

class Battleship(Ship):

	def __init__(self):
		super(Battleship, self).__init__()

class Submarine(Ship):

	def __init__(self):
		super(Submarine, self).__init__()
		
##### $ END SHIP CLASSES $ #####################################################

##### $ BEGIN WEAPON CLASSES $ #################################################

class Mine(object):

	def __init__(self):
		pass

class Torpedo(object):

	def __init__(self):
		pass

##### $ END WEAPON CLASSES $ ###################################################

##### $ BEGIN OBSTACLE CLASSES $ ###############################################

class Obstacle(object):

	def __init__(self):
		pass

##### $ END OBSTACLE CLASSES $ #################################################

################################################################################
################################################################################
################################################################################
