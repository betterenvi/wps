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
    # create one dataset with default args
    # one dataset contains many names and each name has several people.
    # tr_set = TrainSet()  # not work now due to encoding
    ts_set = TestSet()

    # print names in the dataset
    print(ts_set.names)

    # calculate features for the first name in the dataset
    fc = FeatureCollector(ts_set.web_names[0])
    print(fc.get_features())
    print(fc.get_similarity(method='cosine'))


if __name__ == '__main__':
    main()
