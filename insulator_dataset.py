import numpy as np
import skimage.draw
import skimage.io
import json
import os
from Mask_RCNN.mrcnn import utils


class InsulatorDataset(utils.Dataset):

    def load_dataset(self, dataset_dir):
        self.add_class("dataset", 1, "insulator")
        images_dir = dataset_dir
        annotations = json.load(
            open(os.path.join(dataset_dir, "via_project.json")))
        annotations = list(annotations.values())

        for a in annotations:
            if 'regions' in a and a['regions']:
                polygons = [r['shape_attributes'] for r in a['regions']]
                image_path = os.path.join(images_dir, a['filename'])
                image = skimage.io.imread(image_path)
                height, width = image.shape[:2]

                self.add_image(
                    "dataset",
                    image_id=a['filename'],
                    path=image_path,
                    width=width, height=height,
                    polygons=polygons)

    def load_mask(self, image_id):
        info = self.image_info[image_id]
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            mask[rr, cc, i] = 1
        return mask.astype(np.bool), np.ones([mask.shape[-1]], dtype=np.int32)
