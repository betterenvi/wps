import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--tr_dir',
    type=str,
    default='./weps2007_data_1.1/traininig',
    help=''
)
parser.add_argument(
    '--tr_web_subdir',
    type=str,
    default='web_pages',
    help='should join with tr_dir'
)
parser.add_argument(
    '--tr_gold_subdir',
    type=str,
    default='truth_files',
    help='should join with tr_dir'
)
parser.add_argument(
    '--ts_dir',
    type=str,
    default='./WePS2_test_data/data/test',
    help='Direcotry containning test data'
)
parser.add_argument(
    '--ts_web_subdir',
    type=str,
    default='web_pages',
    help='should join with ts_dir'
)
parser.add_argument(
    '--ts_gold_subdir',
    type=str,
    default='gold_standard',
    help='should join with ts_dir'
)
parser.add_argument(
    '--ts_gold_subdir',
    type=str,
    default='gold_standard',
    help='should join with ts_dir'
)

ARGS, unknown = parser.parse_known_args(sys.argv[1:])

ARGS.tr_web_dir = os.path.join(ARGS.tr_dir, ARGS.tr_web_subdir)
ARGS.tr_gold_dir = os.path.join(ARGS.tr_dir, ARGS.tr_gold_subdir)
ARGS.ts_web_dir = os.path.join(ARGS.ts_dir, ARGS.ts_web_subdir)
ARGS.ts_gold_dir = os.path.join(ARGS.ts_dir, ARGS.ts_web_subdir)
