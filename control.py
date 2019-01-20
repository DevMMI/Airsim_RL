# ready to run example: PythonClient/multirotor/hello_drone.py
import airsim
import os
import numpy as np
# connect to the AirSim simulator
dir_path = os.path.dirname(os.path.realpath(__file__))

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Async methods returns Future. Call join() to wait for task to complete.
client.takeoffAsync().join()
#client.moveToPositionAsync(-10, 10, -10, 5).join()
client.hoverAsync().join()

# collision api
action = 19 * np.random.random_sample((1,20)) + 1


client.moveByVelocityAsync(action[0,0], action[0,1], 0, 1.0).join()
done = 0
print("reached beginning of loop")
while done<150:
    done += 1

    # Getting collision info API
    collision_info = client.simGetCollisionInfo()
    #if collision_info.has_collided:
    #    print("Collision at pos {}".format(collision_info.position))


    # Grabbing an image API
    responses = client.simGetImages([airsim.ImageRequest("front_center", airsim.ImageType.Scene, False, False)])
    response = responses[0]
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
    img_rgba = img1d.reshape(response.height, response.width, 4)
    img_rgba = np.flipud(img_rgba)

    # saving image
    file = "pic" + str(done) + ".png"
    name = os.path.join(dir_path, "temp_images", file)
    print("name {}".format(name))
    airsim.write_png(name, img_rgba)

client.hoverAsync().join()

        #break
# take images
# responses = client.simGetImages([
#     airsim.ImageRequest("0", airsim.ImageType.DepthVis),
#     airsim.ImageRequest("1", airsim.ImageType.DepthPlanner, True)])
# print('Retrieved images: %d', len(responses))
#
# # do something with the images
# for response in responses:
#     if response.pixels_as_float:
#         print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
#         airsim.write_pfm(os.path.normpath('./temp/py1.pfm'), airsim.getPfmArray(response))
#     else:
#         print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
#         airsim.write_file(os.path.normpath('./temp/py1.png'), response.image_data_uint8)
