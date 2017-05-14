# -*- coding: utf-8 -*-
import os
import sys
import re
import collections

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src import util
from src.config import ARGS
from src.reader import (
    TrainWebName,
    TestWebName,
    TrainSet,
    TestSet,
)


class FeatureCollector(object):
    def __init__(self, web_name):
        super(FeatureCollector, self).__init__()
        self._web_name = web_name
        self._features = pd.DataFrame(index=web_name.docs)
        self._calculate()

    def _calculate(self):
        self._calc_tfidf()

    def _add_features(self, features):
        self._features = pd.concat([self._features, features], axis=1)

    def _calc_tfidf(self):
        self._tfidf_vectorizer = TfidfVectorizer(min_df=3,
                                                 max_features=None,
                                                 ngram_range=(1, 2),
                                                 stop_words='english')

        tfv = self._tfidf_vectorizer
        tfv.fit(self._web_name.texts)
        feature_names = tfv.get_feature_names()
        tfidf = pd.DataFrame(
            tfv.transform(self._web_name.texts).todense(),
            index=self._features.index,
            columns=['tfidf_' + name for name in feature_names]
        )
        self._add_features(tfidf)

    def get_features(self):
        return self._features

    def get_similarity(self, method='cosine'):
        if method == 'cosine':
            return cosine_similarity(self._features)
        else:
            raise ValueError('Unsupported similarity')



