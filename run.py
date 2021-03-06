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


def main():
    # create one dataset with default args.
    # one dataset contains many names and each name has several people.
    tr_set = TrainSet()  # drop some data due to encoding
    print(tr_set.names)
    print(len(tr_set.names))
    # ts_set = TestSet()   # read whole test set
    ts_set = TestSet(names=['TOM_LINTON'])  # or only read given names
    tr_set = ts_set
    # print names in the dataset
    print(ts_set.names)

    # calculate features for the first name in the dataset
    wn = tr_set.web_names[0]
    print(wn.entities)
    fc = FeatureCollector(wn)
    print(fc.get_features())
    print(fc.get_similarity(method='cosine'))


if __name__ == '__main__':
    main()
