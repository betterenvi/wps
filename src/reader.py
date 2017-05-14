import os
import sys
import re
import collections

from bs4 import BeautifulSoup

from src import util
from src.config import ARGS


class WebName(object):
    def __init__(self, name, web_dir, desc_dir, gold_dir, rank_as_int=True):
        super(WebName, self).__init__()
        self._name = name
        self._web_dir = web_dir
        self._desc_dir = desc_dir
        self._gold_dir = gold_dir
        self._rank_as_int = rank_as_int
        self.entities = collections.defaultdict(list)
        self.cluster = {}
        self.discarded = list()
        self._read_data()

    def _read_data(self):
        self._read_web()
        self._read_desc()
        self._read_gold()

    def _parse_web_id(self, path):
        '''
        just a placeholder, should be implemented in sub class
        '''
        return 1 if self._rank_as_int else '1'

    def _read_web(self):
        self._webs = util.walkdir(self._web_dir, ARGS.web_ext)
        self._web_ids = [self._parse_web_id(w) for w in self._webs]
        self._texts = [util.read_clean_html(w) for w in self._webs]

    def _read_desc(self):
        pass

    def _parse_gold(self, soup):
        if not hasattr(soup, 'children'):
            return
        if str(soup) == '<entity':
            entity_id = soup.attrs['id']
            for ch in list(soup.children):
                rank = ch.attrs['rank']
                if self._rank_as_int:
                    rank = int(rank)
                self.entities[entity_id].append(rank)
        elif str(soup) == '<discarded':
            for ch in list(soup.children):
                self.discarded.append(ch.attrs['rank'])
        else:
            for ch in list(soup.children):
                self._parse_gold(self, ch)

    def _read_gold(self):
        path = os.path.join(self._gold_dir, self._name + ARGS.gold_ext)
        html = util.read_html(path)
        soup = BeautifulSoup(html)
        self._parse_gold(soup)
        for entity_id in self.entities.keys():
            for rank in self.entities[entity_id]:
                self.cluster[rank] = entity_id


class TrainWebName(WebName):
    def __init__(self,
                 name,
                 web_dir=ARGS.tr_web_dir,
                 desc_dir=ARGS.tr_desc_dir,
                 gold_dir=ARGS.tr_gold_dir,
                 rank_as_int=True):

        super(TrainWebName, self).__init__(name,
                                        web_dir, desc_dir, gold_dir,
                                        rank_as_int)

    def _parse_web_id(self, path):
        '''
        e.g.
        input: weps2007_data_1.1/traininig/web_pages/Abby_Watkins/raw/001/index.html
        return: 1
        '''
        parent_dir = os.path.basename(os.path.dirname(path))
        rank = int(parent_dir)
        return rank if self._rank_as_int else str(rank)


class TestWebName(WebName):
    def __init__(self,
                 name,
                 web_dir=ARGS.ts_web_dir,
                 desc_dir=ARGS.ts_desc_dir,
                 gold_dir=ARGS.ts_gold_dir,
                 rank_as_int=True):

        super(TestWebName, self).__init__(name,
                                        web_dir, desc_dir, gold_dir,
                                        rank_as_int)

    def _parse_web_id(self, path):
        '''
        e.g.
        input: WePS2_test_data/data/test/web_pages/AMANDA_LENTZ/001.html
        return: 1
        '''
        basename = os.path.basename(path)
        rank = int(basename[:(-len(ARGS.web_ext))])
        return rank if self._rank_as_int else str(rank)


class DataSet(object):
    def __init__(self,
                 web_dir, desc_dir, gold_dir,
                 rank_as_int=True,
                 WebNameClass=TrainWebName):
        super(DataSet, self).__init__()
        self._WebNameClass = WebNameClass
        self._web_dir = web_dir
        self._desc_dir = desc_dir
        self._gold_dir = gold_dir
        self._rank_as_int = rank_as_int
        self._build()

    def _build(self):
        WebNameClass = self._WebNameClass
        self.names = os.listdir(self._web_dir)
        self.web_names = []
        for name in self.names:
            web_name = WebNameClass(name, self._web_dir,
                                    self._desc_dir, self._gold_dir,
                                    self._rank_as_int)
            self.web_names.append(web_name)


class TrainSet(DataSet):
    def __init__(self,
                 web_dir=ARGS.tr_web_dir,
                 desc_dir=ARGS.tr_desc_dir,
                 gold_dir=ARGS.tr_gold_dir,
                 rank_as_int=True,
                 WebNameClass=TrainWebName):

        super(TrainSet, self).__init__(web_dir, desc_dir, gold_dir,
                                       rank_as_int, WebNameClass)


class TestSet(DataSet):
    def __init__(self,
                 web_dir=ARGS.ts_web_dir,
                 desc_dir=ARGS.ts_desc_dir,
                 gold_dir=ARGS.ts_gold_dir,
                 rank_as_int=True,
                 WebNameClass=TestWebName):

        super(TestSet, self).__init__(web_dir, desc_dir, gold_dir,
                                      rank_as_int, WebNameClass)
