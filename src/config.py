# -*- coding: utf-8 -*-
import os
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
parser.add_argument(
    '--tfidf_max_features',
    type=int,
    default=2000,
    help=''
)
parser.add_argument(
    '--tfidf_min_df',
    type=int,
    default=1,
    help=''
)
parser.add_argument(
    '--tfidf_min_ngram_range',
    type=int,
    default=1,
    help=''
)
parser.add_argument(
    '--tfidf_max_ngram_range',
    type=int,
    default=2,
    help=''
)

ARGS, unknown = parser.parse_known_args(sys.argv[1:])

ARGS.tr_doc_dir = os.path.join(ARGS.tr_dir, 'web_pages')
ARGS.tr_desc_dir = os.path.join(ARGS.tr_dir, 'description_files')
ARGS.tr_gold_dir = os.path.join(ARGS.tr_dir, 'truth_files')
ARGS.ts_doc_dir = os.path.join(ARGS.ts_dir, 'web_pages')
ARGS.ts_desc_dir = os.path.join(ARGS.ts_dir, 'metadata')
ARGS.ts_gold_dir = os.path.join(ARGS.ts_dir, 'gold_standard')

ARGS.doc_ext = '.html'
ARGS.doc_basename = 'index.html'
ARGS.desc_ext = '.xml'
ARGS.gold_ext = '.xml'
