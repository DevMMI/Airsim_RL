import numpy as np
import time
from math import sqrt
import cv2
from pylab import array, arange, uint8
from PIL import Image
import eventlet
from eventlet import Timeout
import multiprocessing as mp
# Change the path below to point to the directoy where you installed the AirSim PythonClient
#sys.path.append('C:/Users/Kjell/Google Drive/MASTER-THESIS/AirSimpy')

from AirSimClient import *


class myAirSimClient(MultirotorClient):

    def __init__(self):
        self.img1 = None
        self.img2 = None

        MultirotorClient.__init__(self)
        MultirotorClient.confirmConnection(self)
        self.enableApiControl(True)
        self.armDisarm(True)

        self.home_pos = self.getPosition()

        self.home_ori = self.getOrientation()

        self.z = -6

    def straight(self, duration, speed):
        pitch, roll, yaw  = self.getPitchRollYaw()
        vx = math.cos(yaw) * speed
        vy = math.sin(yaw) * speed
        self.moveByVelocityZ(vx, vy, self.z, duration, DrivetrainType.ForwardOnly)
        start = time.time()
        return start, duration

    def yaw_right(self, duration):
        self.rotateByYawRate(30, duration)
        start = time.time()
        return start, duration

    def yaw_left(self, duration):
        self.rotateByYawRate(-30, duration)
        start = time.time()
        return start, duration


    def take_action(self, action):
        # necessary
        ''' takes action and returns current position, whether collided, current velocity '''

        # get position
        vehicle_pose = client.simGetVehiclePose().position
        pose_x = vehicle_pose.x_val
        pose_y = vehicle_pose.y_val
        pose_z = vehicle_pose.z_val

        # get velocity
        vehicle_linear_vel = self.simGetGroundTruthKinematics().linear_velocity
        vehicle_vel = sqrt(vehicle_linear_vel.x_val**2 + vehicle_linear_vel.y_val**2)

        # get collision occurrence
        collided = False
        collision_info = self.simGetCollisionInfo()
        if collision_info.has_collided:
           collided = True



    def goal_direction(self, goal, pos):

        pitch, roll, yaw  = self.getPitchRollYaw()
        yaw = math.degrees(yaw)

        pos_angle = math.atan2(goal[1] - pos.y_val, goal[0]- pos.x_val)
        pos_angle = math.degrees(pos_angle) % 360

        track = math.radians(pos_angle - yaw)

        return ((math.degrees(track) - 180) % 360) - 180


    def getObservation(self):
        # get image as floating point pixel values
        responses = self.simGetImages([ImageRequest("front_center", airsim.ImageType.Scene, True, False)])
        response = responses[0]
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)

        # normalizing and reshaping image
        img1d = (img1d - np.mean(img1d, axis=0)) / np.std(img1d, axis=0)
        img_fp *= (1.0/img_rgba.max()) # normalize pixels between 0 and 1
        img_fp = img1d.reshape(response.height, response.width)
        img_fp = np.flipud(img_rgba) # flip upside down

        return img_fp

    def resetEnv(self):

        self.reset()
        time.sleep(0.2)
        self.enableApiControl(True)
        self.armDisarm(True)
        time.sleep(1)
        self.moveToZ(self.z, 3)
        time.sleep(3)
