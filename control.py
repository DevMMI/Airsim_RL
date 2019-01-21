# API examples
import airsim
import os
import numpy as np
import time
from math import sqrt
dir_path = os.path.dirname(os.path.realpath(__file__))

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Async methods returns Future. Call join() to wait for task to complete.
client.takeoffAsync().join()
client.hoverAsync().join()

# collision api
action = 19 * np.random.random_sample((1,20)) + 1


client.moveByVelocityAsync(action[0,0], action[0,1], 0, 1.0).join()
done = 0
count = 100
print("reached beginning of loop")
while done < count:
    done += 1

    # Getting collision info API
    collision_info = client.simGetCollisionInfo()
    #if collision_info.has_collided:
    #    print("Drone has collided}")


    # Grabbing an image API
    responses = client.simGetImages([airsim.ImageRequest("front_center", airsim.ImageType.Scene, False, False)])
    response = responses[0]
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
    img_rgba = img1d.reshape(response.height, response.width, 4)
    img_rgba = np.flipud(img_rgba)

    # Saving image API
    file = "pic" + str(done) + ".png"
    name = os.path.join(dir_path, "temp_images", file)
    airsim.write_png(name, img_rgba)

    # Finding position api
    #api Pose simGetVehiclePose(const std::string& vehicle_name = "") const;
    vehicle_pose = client.simGetVehiclePose().position
    vehicle_orientation = client.simGetVehiclePose().orientation
    #print("Pose is x {}, y {}, z {}".format(vehicle_pose.x_val, vehicle_pose.y_val, vehicle_pose.z_val))

    # Find velocity API
    vehicle_linear_vel = client.simGetGroundTruthKinematics().linear_velocity
    vehicle_vel = sqrt(vehicle_linear_vel.x_val**2 + vehicle_linear_vel.y_val**2)
    #print("Velocity is {}".format(vehicle_vel))
    # Resetting to origin api
    if done == 50:
        client.moveByVelocityAsync(0, 0, 0, 1.0).join()

         #% 10 == 0:

    #     print("Resetting zero")
    #     client.reset()
    #     print("post reset")
    #     client.enableApiControl(True)
    #     client.armDisarm(True)
    #     client.moveByVelocityAsync(action[0,0], action[0,1], 0, 1.0).join()

client.hoverAsync().join()
