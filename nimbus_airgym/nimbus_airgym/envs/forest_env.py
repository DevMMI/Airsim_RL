
import gym
import logging as log
import numpy as np
from gym import spaces
from gym.spaces import Dict
from gym.spaces.box import Box
from nimbus_airgym.envs.nimbus_sim_client import *
from math import sqrt
#from AirSimClient import *
from airsim import *


class ForestEnv(gym.Env):

    airgym = None
    ceiling = -25
    radius = 30

    def __init__(self):
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(144, 256))
        self.state = np.zeros((144, 256), dtype=np.float16)
        self.action_space = spaces.Box(low=0.0, high=1.0, shape=(2))
        self.episodeN = 0
        self.stepN = 0

        global airgym
        airgym = NimbusSimClient()

    def _step(self, action):
        ''' takes action, environment returns an observation and reward,
            returns observation, reward, done and info values '''
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        (collided, position, velocity) = airgym.takeAction(action)
        reward = self.computeReward(collided, position, velocity)

        self.state = airgym.getObservation()

        return self.state, reward, done, {}

    def _reset(self):
        """
        Resets the state of the environment and returns an initial observation.

        # Returns
            observation (object): The initial observation of the space. Initial reward is assumed to be 0.
        """
        self.stepN = 0
        self.episodeN += 1

        airgym.resetEnv()
        self.state = airgym.getObservation
        return self.state

    def computeReward(self, collided, position, velocity):
        distance = sqrt(position.x_val**2 + position.y_val**2)
        if collided:
            return -50
        if position.z_val < ceiling or distance > radius:
            return -5
        else:
            return 5
