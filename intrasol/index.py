__author__ = 'ixtix'

import os
import logging
from conf import settings
from conf import SettingsDefaults
from file import File

class CacheFile(file):
    def update_index(self):
        # check if index is uptodate
        # how to index??
        # self.update
        self.update()

class Indexer:
    def __init__(self, subparsers):
        index_parser = subparsers.add_parser("index", help="runs the over the given tree of a categorie and index every file")
        index_parser.add_argument("--cache", type=str, dest="INDEX_CACHE_FILE", default=SettingsDefaults.INDEX_CACHE_FILE)
        index_parser.set_defaults(func=self)
        self.logger = logging.getLogger("Indexer")
        #ToDo: Log Indexer initialized

    def __call__(self, settings):
        # do the indexing
        #ToDo: Error handling
        self.logger.debug("start indexing")
        if settings.SECTION.upper() == "ALL":
            self.logger.info("start indexing all sections")
            for section in settings.SECTIONS.keys():
                self.index_section(section)
        else:
            self.index_section(settings.SECTION)

    def index_section(self, section):
        self.logger.info("start indexing section: "+section)
        path = settings.SECTIONS[section]
        self.index_tree(path, section)

    def index_tree(self, path, section="default"):
        self.logger.debug("starting tree walk on path: "+path)
        tree = os.walk(path)
        for dir, subdirs, fnames in tree:
            self.index_dir(dir, fnames, settings.SECTION)

    def index_dir(self, dir, fnames=None, section="default"):
        #ToDo: Error handling
        self.logger.debug("indexing dir: %s" % dir)
        if fnames == None:
            fnames = []
            entries = os.listdir(dir)
            for entry in entries:
                if not os.path.isdir(entry):
                    fnames.add(entry)
        for fname in fnames:
            self.index(os.path.join(dir, fname), section)

    def index(self, fpath, section):
        #ToDo: Error handling
        # push file to solr
        self.logger.debug("indexing file: %s" % fpath)
        file = CacheFile(fpath, section)
        file.update_index()

