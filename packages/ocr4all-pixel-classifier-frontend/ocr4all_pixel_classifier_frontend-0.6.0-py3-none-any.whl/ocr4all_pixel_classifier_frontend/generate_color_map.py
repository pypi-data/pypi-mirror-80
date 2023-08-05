import argparse
import multiprocessing

from ocr4all.colors import compute_from_images


def main():
    parser = argparse.ArgumentParser(add_help=False)
    paths_args = parser.add_argument_group("Paths")
    paths_args.add_argument("-I", "--input-dir", type=str, required=True,
                            help="Mask directory to process")
    paths_args.add_argument("-O", "--output-dir", type=str, required=True,
                            help="The output dir for the color map")

    opt_args = parser.add_argument_group("optional arguments")
    opt_args.add_argument("-h", "--help", action="help", help="show this help message and exit")
    opt_args.add_argument("--max-image", type=int, default=-1,
                          help="Max images to check for color. -1 to check every mask")
    opt_args.add_argument("-j", "--jobs", "--threads", metavar='THREADS', dest='threads',
                          type=int, default=multiprocessing.cpu_count(),
                          help="Number of threads to use")

    args = parser.parse_args()
    compute_from_images(args.input_dir, args.output_dir, args.max_image, args.threads)


if __name__ == '__main__':
    main()
