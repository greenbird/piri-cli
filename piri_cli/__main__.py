import argparse
import json
import sys

from piri.process import Process
from returns.curry import partial
from returns.result import safe

from piri_cli.common import read_file, write_file

parser = argparse.ArgumentParser(
    description='Transforms input json with provided cfg file to output.json',
)

parser.add_argument(
    'configuration',
    type=str,
    help='Path to configuration.json',
)

parser.add_argument(
    'input',
    type=str,
    help='Path to input.json',
)

parser.add_argument(
    '-o',
    '--output',
    type=str,
    help='Path and name of file to write',
    default='output.json',
)

args = parser.parse_args()


def on_failure(failure):
    """Print out reason for failure and exit."""
    sys.exit('Execution failed.\nError type {0}\nError msg: {1}'.format(
        type(failure),
        failure,
    ))


configuration = read_file(
    args.configuration, 'r',
).bind(
    safe(json.loads),
).alt(on_failure).unwrap()

input_data = read_file(
    args.input, 'r',
).bind(
    safe(json.loads),
).alt(on_failure).unwrap()

Process()(
    input_data,
    configuration,
).bind(
    safe(json.dumps),
).bind(
    partial(write_file, file_path=args.output),
).alt(on_failure)
