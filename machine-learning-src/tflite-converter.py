from tflite_support.metadata_writers import object_detector
from tflite_support.metadata_writers import writer_utils

_TFLITE_MODEL_WITH_METADATA_PATH = "fire_smoke_detection_metadata.tflite"

writer = object_detector.MetadataWriter.create_for_inference(
    writer_utils.load_file("fire_smoke_detection.tflite"), input_norm_mean=[126.0], 
    input_norm_std=[64.6], label_file_paths=["test_label_map.txt"])
writer_utils.save_file(writer.populate(), _TFLITE_MODEL_WITH_METADATA_PATH)