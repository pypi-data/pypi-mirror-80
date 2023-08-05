import argparse
import json
import os
from typing import Generator, List, Callable, Optional, Union

import numpy as np
from ocr4all_pixel_classifier.lib.dataset import DatasetLoader, SingleData
from ocr4all_pixel_classifier.lib.image_ops import compute_char_height
from ocr4all_pixel_classifier.lib.output import output_data, scale_to_original_shape
from ocr4all_pixel_classifier.lib.postprocess import find_postprocessor, postprocess_help
from ocr4all_pixel_classifier.lib.predictor import Predictor, PredictSettings, Prediction
from ocr4all.files import glob_all
from ocr4all.colors import ColorMap, DEFAULT_COLOR_MAPPING
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--load", metavar="MODEL", type=str, required=True, nargs="+",
                        help="Model to load")
    parser.add_argument("--char_height", type=int, required=False,
                        help="Average height of character m or n, ...")
    parser.add_argument("--target_line_height", type=int, default=6,
                        help="Scale the data images so that the line height matches this value (must be the same as in training)")
    parser.add_argument("--output", required=True,
                        help="Output dir")
    parser.add_argument("--binary", type=str, required=True, nargs="+",
                        help="directory name of the binary images")
    parser.add_argument("--images", type=str, required=True, nargs="+",
                        help="directory name of the images on which to train")
    parser.add_argument("-n", "--norm", type=str, required=False, nargs="+",
                        help="use normalization files for input char height")
    parser.add_argument("--keep_low_res", action="store_true",
                        help="keep low resolution prediction instead of rescaling output to orignal image size")
    parser.add_argument("--cc_majority", action="store_true",
                        help="DEPRECATED: use --postprocess instead. classify all pixels of each connected component as most frequent class.")
    parser.add_argument("--postprocess", type=str, nargs="+", default=[],
                        choices=["cc_majority", "bounding_boxes"],
                        help="add postprocessor functions to run on the prediction. use 'list' or 'help' to show available postprocessors")
    parser.add_argument("--color_map", type=str, default=None, help="color_map to load")
    parser.add_argument("--gpu_allow_growth", action="store_true")
    args = parser.parse_args()

    if "list" in args.postprocess or "help" in args.postprocess:
        print(postprocess_help())
        exit(0)

    image_file_paths = sorted(glob_all(args.images))
    binary_file_paths = sorted(glob_all(args.binary))

    if len(image_file_paths) != len(binary_file_paths):
        parser.error("Got {} images but {} binary images".format(len(image_file_paths), len(binary_file_paths)))

    print("Loading {} files with character height {}".format(len(image_file_paths), args.char_height))

    num_files = len(image_file_paths)

    line_heights = parse_line_heights(args, num_files, parser)

    post_processors = [find_postprocessor(p) for p in args.postprocess]
    if args.cc_majority:
        from ocr4all_pixel_classifier.lib.postprocess import vote_connected_component_class
        post_processors += [vote_connected_component_class]

    os.makedirs(args.output, exist_ok=True)

    if args.color_map:
        color_map = ColorMap.load(args.color_map)
    else:
        color_map = ColorMap(DEFAULT_COLOR_MAPPING)

    predictions = predict(args.output,
                          binary_file_paths,
                          image_file_paths,
                          color_map,
                          line_heights,
                          target_line_height=args.target_line_height,
                          models=args.load,
                          high_res_output=not args.keep_low_res,
                          post_processors=post_processors,
                          gpu_allow_growth=args.gpu_allow_growth,
                          )

    for _, prediction in tqdm(enumerate(predictions)):
        output_data(args.output, prediction.labels, prediction.data, color_map)


def parse_line_heights(args, num_files, parser):
    if args.char_height:
        line_heights = [args.char_height] * num_files
    elif args.norm:
        norm_file_paths = sorted(glob_all(args.norm)) if args.norm else []
        if len(norm_file_paths) == 1:
            line_heights = [json.load(open(norm_file_paths[0]))["char_height"]] * num_files
        else:
            if len(norm_file_paths) != num_files:
                parser.error("Number of norm files must be one or equals the number of image files")
            line_heights = [json.load(open(n))["char_height"] for n in norm_file_paths]
    else:
        if not args.binary:
            parser.error("No binary files given, cannot auto-detect char height")
        line_heights = [compute_char_height(image, True)
                        for image in tqdm(args.binary, desc="Auto-detecting char height", unit="pages")]
    return line_heights


def predict(output,
            binary_file_paths: List[str],
            image_file_paths: List[str],
            color_map: ColorMap,
            line_heights: Union[List[int], int],
            target_line_height: int,
            models: List[str],
            high_res_output: bool = True,
            post_processors: Optional[List[Callable[[np.ndarray, SingleData], np.ndarray]]] = None,
            gpu_allow_growth: bool = False,
            ) -> Generator[Prediction, None, None]:
    dataset_loader = DatasetLoader(target_line_height, prediction=True, color_map=color_map)

    if type(line_heights) is int:
        line_heights = [line_heights] * len(image_file_paths)

    data = dataset_loader.load_data(
        [SingleData(binary_path=b, image_path=i, line_height_px=n)
         for b, i, n in zip(binary_file_paths, image_file_paths, line_heights)]
    )
    predictors = [Predictor(PredictSettings(
        network=os.path.abspath(model),
        output=output,
        high_res_output=high_res_output,
        post_process=post_processors,
        color_map=color_map,
        n_classes=len(color_map),
        gpu_allow_growth=gpu_allow_growth,
    )) for model in models]

    if len(predictors) == 1:
        predictor = predictors[0]
        yield from predictor.predict(data)
    else:
        for singledata in data:
            all_model_preds = [predictor.predict_single(singledata) for predictor in reversed(predictors)]
            all_probs = [p.probabilities for p in all_model_preds]
            average_probabilities = np.mean(np.array(all_probs), axis=0)
            pred = np.argmax(average_probabilities, axis=2)
            if high_res_output:
                singledata, pred = scale_to_original_shape(singledata, pred)
            yield Prediction(pred, average_probabilities, singledata)


if __name__ == "__main__":
    main()
