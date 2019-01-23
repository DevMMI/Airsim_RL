
import numpy as np
from math import sqrt
from airsim import *
#from AirSimClient import *


class NimbusSimClient(MultirotorClient):

    def __init__(self):
        MultirotorClient.__init__(self)
        MultirotorClient.confirmConnection(self)
        self.enableApiControl(True)
        self.armDisarm(True)

    def takeAction(self, action):
        ''' takes action and returns current position, whether collided, current velocity '''
        # take action
        self.moveByVelocityAsync(action[0], action[1], 0, 1.0).join()

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
        client.reset()
        print("post reset")
        client.enableApiControl(True)
        client.armDisarm(True)
        client.moveToZAsync(-3, 2).join()
