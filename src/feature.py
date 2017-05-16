# -*- coding: utf-8 -*-
import os
import sys
import re
import collections

import nltk
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
        features_list = []
        features_list.append(self._get_tfidf())
        if ARGS.use_ne != 0:
            features_list.append(self._get_named_entity())
        self._features = pd.concat(features_list, axis=1)

    def _add_features(self, features):
        self._features = pd.concat([self._features, features], axis=1)

    def _get_tfidf(self):
        self._tfidf_vectorizer = TfidfVectorizer(
            min_df=ARGS.tfidf_min_df,
            max_features=ARGS.tfidf_max_features,
            ngram_range=(ARGS.tfidf_min_ngram_range,
                         ARGS.tfidf_max_ngram_range),
            stop_words='english')

        tfv = self._tfidf_vectorizer
        tfv.fit(self._web_name.texts)
        feature_names = tfv.get_feature_names()
        tfidf = pd.DataFrame(
            tfv.transform(self._web_name.texts).todense(),
            index=self._features.index,
            columns=['tfidf_' + name for name in feature_names]
        )
        return tfidf

    def _get_named_entity(self):
        texts = self._web_name.texts
        tokens = [nltk.pos_tag(nltk.word_tokenize(text)) for text in texts]
        self._ne_trees = list(nltk.ne_chunk_sents(tokens))
        self._nes = []
        self._ne_types = []
        for tree in self._ne_trees:
            ne, ne_type = [], []
            for ele in tree:
                if type(ele) == nltk.tree.Tree:
                    ne.append(ele[0][0])
                    ne_type.append(ele.label())
            self._nes.append(ne)
            self._ne_types.append(ne_type)

        self._ne_counters = [collections.Counter(ne) for ne in self._nes]
        ne_sets = set()
        for ne in self._nes:
            ne_sets |= set(ne)

        index = self._features.index
        columns = list(ne_sets)
        ne_df = pd.DataFrame(0, index=index, columns=columns)
        for i, c in enumerate(self._ne_counters):
            cols = list(self._ne_counters[i].keys())
            cnts = list(self._ne_counters[i].values())
            ne_df.loc[index[i], cols] = cnts

        ne_df.columns = ['ne_' + x for x in ne_df.columns]
        return ne_df

    def get_features(self):
        return self._features

    def get_similarity(self, method='cosine'):
        if method == 'cosine':
            return cosine_similarity(self._features)
        else:
            raise ValueError('Unsupported similarity')
