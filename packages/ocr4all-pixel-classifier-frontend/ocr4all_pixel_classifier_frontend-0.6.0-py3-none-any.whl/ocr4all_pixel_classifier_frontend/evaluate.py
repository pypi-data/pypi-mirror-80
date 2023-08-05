import argparse
import multiprocessing
from dataclasses import dataclass
from functools import partial
from typing import Tuple

import numpy as np
from ocr4all.files import imread_bin, match_filenames
from ocr4all.colors import ColorMap
from ocr4all_pixel_classifier.lib.evaluation import count_matches, total_accuracy, f1_measures, ConnectedComponentEval, \
    cc_matching
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--masks", type=str, required=True, nargs="+",
                        help="expected masks")
    parser.add_argument("--preds", type=str, required=True, nargs="+",
                        help="prediction results")
    parser.add_argument("--binary", type=str, required=True, nargs="+",
                        help="binary source images")
    parser.add_argument("--color-map-model", type=str, required=False, help="color map used in model")
    parser.add_argument("--color-map-eval", type=str, required=False, help="color map used in evaluation data set")
    parser.add_argument("-v", "--verbose", action="store_true", help="Also output statistics per image")
    parser.add_argument("-j", "--jobs", "--threads", metavar='THREADS', dest='threads',
                        type=int, default=multiprocessing.cpu_count(),
                        help="Number of threads to use")
    parser.add_argument("--csv", action="store_true", help="enable csv output")
    cceval_args = parser.add_argument_group("Connected Component Evaluation")
    cceval_args.add_argument("-T", "--cc-threshold-tp", type=float, default=1.0,
                             help="ratio of pixels required for a true positive")
    cceval_args.add_argument("-F", "--cc-threshold-fp", type=float, default=0.1,
                             help="ratio of pixels required for a false positive")
    cceval_args.add_argument("-M", "--cc-threshold-mask", type=float, default=1.0,
                             help="ratio of pixels required for mask component to be considered text")
    parser.add_argument("--verify-filenames", action="store_true")
    parser.add_argument("--singleclass", action="store_true", help="evaluate as"
                                                                   "binary classificator by treating background and image class as same")
    args = parser.parse_args()

    # if args.csv and args.verbose:
    #    parser.error("--csv and --verbose are currently not compatible")

    if bool(args.color_map_model) != bool(args.color_map_eval):
        parser.error("color map is only useful if given for both model and evaluation data set")

    if len(args.masks) != len(args.preds) or len(args.preds) != len(args.binary):
        parser.error("Number of masks, predictions and binary images not equal ({} / {} / {})"
                     .format(len(args.masks), len(args.preds), len(args.binary)))

    if args.verify_filenames:
        files_match, err = match_filenames(args.binary, args.masks, args.preds)
        if not files_match:
            parser.error("Error in file arguments: " + err)

    # image_tpfpfn_cc = np.zeros([3])

    if args.color_map_model and args.color_map_eval:
        model_map = ColorMap.load(args.color_map_model)
        eval_map = ColorMap.load(args.color_map_eval)
    else:
        model_map = eval_map = ColorMap({(255, 255, 255): (0, 'background'),
                                         (0, 255, 0): (1, 'text'),
                                         (255, 0, 255): (2, 'image')})

    # for mask_p, pred_p, bin_p in tqdm(zip(args.masks, args.preds, args.binary)):

    text_tpfpfn = np.zeros([3])
    image_tpfpfn = np.zeros([3])
    correct_total = np.zeros([2])
    text_tpfpfn_cc = np.zeros([3])

    parfunc = partial(eval_page, eval_map=eval_map, model_map=model_map,
                      verbose=args.verbose, csv=args.csv, singleclass=args.singleclass,
                      args=args)

    if args.csv and args.verbose:
        print('Image,Category,TP,FP,FN,Precision,Recall,F1')
    with multiprocessing.Pool(processes=args.threads) as p:
        for match in tqdm(p.imap(parfunc, zip(args.masks, args.preds, args.binary)), total=len(args.masks)):
            # for page in zip(args.masks, args.preds, args.binary):
            #    match = eval_page(page, eval_map=eval_map, model_map=model_map, verbose=args.verbose)
            text_tpfpfn += match.text
            image_tpfpfn += match.image
            correct_total += match.accuracy
            text_tpfpfn_cc += match.cc

    if args.csv:
        print('Category,TP,FP,FN,Precision,Recall,F1')
        print(csv_total('text', text_tpfpfn))
        print(csv_total('image', image_tpfpfn))
        print(csv_total('text-cc', text_tpfpfn_cc))
        print("acc,{:f}".format(correct_total[0] / correct_total[1]))
    else:
        print("\nText:")
        print(format_total(text_tpfpfn))
        print("\nImage:")
        print(format_total(image_tpfpfn))
        print("\nText CCs:")
        print(format_total(text_tpfpfn_cc))
        print("\nOverall accuracy:")
        print('================================================================\n')
        print(correct_total[0] / correct_total[1])


