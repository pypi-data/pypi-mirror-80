import argparse
import itertools
import sys
import typing

from PIL import Image #type: ignore
from colour_sort import sort, verify, sort_type, colour_space, convert

CLI_SYNTAX_ERROR = 2

def generate_image(args):
    infile = args.infile
    outfile = args.outfile
    sort_type_ = args.sort
    colour_space_ = args.colour_space
    converter_ = args.converter

    input_image = Image.open(infile)
    mode = sort_type.SortType.from_str(sort_type_)
    space = colour_space.ColourSpace.from_str(colour_space_)

    if converter_ == 'PIL':
        converter = convert.PilConverter()
    elif converter_ == 'cv2':
        converter = convert.Cv2Converter()
    else: #if converter_ == 'skimage':
        converter = convert.SkimageConverter()

    generated = sort.create_sorted_image(input_image, mode=mode, colour_space=space, converter=converter)
    try:
        generated.save(outfile, lossless=True)
    except:
        generated.save(outfile)


def verify_image(args):
    infile = args.infile
    print_missing  = args.missing

    input_image = Image.open(infile)
    check = verify.missing_colours(input_image)
    valid = not len(check)
    if valid:
        print('%s is a valid allrgb image!' % infile)
    else:
        print('%s is not a valid allrgb image' % infile)

    if print_missing:
        for colour in check:
            print(colour)


def run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')

    generate_parser = subparsers.add_parser('generate')
    generate_parser.add_argument('infile')
    generate_parser.add_argument('outfile')
    generate_parser.add_argument('--sort', default='brightness', choices=[mode.name.lower() for mode in sort_type.SortType])
    generate_parser.add_argument('--colour-space', default='RGB', choices=[space.name.lower() for space in colour_space.ColourSpace])
    generate_parser.add_argument('--converter', default='PIL', choices=['PIL', 'cv2', 'skimage'])
    generate_parser.set_defaults(func=generate_image)

    verify_parser = subparsers.add_parser('verify')
    verify_parser.add_argument('infile')
    verify_parser.add_argument('--missing', action='store_true')
    verify_parser.set_defaults(func=verify_image)

    args = parser.parse_args()
    if not args.subparser_name:
        parser.print_usage(file=sys.stderr)
        print(f'colour: error: one of the following arguments is required: {", ".join(subparsers.choices.keys())}', file=sys.stderr)
        sys.exit(CLI_SYNTAX_ERROR)

    args.func(args)

if __name__ == '__main__':
    run()
