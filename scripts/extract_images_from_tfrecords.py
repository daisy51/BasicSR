"""Read tfrecords w/o define a graph.

Ref:
http://warmspringwinds.github.io/tensorflow/tf-slim/2016/12/21/tfrecords-guide/
"""

import glob
import os

import cv2
import numpy as np


def celeba_tfrecords():
    # Configurations
    file_pattern = '/home/xtwang/datasets/CelebA_tfrecords/celeba-full-tfr/train/train-r08-s-*-of-*.tfrecords'  # noqa:E501
    # r08: resolution 2^8 = 256
    resolution = 128
    save_path = f'/home/xtwang/datasets/CelebA_tfrecords/tmptrain_{resolution}'

    save_all_path = os.path.join(save_path, f'all_{resolution}')
    os.makedirs(save_all_path)

    idx = 0
    print(glob.glob(file_pattern))
    for record in glob.glob(file_pattern):
        record_iterator = tf.python_io.tf_record_iterator(record)
        for string_record in record_iterator:
            example = tf.train.Example()
            example.ParseFromString(string_record)
            # label = example.features.feature['label'].int64_list.value[0]

            # attr = example.features.feature['attr'].int64_list.value
            # male = attr[20]
            # young = attr[39]

            shape = example.features.feature['shape'].int64_list.value
            h, w, c = shape
            img_str = example.features.feature['data'].bytes_list.value[0]
            img = np.fromstring(img_str, dtype=np.uint8).reshape((h, w, c))

            # save image
            img = img[:, :, [2, 1, 0]]
            cv2.imwrite(
                os.path.join(save_all_path, '{:06d}.png'.format(idx)), img)

            idx += 1
            print(idx)


if __name__ == '__main__':
    try:
        import tensorflow as tf
    except Exception:
        raise ImportError('You need to install tensorflow to read tfrecords.')
    celeba_tfrecords()
