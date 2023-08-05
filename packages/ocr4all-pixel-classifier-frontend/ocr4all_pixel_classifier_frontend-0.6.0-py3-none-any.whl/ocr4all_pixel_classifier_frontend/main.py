import sys

import argparse
import importlib

commands = {
    'train': {
        'script': 'ocr4all_pixel_classifier_frontend.train',
        'main': 'main',
        'help': 'Train the neural network. See more via "* train --help"'
    },
    'predict': {
        'script': 'ocr4all_pixel_classifier_frontend.predict',
        'main': 'main',
        'help': 'Predict a result with the neural network. See more via "* predict --help"'
    },
    'predict-json': {
        'script': 'ocr4all_pixel_classifier_frontend.predict_json',
        'main': 'main',
        'help': 'Predict a result with the neural network, input via JSON. See more via "* predict --help"'
    },
    'create-dataset-file': {
        'script': 'ocr4all_pixel_classifier_frontend.create_dataset_file',
        'main': 'main',
        'help': 'Create a dataset file'
    },
    'compute-image-normalizations': {
        'script': 'ocr4all_pixel_classifier_frontend.compute_image_normalizations',
        'main': 'main',
        'help': 'Compute image normalizations'
    },
    'compute-color-map': {
        'script': 'ocr4all_pixel_classifier_frontend.generate_color_map',
        'main': 'main',
        'help': 'Generates color map'
    },
    'inspect-color-map': {
        'script': 'ocr4all_pixel_classifier_frontend.inspect_color_map',
        'main': 'main',
        'help': 'Displays color map on a color-enabled terminal'
    },
    'convert-colors': {
        'script': 'ocr4all_pixel_classifier_frontend.convert_colors',
        'main': 'main',
        'help': 'Convert predictions or masks from one color mapping to another'
    },
    'migrate-model': {
        'script': 'ocr4all_pixel_classifier_frontend.migrate_model',
        'main': 'main',
        'help': 'Convert old model to new format'
    },
    'gen-masks': {
        'script': 'ocr4all_pixel_classifier_frontend.gen_masks',
        'main': 'main',
        'help': 'Generate mask images from PAGE XML'
    },
    'find-segments': {
        'script': 'ocr4all_pixel_classifier_frontend.find_segments',
        'main': 'main',
        'help': 'Run a prediction and region segmentation'
    },
    'eval': {
        'script': 'ocr4all_pixel_classifier_frontend.evaluate',
        'main': 'main',
        'help': 'Evaluate a model'
    },
}


def main():
    # Pretty print help for main programm
    usage = 'page-segmentation <command> [<args>]\n\nCOMMANDS:'
    # Add all commands to help
    max_name_length = max(len(name) for name, _ in commands.items())
    for name, command in commands.items():
        usage += '\n\t{name:<{col_width}}\t{help}'.format(name=name, col_width=max_name_length, help=command["help"])

    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('command', help='The sub command to execute, see COMMANDS')
    parser.add_argument("--completion")

    args = parser.parse_args(sys.argv[1:2])
    sys.argv = sys.argv[:1] + sys.argv[2:]

    if args.command in commands.keys():
        command = commands[args.command]
        command_module = importlib.import_module(command['script'])
        command_main = getattr(command_module, command['main'])
        command_main()
    else:
        print('Unrecognized command')
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
