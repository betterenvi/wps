import os
import sys
import re
import collections

from bs4 import BeautifulSoup

from src import util
from src.config import ARGS
from src.reader import (
    TrainWebName,
    TestWebName,
    TrainSet,
    TestSet,
)


