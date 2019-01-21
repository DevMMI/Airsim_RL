import logging as log
import numpy as np
import random

import gym
from gym import spaces
from gym.utils import seeding
from gym.spaces import Tuple, Box, Discrete, MultiDiscrete, Dict
from gym.spaces.box import Box

from gym_airsim.envs.myAirSimClient import *

from AirSimClient import *



class ForestEnv(gym.Env):

    airgym = None

    def __init__(self):
        # necessary
        # left depth, center depth, right depth, yaw
        # necessary
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(144, 256))
        self.state = np.zeros((144, 256), dtype=np.float16)

        # necessary
        self.action_space = spaces.Box(low=0.0, high=1.0, shape=(2))

        self.goal = 	[221.0, -9.0] # global xy coordinates


        self.episodeN = 0
        self.stepN = 0

        self._seed()

        global airgym
        airgym = myAirSimClient()


    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def computeReward(self, now, track_now):

		# test if getPosition works here liek that
		# get exact coordiantes of the tip

        distance_now = np.sqrt(np.power((self.goal[0]-now.x_val),2) + np.power((self.goal[1]-now.y_val),2))


        r = -1


        r = r + (distance_before - distance_now)

        return r, distance_now


    def _step(self, action):
        # necessary
        ''' takes action, environment returns an observation and reward,
            returns observation, reward, done and info values '''
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        (collided, position, velocity) = airgym.take_action(action)
        reward = self.computeReward(collided, position, velocity)



        # Terminate the episode on large cumulative amount penalties,
        # since drone probably got into an unexpected loop of some sort
        if rewardSum < -100:
            done = True

        sys.stdout.write("\r\x1b[K{}/{}==>reward/depth: {:.1f}/{:.1f}   \t {:.0f}  {:.0f}".format(self.episodeN, self.stepN, reward, rewardSum, track, action))
        sys.stdout.flush()

        info = {"x_pos" : now.x_val, "y_pos" : now.y_val}
        self.state = airgym.getObservation()

        return self.state, reward, done, info

    def _reset(self):
        # necessary
        """
        Resets the state of the environment and returns an initial observation.

        # Returns
            observation (object): The initial observation of the space. Initial reward is assumed to be 0.
        """
        airgym.resetEnv()

        self.stepN = 0
        self.episodeN += 1



        print("")

        now = airgym.getPosition()
        track = airgym.goal_direction(self.goal, now)
        self.state = airgym.getObservation

        return self.state
