# -*- coding: utf-8 -*-
import os
import sys

from src.config import ARGS
from src.reader import (
    TrainWebName,
    TestWebName,
    TrainSet,
    TestSet,
)

from src.feature import FeatureCollector
from src import util

def main():
    # tr_set = TrainSet()
    print(ARGS.ts_doc_dir)
    print(os.listdir(ARGS.ts_doc_dir))
    ts_set = TestSet()
    tr_set = ts_set
    print(tr_set.names)

    fc = FeatureCollector(tr_set.web_names[0])
    print(fc.get_features())
    print(fc.get_similarity())


if __name__ == '__main__':
    main()
