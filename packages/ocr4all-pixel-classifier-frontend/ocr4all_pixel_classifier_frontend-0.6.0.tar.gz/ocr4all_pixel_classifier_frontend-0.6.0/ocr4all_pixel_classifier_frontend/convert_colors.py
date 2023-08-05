import argparse
import functools
import multiprocessing
import os

from ocr4all.colors import ColorMap
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(add_help=False)
    paths_args = parser.add_argument_group("Paths")
    paths_args.add_argument("-i", "--input-color-map", type=str, required=True,
                            help="color mapping for the input images")
    paths_args.add_argument("-o", "--output-color-map", type=str, required=True,
                            help="desired output color mapping")
    paths_args.add_argument("-O", "--output-dir", type=str, required=True,
                            help="The output dir for the recolored masks")
    paths_args.add_argument("images", metavar="IMAGE", type=str, nargs="+",
                            help="the images to convert")

    opt_args = parser.add_argument_group("optional arguments")
    opt_args.add_argument("-j", "--jobs", "--threads", metavar='THREADS', dest='threads',
                          type=int, default=multiprocessing.cpu_count(),
                          help="Number of threads to use")
    opt_args.add_argument("-h", "--help", action="help", help="show this help message and exit")

    args = parser.parse_args()

    in_map = ColorMap.load(args.input_color_map)
    out_map = ColorMap.load(args.output_color_map)

    os.makedirs(args.output_dir, exist_ok=True)

    convert_m = functools.partial(convert, outdir=args.output_dir,
                                  in_map=in_map,
                                  out_map=out_map,
                                  )

    with multiprocessing.Pool(processes=args.threads) as p:
        for _ in tqdm(p.imap(convert_m, args.images), total=len(args.images), unit="img"):
            pass


def convert(img_path, outdir, in_map: ColorMap, out_map: ColorMap):
    labels = in_map.imread_labels(img_path)
    res = out_map.to_image(labels)
    res.save(os.path.join(outdir, os.path.basename(img_path)))


if __name__ == '__main__':
    main()
