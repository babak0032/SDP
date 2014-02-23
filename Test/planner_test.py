import unittest
from planning.models import Vector
from planning.planner import *
from numpy.testing import assert_almost_equal


class TestYPredictionLeft(unittest.TestCase):

    def setUp(self):
        self.planner = Planner('left')
        self.our_goal = self.planner._world.our_goal
        self.their_attacker = self.planner._world.their_attacker
        self.pitch = self.planner._world._pitch

    def test_straight_shot(self):
        # Shot to the center:
        self.their_attacker.vector = Vector(200, self.our_goal.y, pi, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), self.our_goal.y)
        # Shot to the bottom:
        goal_top = self.our_goal.y - (self.our_goal.width/2)
        self.their_attacker.vector = Vector(200, goal_top, pi, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), goal_top)

    def test_straight_corrected_shot(self):
        # Shot above the top:
        goal_top = self.our_goal.y + (self.our_goal.width/2)
        self.their_attacker.vector = Vector(200, goal_top + 20, pi, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), goal_top)
        # Shot below the bottom:
        goal_bottom = self.our_goal.y - (self.our_goal.width/2)
        self.their_attacker.vector = Vector(200, goal_bottom - 20, pi, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), goal_bottom)

    def test_angle_shot(self):
        # Shot above the center:
        self.their_attacker.vector = Vector(50, self.our_goal.y, (3*pi)/4, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), self.our_goal.y + 50)
        # Shot below the center:
        self.their_attacker.vector = Vector(50, self.our_goal.y, (5*pi)/4, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), self.our_goal.y - 50)

    def test_bounce_shot(self):
        # Shot bounced of the top:
        self.their_attacker.vector = Vector(self.pitch.height, self.pitch.height/2, (3*pi)/4, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), self.pitch.height/2)
        # Shot bounced of the bottom:
        self.their_attacker.vector = Vector(self.pitch.height, self.pitch.height/2, (5*pi)/4, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), self.pitch.height/2)
        # Shot bounced of the top that needs to be corrected:
        goal_top = self.our_goal.y + (self.our_goal.width/2)
        self.their_attacker.vector = Vector(self.pitch.height/2, self.pitch.height/2, (13*pi)/16, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), goal_top)

    def test_no_intersection(self):
        self.their_attacker.vector = Vector(self.pitch.height, self.pitch.height/2, pi/4, 0)
        self.assertEqual(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), None)


class TestYPredictionRight(unittest.TestCase):

    def setUp(self):
        self.planner = Planner('right')
        self.our_goal = self.planner._world.our_goal
        self.their_attacker = self.planner._world.their_attacker
        self.pitch = self.planner._world._pitch

    def test_straight_shot(self):
        # Shot to the center:
        self.their_attacker.vector = Vector(400, self.our_goal.y, 0, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), self.our_goal.y)
        # Shot to the bottom:
        goal_top = self.our_goal.y - (self.our_goal.width/2)
        self.their_attacker.vector = Vector(400, goal_top, 0, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), goal_top)

    def test_straight_corrected_shot(self):
        # Shot above the top:
        goal_top = self.our_goal.y + (self.our_goal.width/2)
        self.their_attacker.vector = Vector(200, goal_top + 20, 0, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), goal_top)
        # Shot below the bottom:
        goal_bottom = self.our_goal.y - (self.our_goal.width/2)
        self.their_attacker.vector = Vector(200, goal_bottom - 20, 0, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), goal_bottom)
    
    def test_angle_shot(self):
        # Shot above the center:
        self.their_attacker.vector = Vector(self.pitch.width - 50, self.our_goal.y, pi/4, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), self.our_goal.y + 50)
        # Shot below the center:
        self.their_attacker.vector = Vector(self.pitch.width - 50, self.our_goal.y, (7*pi)/4, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), self.our_goal.y - 50)

    def test_bounce_shot(self):
        # Shot bounced of the top:
        self.their_attacker.vector = Vector(self.pitch.width - self.pitch.height, self.pitch.height/2, pi/4, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), self.pitch.height/2)
        # Shot bounced of the bottom:
        self.their_attacker.vector = Vector(self.pitch.width - self.pitch.height, self.pitch.height/2, (7*pi)/4, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), self.pitch.height/2)
        # Shot bounced of the top that needs to be corrected:
        goal_top = self.our_goal.y + (self.our_goal.width/2)
        self.their_attacker.vector = Vector(self.pitch.width - (self.pitch.height/2), self.pitch.height/2, (5*pi)/16, 0)
        assert_almost_equal(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), goal_top)

    def test_no_intersection(self):
        self.their_attacker.vector = Vector(self.pitch.height, self.pitch.height/2, (3*pi)/4, 0)
        self.assertEqual(self.planner.predict_y_intersection(self.our_goal, self.their_attacker), None)