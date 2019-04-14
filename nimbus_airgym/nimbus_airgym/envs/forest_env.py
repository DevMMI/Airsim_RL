
import gym
import logging as log
import numpy as np
from gym import spaces
from gym.spaces import Dict
from gym.spaces.box import Box
from nimbus_airgym.envs.nimbus_sim_client import *
import math
from math import sqrt
#from AirSimClient import *
from airsim import *


class ForestEnv(gym.Env):

    airgym = None


    def __init__(self):
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(144, 256, 1), dtype=np.float16)
        self.state = np.zeros((144, 256, 1), dtype=np.float16)
        self.action_space = spaces.Box(low=-50.0, high=50.0, shape=(1, 2), dtype=np.float16)
        self.episodeN = 0
        self.stepN = 0
        self.ceiling = -25
        self.radius = 60

        global airgym
        airgym = NimbusSimClient()

    def step(self, action):
        ''' takes action, environment returns an observation and reward,
            returns observation, reward, done and info values '''
        action = action[0]

        collided, position, velocity = airgym.takeAction(action)
        reward = self.computeReward(collided, position, velocity)

        self.state = airgym.getObservation()
        if(self.state.max() == 0.0):
            return self.state, reward, 0.0, {}, 1

        return self.state, reward, 0.0, {}, 0

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        """
        Resets the state of the environment and returns an initial observation.

        # Returns
            observation (object): The initial observation of the space. Initial reward is assumed to be 0.
        """

        self.stepN = 0
        self.episodeN += 1

        airgym.resetEnv()
        self.state = airgym.getObservation()
        return self.state

    def computeReward(self, collided, position, velocity):
        global ceiling
        distance = sqrt(position.x_val**2 + position.y_val**2)
        if collided:
            return 50.0
        else:
            reward = -10
        reward = 0

        # velocity greater than 0 is favored, peaks around 20
        #reward += 10.0 * math.tanh(0.1 * velocity)
        #reward += velocity
        #reward = 5

        reward += (0.5 * distance)
        # reward as drone goes further above ceiling
        # if position.z_val < self.ceiling:
        #     difference = float(self.ceiling - position.z_val)
        #     # more positive difference is worse
        #     reward += (-50.0 * math.tanh(0.05 * difference))
        #
        #
        # if distance > self.radius:
        #     difference = distance - self.radius
        #     # more positive difference is worse
        #     reward += (-50 * math.tanh(0.05 * difference))

        return reward
