"""
2016 Booth: Obstacle Class

@Author: Atulya Ravishankar
@Organization: Student Dormitory Council, Booth Committee
@Chair: David Perry

This file contains the implementation of the Obstacle class

Updates:
	- 2/26/2016: Implemented initial class methods
"""

################################################################################
########################### Obstacle class #####################################

class Obstacle(object):

	def __init__(self, unique_id, obstacle_type, position):
		self.id = unique_id
		self.obstacle_type = obstacle_type
		self.position = position

	def get_obstacle_type(self):
		return self.obstacle_type

	def get_obstacle_id(self):
		return self.id

	def get_obstacle_position(self):
		return self.position

	def __str__(self):
		return "'id': " + str(self.id) + "\n'obstacle_type': " + \
		            self.obstacle_type + "\n'position': " + str(self.position)

################################################################################
################################################################################