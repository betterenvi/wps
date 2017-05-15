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
    # you may create one small test dataset to test your code.
    # create one dataset with default args.
    # one dataset contains many names and each name has several people.
    # tr_set = TrainSet()  # not work now due to encoding
    # ts_set = TestSet()   # read whole test set
    ts_set = TestSet(names=['TOM_LINTON'])  # or only read given names

    # print names in the dataset
    print(ts_set.names)

    # calculate features for the first name in the dataset
    fc = FeatureCollector(ts_set.web_names[0])
    print(fc.get_features())
    print(fc.get_similarity(method='cosine'))


if __name__ == '__main__':
    main()
