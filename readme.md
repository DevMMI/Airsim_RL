# Documentation for some good resources for our project #

## Airsim C++ executables ##
AirSim/build_debug/output/bin

## How to quit execution of a python script without crashing unreal engine
ctrl+z on python script

$ps #to find the process id of script

$kill -9 <process id>
  
then end the Airsim run

  
## A good example of what settings should look like ##
https://github.com/Microsoft/AirSim/blob/master/docs/settings.md

## Drone API source is located ##
AirSim/Unreal/Plugins/AirSim/Source/AirLib/(src/include)/vehicles/multirotor/
AirSim/Unreal/Plugins/AirSim/Source/AirLib/(src/include)/api/

## An image request is formatted ##
ImageRequest(const std::string& camera_name_val, ImageCaptureBase::ImageType image_type_val, bool pixels_as_float_val = false, bool compress_val = true)

## D4PG

### Continue Training from Checkpoint Issue

After running a training session once and re-running, not continuing from last checkpoint. Tracing the issue:

*  In *D4PG/settings.py* we have `LOAD = True`.
*  In *utils/Saver.py* we have load function. Called in *D4PG/main.py* and our "model is loaded".
*  Probably need to look into `self.saver.restore(self.sess, ckpt.model_checkpoint_path)` and make sure it is behaving as intended.
*  With regards to saving, appears to be working fine. Under *D4PG\model* there is the *checkpoint* file with `model_checkpoint_path:` and `all_model_checkpoint_paths:` inside. There are also *.ckpt* files in the same folder which I assume are the weights/ checkpoints.
