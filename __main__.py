r"""
This script is used to have colorply access from the commandline.
Simply run

```python
$ python colorply
```

You can add additionnal arguments, like so

```python
$ python colorply --my_argument
```

The available argument are:
* interface
* inply
* outply
* calib
* oridir
* imdir
* imext
* channel
* mode
"""

import argparse
import colorply
from colorply.ui import interface

if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Colorply - Multispectral photogrammetry add-on for MicMac 3D")
    args.add_argument("-i", "--interface", default=False,
                      type=bool, help="Launch colorply interface")
    args.add_argument("-iply", "--inply",
                      default="colorply/test/data/result/RVB_GRE.ply",
                      type=str, help="Path to the 3D model to add a channel")
    args.add_argument("-oply", "--outply",
                      default="output.ply",
                      type=str, help="Name of the resulting ply model")
    args.add_argument("-c", "--calib",
                      default="colorply/test/data/calibration/Ori-1bande_All_CampariGCP/AutoCal_Foc-4000_Cam-SequoiaSequoia-GRE.xml",
                      type=str, help="Path to the camera calibration used to generate the initial ply file")
    args.add_argument("-o", "--oridir",
                      default="colorply/test/data/calibration/Ori-1bande_All_CampariGCP",
                      type=str, help="Path to the image orientation folder used to generate the initial ply file")
    args.add_argument("-imd", "--imdir",
                      default="colorply/test/data/images/NIR",
                      type=str, help="Path to the images used to generate the initial ply file")
    args.add_argument("-e", "--imext",
                      default="TIF",
                      type=str, help="Extension of the images used to generate the initial ply file")
    args.add_argument("-ch", "--channel",
                      default="unk",
                      type=str, help="Name of the channel, corresponding to the image wavelength in `imdir`")
    args.add_argument("-m", "--mode",
                      default="avg",
                      type=str, help="Mode to merge new radiometry")

    args = args.parse_args()

    # Main core
    if args.interface:
        interface()

    else:
        input_ply = args.inply
        output_ply = args.outply
        calibration_file = args.calib
        orientation_dir = args.oridir
        image_dir = args.imdir
        image_ext = args.imext
        channel = args.channel
        mode = args.mode

        colorply.add_cloud_channel(input_ply,
                                   output_ply,
                                   calibration_file,
                                   orientation_dir,
                                   image_dir,
                                   image_ext=image_ext,
                                   channel=channel,
                                   mode=mode)
