__author__ = 'ixtix'

import sys
import os
import logging
import datetime
from conf import settings
from conf import SettingsDefaults
from file import File

class CacheFile(File):
    def update_index(self):
        # check if index is uptodate
        # how to index??
        # self.update
        try:
            conn = self.solrConn()
            entries = conn.query("", {"id": self.id}).execute().result.docs
            if len(entries) == 1:
                entry = entries[0]
                if entry["fmodified"] <= self.fmodified:
                    self.logger.debug("File (%s) is allready indexed" % str(self))
                    conn.update({"id": self.id, "updated": datetime.datetime.now()})
                    conn.commit()
                else:
                    self.logger.debug("File (%s) is outdated force reindex" % str(self))
                    self.update()
            else:
                self.update()
        except:
            exc_info = sys.exc_info()
            self.logger.debug("chache check throws exec(%s: %s), reindex the file" % (exc_info[0], exc_info[1])) 
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
        setattr(settings, "START_DATE", datetime.datetime.now())
        if settings.PATH == None:
            if settings.SECTION.upper() == "ALL":
                self.logger.info("start indexing all sections")
                for section in settings.SECTIONS.keys():
                    self.index_section(section)
            else:
                self.index_section(settings.SECTION)
            # delete missing!!
        else:
            self.index_tree(settings.PATH, settings.SECTION)

    def index_section(self, section):
        self.logger.info("start indexing section: "+section)
        path = settings.SECTIONS[section]
        self.index_tree(path, section)

    def index_tree(self, path, section="default"):
        try:
            self.logger.debug("starting tree walk on path: '%s' with type=%s" % (path, type(path)))
            tree = os.walk(path)
            for dirname, subdirs, fnames in tree:
                self.index_dir(dirname, fnames, section)
        except:
            exc_info = sys.exc_info()
            self.logger.error("error while indexing tree(%s) for section(%s) last dirname (%s). Exception: %s Value: %s" % (path, section, dirname, exc_info[0], exc_info[1]))

    def index_dir(self, dirname, fnames=None, section="default"):
        #ToDo: Error handling
        self.logger.debug("indexing dir: %s" % dirname)
        if fnames == None:
            fnames = []
            entries = os.listdir(dirname)
            for entry in entries:
                if not os.path.isdir(entry):
                    fnames.add(entry)
        for fname in fnames:
            self.index(os.path.join(dirname, fname), section)

    def index(self, fpath, section):
        #ToDo: Error handling
        # push file to solr
        self.logger.debug("indexing file: %s" % fpath)
        file = CacheFile(fpath, section)
        file.update_index()

