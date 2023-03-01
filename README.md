# SuperwiselyTestTasks
Solutions for Supervisely test tasks for the Python Developer role.

## Task №1: "Write two split and merge scripts. The split script accepts an image, window size (h, w) in pixels or percent, offset by x and y, and slices images with sliding window approach. The result is saved in a directory - all the settings must be saved in the names of the resulting images. The merge script takes a folder of sliced images as input and assembles thethe original one. In the end it is necessary to verify that the pixels of the result are exactly the same as in the original image."

### Solution:
I used the PIL library to solve this problem. The logic behind it is as follows: the split script checks the presence of a given file, if the window size is given in percentages, converts them into pixels, checks that the window size does not go beyond the image and, using the crop() method, iterates over the horizontal and vertical coordinates of the image and slices the image into many smaller ones. For each window position, the code generates a unique filename for the corresponding patch, based on the input image filename and the window coordinates.<br>
![Screenshot 2023-03-01 154701](https://user-images.githubusercontent.com/56644580/222130768-6941f943-ff9b-40ff-84b2-706bc5e13899.jpg)<br>
The merge script creates a blank image of size and mode based on the original image. using the paste method the script assembles the original image from the pieces based on the data stored in the name of the pieces and then checks both images with ImageChops.difference(). The image is restored without pixel changes only if the slices and the image itself are saved in png format without compression, so the merged image size is more than that of the original.
#### Time spent: ~3.5 hrs.
<br>

## Task №2: "Write a visualiser for the DAVIS dataset. The script should produce a result like this - take N videos and stitch them together one after the other or in a grid like this."

### Solution:
For this one, I downloaded TrainVal dataset from the DAVISChallenge website (<href>https://data.vision.ee.ethz.ch/csergi/share/davis/DAVIS-2017-trainval-480p.zip</href>) and unpaked it in the folder with script.<br>
So, the logic behind this one is as follows. We have a folder with the original frames, and corresponding "masks" with colour object. First of all, using the PIL library, I merged these images by applying masks over the original frames using the blend() method and saved the resulting frames in a separate directory without disturbing the folder view. <br>
The main problem is that the contrast of a frame changes during merging using this method.
The composite() method doesn't have this problem, but the mask became not sufficiently visible.<br>
Also, the frames are saved with a loss of quality in jpg format, so to save the quality it is necessary to change the extension to png format and sacrifice the running time.<br>
Then, using the OpenCV library, I assembled the resulting frames into a total video in 30 fps, consisting of video segments.
#### Time spent: ~3 hrs
<br>

## Task №3: "Take any public dataset with 3d point clouds with cars marked on them (e.g. waymo, nuscenes or kitti3d). Write a script which, using the markup of the cars as cuboids, cuts them out of the original point cloud and saves them as separate point clouds."

### Solution:
This one was quite tricky because you need the knowledge of pointclouds.
After researching I choose to use nuScenes dataset mini <href>https://www.nuscenes.org/download</href> and their devkit <href>https://github.com/nutonomy/nuscenes-devkit</href>.
Using their example scripts <href>https://github.com/nutonomy/nuscenes-devkit/tree/master/python-sdk/nuscenes/scripts</href> I believe I`ve managed to create a solution for the task.<br>
That being said, the logic of the solution is as follows: The script goes through all scenes in the dataset, filters the data by class "vehicles" and finds point clouds by LIDAR_TOP category. Then using the method LidarPointCloud.from_file() we get an array of points and write it to a new file. 
#### Time spent: ~2.5 hrs
