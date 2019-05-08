from gym_ergojr import get_scene
from gym_ergojr.utils.pybullet import DistanceBetweenObjects
from gym_ergojr.utils.urdf_helper import URDF
import pybullet as p
import numpy as np


class Ball(object):

    def __init__(self, scaling=0.02):
        self.scaling = scaling
        xml_path = get_scene("ball")
        self.ball_file = URDF(xml_path, force_recompile=False).get_path()
        self.hard_reset()

    def changePos(self, new_pos, speed=1):
        p.changeConstraint(
            self.ball_cid, new_pos, maxForce=25000 * self.scaling * speed)

    def hard_reset(self):
        startOrientation = p.getQuaternionFromEuler([0, 0, 0])
        self.id = p.loadURDF(
            self.ball_file, [0, 0, .5],
            startOrientation,
            useFixedBase=0,
            globalScaling=self.scaling)
        self.ball_cid = p.createConstraint(
            self.id,
            -1,
            -1,
            -1,
            p.JOINT_FIXED,
            jointAxis=[0, 0, 0],
            parentFramePosition=[0, 0, 0],
            childFramePosition=[0, 0, 0])
        p.changeConstraint(
            self.ball_cid, [0, 0, 0.1], maxForce=25000 * self.scaling)


class Puck(object):

    def __init__(self, friction=.4):
        self.friction = friction

        self.puck = None
        self.dbo = None
        self.target = None
        self.goal = None
        self.obj_visual = None

        xml_path = get_scene("ergojr-pusher-puck")
        self.robot_file = URDF(xml_path, force_recompile=True).get_path()

        # # GYM env has to do this
        # self.hard_reset()

    def add_puck(self):
        self.puck = p.loadURDF(
            self.robot_file, [
                np.random.uniform(-0.08, -0.14),
                np.random.uniform(0.05, 0.1), 0.0
            ],
            p.getQuaternionFromEuler([0, 0, 0]),
            useFixedBase=1)

        for joint in [0, 1]:
            p.setJointMotorControl2(
                self.puck,
                joint,
                p.VELOCITY_CONTROL,
                force=self.friction,
                targetVelocity=0)

        self.dbo = DistanceBetweenObjects(self.puck, 1)

    def reset(self):
        if self.puck is not None:
            p.removeBody(self.puck)

        self.add_puck()

        if self.target is not None:
            p.removeBody(self.target)

        self.add_target()

    def hard_reset(self):
        self.add_puck()
        self.obj_visual = p.createVisualShape(
            p.GEOM_CYLINDER, radius=0.02, length=0.01, rgbaColor=[0, 1, 0, 1])
        self.add_target()

    def add_target(self):
        self.dbo.goal = np.array(
            [np.random.uniform(-.30, -.1),
             np.random.uniform(-.3, .1), 0])

        self.target = p.createMultiBody(
            baseVisualShapeIndex=self.obj_visual, basePosition=self.dbo.goal)
