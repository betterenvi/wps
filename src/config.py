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
    '--ts_dir',
    type=str,
    default='./WePS2_test_data/data/test',
    help='Direcotry containning test data'
)
ARGS, unknown = parser.parse_known_args(sys.argv[1:])

ARGS.tr_web_dir = os.path.join(ARGS.tr_dir, 'web_pages')
ARGS.tr_desc_dir = os.path.join(ARGS.tr_dir, 'description_files')
ARGS.tr_gold_dir = os.path.join(ARGS.tr_dir, 'truth_files')
ARGS.ts_web_dir = os.path.join(ARGS.ts_dir, 'web_pages')
ARGS.ts_desc_dir = os.path.join(ARGS.ts_dir, 'metadata')
ARGS.ts_gold_dir = os.path.join(ARGS.ts_dir, 'gold_standard')

ARGS.web_ext = '.html'
ARGS.web_basename = 'index.html'
ARGS.desc_ext = '.xml'
ARGS.gold_ext = '.xml'
