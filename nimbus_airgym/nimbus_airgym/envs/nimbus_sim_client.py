
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
        action = action * 20.0 # denormalize action
        #print("{} {}".format(action[0], action[1]))
        #exit(0)
        self.moveByVelocityAsync(float(action[0]), float(action[1]), float(0.0), float(0.3)).join()
        #self.moveByVelocityAsync(1.0, 1.0, 0.0, 0.3).join()

        # get position
        vehicle_pose = self.simGetVehiclePose().position
        pose_x = vehicle_pose.x_val
        pose_y = vehicle_pose.y_val
        pose_z = vehicle_pose.z_val
        pose = Vector3r(pose_x, pose_y, pose_z)

        # get velocity
        vehicle_linear_vel = self.simGetGroundTruthKinematics().linear_velocity
        vehicle_vel = sqrt(vehicle_linear_vel.x_val**2 + vehicle_linear_vel.y_val**2)

        # get collision occurrence
        collided = False
        collision_info = self.simGetCollisionInfo()
        if collision_info.has_collided:
           collided = True

        return collided, pose, vehicle_vel


    def getObservation(self):
        # get image as floating point pixel values
        try:
            responses = self.simGetImages([ImageRequest("front_center", ImageType.Scene, True, False)])
            response = responses[0]


            #img1d = np.fromstring(''.join(response.image_data_float), dtype=np.float32)
            img1d = np.array(response.image_data_float, dtype=np.float32)

            # normalizing and reshaping image
            std_fp = np.std(img1d, axis=0)
            if(std_fp == 0):
                std_fp = np.ones(img1d.shape[0])
            img_fp = (img1d - np.mean(img1d, axis=0)) / std_fp
            max_fp = img_fp.max()
            if(max_fp == 0):
                max_fp = 1.0
            img_fp *= (1.0/max_fp) # normalize pixels between 0 and 1
            img_fp = img_fp.reshape(response.height, response.width, 1)
            img_fp = np.flipud(img_fp) # flip upside down

            return img_fp
        except:
            return np.zeros((1,1))

    def resetEnv(self):
        self.reset()
        print("post reset")
        self.enableApiControl(True)
        self.armDisarm(True)
        self.moveToZAsync(-3, 2).join()
