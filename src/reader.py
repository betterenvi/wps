# -*- coding: utf-8 -*-
import os
import sys
import re
import collections

from bs4 import BeautifulSoup

from src import util
from src.config import ARGS


class WebName(object):
    '''
    Many people have the same name.
    WebName is a class, holding the name and several people who has this name.
    '''
    def __init__(self, name, doc_dir, desc_dir, gold_dir,
                 rank_as_int=True, gold_ext='.xml'):
        super(WebName, self).__init__()
        self._name = name
        self._doc_dir = doc_dir
        self._desc_dir = desc_dir
        self._gold_dir = gold_dir
        self._rank_as_int = rank_as_int
        self._gold_ext = gold_ext
        self.entities = collections.defaultdict(list)
        # all_* contain those discarded
        self.all_doc_files = list()
        self.all_docs = list()
        self.all_texts = list()
        self.discarded = list()
        # don't consider discarded
        self.doc_files = list()
        self.docs = list()
        self.texts = list()
        self.doc2entity = {}
        #
        self.doc_avails = []
        self.available = True
        self._read_data()

    @property
    def num_docs(self):
        return len(self.docs)

    def _read_data(self):
        try:
            self._read_doc()
            self._read_desc()
            self._read_gold()
            self._discard()
        except Exception as e:
            print('"{}" not available due to'.format(self._name), e)
            self.available = False

    def _discard(self):
        for i, doc in enumerate(self.all_docs):
            if doc not in self.discarded:
                self.doc_files.append(self.all_doc_files[i])
                self.docs.append(doc)
                self.texts.append(self.all_texts[i])

    def _parse_rank(self, rank):
        if self._rank_as_int:
            rank = int(rank)
        return rank

    def _parse_doc_id(self, path):
        '''
        just a placeholder, should be implemented in sub class
        '''
        return self._parse_rank('1')

    def _find_docs(self):
        self.all_doc_files = util.walkdir(self._doc_dir, ARGS.doc_ext)

    def _read_doc(self):
        self._find_docs()
        for w in self.all_doc_files:
            try:
                tx = util.read_clean_html(w)
                self.all_texts.append(tx)
                self.doc_avails.append(True)
            except Exception as e:
                self.doc_avails.append(False)
        tmp = []
        for i, avil in enumerate(self.doc_avails):
            if avil:
                tmp.append(self.all_doc_files[i])
                self.all_docs.append(self._parse_doc_id(self.all_doc_files[i]))
        self.all_doc_files = tmp

    def _read_desc(self):
        pass

    def _parse_gold(self, soup):
        if not hasattr(soup, 'children'):
            return
        if soup.name == 'entity':
            entity_id = soup['id']
            for ch in list(soup.children):
                if ch.name != 'doc':
                    continue
                rank = self._parse_rank(ch['rank'])
                if rank in self.all_docs:
                    self.entities[entity_id].append(rank)
        elif soup.name == 'discarded':
            for ch in list(soup.children):
                if ch.name != 'doc':
                    continue
                rank = self._parse_rank(ch['rank'])
                if rank in self.all_docs:
                    self.discarded.append(rank)
        else:
            for ch in list(soup.children):
                self._parse_gold(ch)

    def _read_gold(self):
        path = os.path.join(self._gold_dir, self._name + self._gold_ext)
        html = util.read_file(path)
        soup = BeautifulSoup(html, 'lxml')
        self._parse_gold(soup)
        for entity_id in self.entities.keys():
            for rank in self.entities[entity_id]:
                self.doc2entity[rank] = entity_id


class TrainWebName(WebName):
    def __init__(self, name, doc_dir, desc_dir, gold_dir, rank_as_int=True):
        super(TrainWebName, self).__init__(name, doc_dir, desc_dir, gold_dir,
                                           rank_as_int, gold_ext=ARGS.tr_gold_ext)

    def _find_docs(self):
        all_doc_files = util.walkdir(self._doc_dir, ARGS.doc_ext)
        self.all_doc_files = []
        for doc in all_doc_files:
            if doc.endswith('index.html'):
                self.all_doc_files.append(doc)

    def _parse_doc_id(self, path):
        '''
        e.g.
        input: weps2007_data_1.1/traininig/web_pages/Abby_Watkins/raw/001/index.html
        return: 1
        '''
        parent_dir = os.path.basename(os.path.dirname(path))
        try:
            rank = int(parent_dir)
            return rank if self._rank_as_int else str(rank)
        except Exception as e:
            print('_parse_doc_id:', path, parent_dir)
            print(e)


class TestWebName(WebName):
    def __init__(self, name, doc_dir, desc_dir, gold_dir, rank_as_int=True):

        super(TestWebName, self).__init__(name, doc_dir, desc_dir, gold_dir,
                                          rank_as_int, gold_ext=ARGS.ts_gold_ext)

    def _discard(self):
        for i, doc in enumerate(self.all_docs):
            self.doc_files.append(self.all_doc_files[i])
            self.docs.append(doc)
            self.texts.append(self.all_texts[i])

    def _parse_doc_id(self, path):
        '''
        e.g.
        input: WePS2_test_data/data/test/web_pages/AMANDA_LENTZ/001.html
        return: 1
        '''
        basename = os.path.basename(path)
        rank = int(basename[:(-len(ARGS.doc_ext))])
        return rank if self._rank_as_int else str(rank)


class DataSet(object):
    '''
    DataSet: contains many names and each name has several people.
    '''
    def __init__(self,
                 doc_dir, desc_dir, gold_dir,
                 names=None,
                 rank_as_int=True,
                 WebNameClass=TrainWebName):
        super(DataSet, self).__init__()
        self._WebNameClass = WebNameClass
        self._doc_dir = doc_dir
        self._desc_dir = desc_dir
        self._gold_dir = gold_dir
        self._rank_as_int = rank_as_int
        if names is None:
            self.all_names = os.listdir(self._doc_dir)
        else:
            assert type(names) == list
            self.all_names = names
        self._build()

    def _build(self):
        WebNameClass = self._WebNameClass
        self.web_names = []
        self.names = []
        for name in self.all_names:
            web_name = WebNameClass(name,
                                    os.path.join(self._doc_dir, name),
                                    self._desc_dir, self._gold_dir,
                                    self._rank_as_int)
            if web_name.available:
                self.web_names.append(web_name)
                self.names.append(name)

        self.num_names = len(self.names)


class TrainSet(DataSet):
    def __init__(self,
                 doc_dir=ARGS.tr_doc_dir,
                 desc_dir=ARGS.tr_desc_dir,
                 gold_dir=ARGS.tr_gold_dir,
                 names=None,
                 rank_as_int=True,
                 WebNameClass=TrainWebName):

        super(TrainSet, self).__init__(doc_dir, desc_dir, gold_dir,
                                       names, rank_as_int, WebNameClass)


class TestSet(DataSet):
    def __init__(self,
                 doc_dir=ARGS.ts_doc_dir,
                 desc_dir=ARGS.ts_desc_dir,
                 gold_dir=ARGS.ts_gold_dir,
                 names=None,
                 rank_as_int=True,
                 WebNameClass=TestWebName):

        super(TestSet, self).__init__(doc_dir, desc_dir, gold_dir,
                                      names, rank_as_int, WebNameClass)
