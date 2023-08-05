import argparse
import os
import sys
import numpy as np

from .core import backends
from .model import Model


def list_backends():
    backends_list = backends()
    print("Available backends:")
    for backend_type in backends_list:
        print(f" {backend_type} - {backends_list[backend_type].version}")


def forward(model_path, input_data, save_path):
    # Load model given by command line option
    try:
        model = Model(model_path)
    except:
        print(f"Error while loading model: {model_path}")
        sys.exit()

    # Load image/numpy file
    try:
        inputs = np.load(input_data)
    except:
        try:
            import imageio
            inputs = imageio.imread(input_data)
            inputs = np.expand_dims(inputs, 0)
        except:
            raise ImportError("imageio library is required to open images.")
            sys.exit()

    # Perform inference
    result = model.forward(inputs)

    # Save result if option was enabled
    if save_path:
        try:
            np.save(save_path, result)
            print(f"Output successfully saved: {save_path}")
        except:
            print(f"Error while saving output {save_path}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest="action")
    b_parser = sp.add_parser("backends", help="List available backends")
    f_parser = sp.add_parser("forward", help="Perform an inference")
    f_parser.add_argument("-m",
                          "--model",
                          type=str,
                          default=None,
                          help="The source model path")
    f_parser.add_argument("input",
                          type=str,
                          default=None,
                          help="Input image or a numpy array")
    f_parser.add_argument("-s",
                          "--save",
                          type=str,
                          default=None,
                          help="Save output to a numpy file")
    args = parser.parse_args()
    if args.action == "backends":
        list_backends()
    if args.action == "forward":
        forward(args.model, args.input, args.save)
