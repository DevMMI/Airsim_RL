# Documentation for some good resources for our project #

## Airsim C++ executables ##
AirSim/build_debug/output/bin

## A good example of what settings should look like ##
https://github.com/Microsoft/AirSim/blob/master/docs/settings.md

## Drone API source is located ##
AirSim/Unreal/Plugins/AirSim/Source/AirLib/(src/include)/vehicles/multirotor/
AirSim/Unreal/Plugins/AirSim/Source/AirLib/(src/include)/api/

## An image request is formatted ##
ImageRequest(const std::string& camera_name_val, ImageCaptureBase::ImageType image_type_val, bool pixels_as_float_val = false, bool compress_val = true)
