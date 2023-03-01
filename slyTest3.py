import numpy as np
import os
import os.path as osp
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud


# Specify the NuScenes dataset location and version:
nuscenes = NuScenes(version='v1.0-mini', dataroot='/data/sets/nuscenes', verbose=True)

# Specify the output directory for the extracted point clouds:
out_path = '/output/'
if not os.path.exists(out_path):
    os.makedirs(out_path)


def get_cars_pcs():
    # Specify the classes of objects to extract (in this case, we only want cars):
    classes = ['vehicle.car']

    # Loop through each scene in the dataset and get the sample data:
    for scene in nuscenes.scene:
        scene_data = nuscenes.get('scene', scene['token'])
        sample_data = nuscenes.get('sample', scene_data['first_sample_token'])

        # Load the annotation data:
        for annotation_token in sample_data['anns']:
            annotation_data = nuscenes.get('sample_annotation', annotation_token)
            # Check if the annotation is of the desired class:
            if annotation_data['category_name'] in classes:
                # Load the point cloud:
                points = nuscenes.get('sample_data', sample_data['data']['LIDAR_TOP'])
                pc = LidarPointCloud.from_file(osp.join(nuscenes.dataroot, points['filename']))

                # Convert the point cloud to a numpy array and save:
                points_array = pc.points
                name = points['filename'].split('/')[-1].split('.')[0]
                np.savetxt(f'{out_path}/{name}.ply', points_array)


if __name__ == "__main__":
    get_cars_pcs()


