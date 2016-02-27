"""
2016 Booth: Board Class (and some testing)

@Author: Atulya Ravishankar
@Organization: Student Dormitory Council, Booth Committee
@Chair: David Perry

This file contains a test function for the Board class

Updates:
    - 2/27/2016: Wrote broad tests for major methods

"""

import json
import board

def test():
    print "Starting tests..."
    print

    # Initialization
    B = board.Board(20, 20, 10, [1, 1, 0], [3, 4, 5], [10, 12, 0], [15, 15, 2])
    B.add_obstacle(1, [5, 6, 4], "Dolphin")
    B.add_obstacle(2, [10, 10, 0], "Iceberg")
    print "Successfuly initialized board (by visual inspection):"
    #print B.current_board()
    print B
    print

    print "Checking dimenion functions...",
    assert(B.board_dimensions() == [20, 20, 10])
    assert(B.is_valid_position([1, 2, 3]))
    assert(B.is_valid_position([0, 0, 0]))
    assert(B.is_valid_position([19, 19, 9]))
    assert(not B.is_valid_position([20, 20, 10]))
    assert(not B.is_valid_position([-1, -2, -3]))
    assert(not B.is_valid_position([-1, 2, 10]))
    print "works as expected"
    print

    # obstacle_exists()
    print "Checking obstacle_exists()...",
    assert(B.obstacle_exists(1))
    assert(B.obstacle_exists(2))
    assert(not B.obstacle_exists(42))
    assert(not B.obstacle_exists(-6))
    print "works as expected"
    print

    # get_attribute() amd obstacle_position()
    print "Checking get_attribute() and get_obstacle_position()..."
    print "Team 1 Battleship location:",B.get_attribute("team1_battleship")
    print "Team 2 Battleship health:",B.get_attribute("team2_battleship_health")
    print "Obstacle (ID = 1) position:", B.get_obstacle_position(1)
    print "Obstacle (ID = 2) position:", B.get_obstacle_position(2)
    print

    # Formatting errors
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
    try:
        B.init_ship(1, "Battleship", [1, 1], 100)
        print "Failed to protect private Board methods"
    except:
        print "Caught attempted call to private Board method"
    try:
        Board(-20, 20, 10, [1, 1, 0], [3, 4, 5], [10, 12, 0], [15, 15, 2])
        print "Failed to catch invalid input parameters to Board()"
    except:
        print "Caught invalid inputs to Board()"
    try:
        Board(20, 20, 0, [1, 1, 0], [3, 4, 5], [10, 12, 0], [15, 15, 2])
        print "Failed to catch invalid input parameters to Board()"
    except:
        print "Caught invalid inputs to Board()"
    try:
        Board(-20, 20, 10, [1, 1, 10], [3, 4, 5], [10, 12, 0], [15, 15, 2])
        print "Failed to catch invalid input parameters to Board()"
    except:
        print "Caught invalid inputs to Board()"
    try:
        Board(-20, 20, 10, [1, 1, 0], [3, 4, -5], [10, 12, 0], [15, 15, 2])
        print "Failed to catch invalid input parameters to Board()"
    except:
        print "Caught invalid inputs to Board()"
    try:
        Board(-20, -20, -10, [-1, -1, -0], [-3, -4, -5], [-10, -12, -0], \
            [-15, -15, -2])
        print "Failed to catch invalid input parameters to Board()"
    except:
        print "Caught invalid inputs to Board()"
    try:
        B.move_ship(1, "Battleship", [-1, 2, 3])
        print "Failed to catch invalid move"
    except:
        print "Caught invalid move"
    try:
        B.move_ship(1, "Battleship", [1, 1, 0])
        print "Failed to catch attempted non-move"
    except:
        print "Caught attempted non-move"
    try:
        B.destroy_obstacle([0, 0, 0])
        print "Failed to catch invalid obstacle location"
    except:
        print "Caught invalid obstacle location"
    print

    # expose()
    print "Checking 'expose' correctness (by visual inspection)..."
    print ("Expect only 'board_height', 'team1_submarine' and \
        'team2_battleship_health':", B.expose(["board_height", \
            "team1_submarine", "team2_battleship_health"]))
    print "Expect only 'obstacles':", B.expose(["obstacles"])
    print "Expect only 'team2_battleship':", B.expose(["team2_battleship"])
    print "Expect nothing:", B.expose([])
    print

    # hit_ship()
    print "Testing hit_ship()...",
    B.hit_ship(1, "Battleship", 60)
    assert(B.get_attribute("team1_battleship_health") == 40)
    B.hit_ship(2, "Submarine", 120)
    assert(B.get_attribute("team2_submarine_health") == 0)
    assert(B.ship_is_sunk(2, "Submarine"))
    print "works as expected"
    print

    # move_ship()
    print "Testing move_ship()...",
    B.move_ship(1, "Submarine", [4, 5, 7])
    assert(B.ship_position(1, "Submarine") == [4, 5, 7])
    print "works as expected"
    print

    # location_occupied()
    print "Testing location_occupied()...",
    assert(B.location_occupied([5, 6, 4]))
    assert(B.location_occupied([1, 1, 0]))
    assert(not B.location_occupied([0, 0, 0]))
    assert(not B.location_occupied([5, 6, 3]))
    print "works as expected"
    print

    # destroy_obstacle()
    print "Testing destroy_obstacle()...",
    B.destroy_obstacle([10, 10, 0])
    B.destroy_obstacle([5, 6, 4])
    new_board = json.loads(B.current_board())
    assert(new_board["obstacles"] == [])
    print "works as expected"
    print

    print "All tests ran to completion successfuly."

################################################################################
################################################################################

def main():
    test()

main()