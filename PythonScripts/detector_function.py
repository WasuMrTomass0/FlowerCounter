import numpy as np
# import os
# import six.moves.urllib as urllib
# import sys
# import tarfile
import tensorflow as tf
# import zipfile
# from collections import defaultdict
# from io import StringIO
# from matplotlib import pyplot as plt
from PIL import Image
from IPython.display import display

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Wczytanie modelu sieci
detection_model = tf.saved_model.load(f"{PATH_INF_GRAPH}/saved_model")
# Wczytanie label_map
category_index = label_map_util.create_category_index_from_labelmap(
    f"{PATH_INF_GRAPH}/label_map.pbtxt", use_display_name=True)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    # Run inference
    model_fn = model.signatures['serving_default']
    output_dict = model_fn(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key: value[0, :num_detections].numpy()
                   for key, value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

    # Handle models with masks:
    if 'detection_masks' in output_dict:
        # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            output_dict['detection_masks'], output_dict['detection_boxes'],
            image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                           tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

    return output_dict


def show_inference(model, image_path):
    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    image_np = np.array(Image.open(image_path))
    # Actual detection.
    output_dict = run_inference_for_single_image(model, image_np)
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        output_dict['detection_boxes'],
        output_dict['detection_classes'],
        output_dict['detection_scores'],
        category_index,
        instance_masks=output_dict.get('detection_masks_reframed', None),
        use_normalized_coordinates=True,
        line_thickness=1)

    print("HELLO WORLD")
    print(f"output_dict['detection_boxes']:   {output_dict['detection_boxes']}")
    print(f"output_dict['detection_classes']: {output_dict['detection_classes']}")
    print(f"output_dict['detection_scores']:  {output_dict['detection_scores']}")
    print(f"output_dict.get('detection_masks_reframed', None) {output_dict.get('detection_masks_reframed', None)}")

    # Show image
    ret_image = Image.fromarray(image_np)
    display(ret_image)
    return ret_image


def detect_from_image(model, image):
    image_np = np.array(image)
    output_dict = run_inference_for_single_image(model, image_np)
    return output_dict['detection_boxes'], output_dict['detection_classes'], output_dict['detection_scores']