@dataclass
class MatchResults:
    text: Tuple[int, int, int]
    image: Tuple[int, int, int]
    cc: np.ndarray
    accuracy: Tuple[int, int]


def format_total(counts):
    ttp, tfp, tfn = counts
    return '================================================================\n' \
           'total:\n' \
           '{:<10} / {:<10} /  {:<10} -> Prec: {:f}, Rec: {:f}, F1: {:f}' \
        .format(ttp, tfp, tfn, *f1_measures(ttp, tfp, tfn))


def csv_total(category: str, counts: np.ndarray):
    ttp, tfp, tfn = counts
    return '{},{},{},{},{:f},{:f},{:f}' \
        .format(category, ttp, tfp, tfn, *f1_measures(ttp, tfp, tfn))


def eval_page(page: Tuple[str, str, str], eval_map: ColorMap, model_map: ColorMap, verbose, csv, singleclass, args):
    mask_p, pred_p, bin_p = page
    mask = eval_map.imread_labels(mask_p)
    pred = model_map.imread_labels(pred_p)
    if singleclass:
        pred[pred == 0] = 2
    fg = imread_bin(bin_p)

    cceval = ConnectedComponentEval(mask, pred, fg).only_label(1,
                                                               args.cc_threshold_mask)

    text_cc_eval = list(cceval.run_per_component(cc_matching(1,
                                                             threshold_tp=args.cc_threshold_tp,
                                                             threshold_fp=args.cc_threshold_fp,
                                                             threshold_mask=args.cc_threshold_mask)))
    if len(text_cc_eval) == 0:
        text_matches_cc = [0, 0, 0]
    else:
        text_matches_cc = sum(text_cc_eval)
    # image_matches_cc = sum(cceval.run_per_component(cc_matching(2, 0.9)))
    # image_tpfpfn_cc += image_matches_cc

    text_matches = count_matches(mask[fg], pred[fg], 1)

    image_matches = count_matches(mask[fg], pred[fg], 2)

    correct = total_accuracy(mask[fg], pred[fg])

    if verbose:
        if csv:
            print("{},text,{},{},{},{},{},{}"
                  .format(bin_p, *text_matches, *f1_measures(*text_matches)))
            print("{},image,{},{},{},{},{},{}"
                  .format(bin_p, *image_matches, *f1_measures(*image_matches)))
            print("{},textcc,{},{},{},{},{},{}"
                  .format(bin_p, *text_matches_cc, *f1_measures(*text_matches_cc)))
        else:
            print("T: {:<10} / {:<10} / {:<10} -> Prec: {:<5f}, Rec: {:<5f}, F1{:<5f} {:>20}"
                  .format(*text_matches, *f1_measures(*text_matches), bin_p))
            print("I: {:<10} / {:<10} / / {:<10} -> Prec: {:<5f}, Rec: {:<5f}, F1{:<5f} {:>20}"
                  .format(*image_matches, *f1_measures(*image_matches), bin_p))
            print("CC: {:<10} / {:<10} / / {:<10} -> Prec: {:<5f}, Rec: {:<5f}, F1{:<5f} {:>20}"
                  .format(*text_matches_cc, *f1_measures(*text_matches_cc), bin_p))

    return MatchResults(text_matches, image_matches, text_matches_cc, correct)


if __name__ == "__main__":
    main()
