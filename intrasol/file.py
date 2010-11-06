# import commen modules
import os
import sys
import hashlib
import datetime
import logging
#import tempfile
# import 3th party
import httplib2
import sunburnt
# import project modules
from intrasol.conf import settings

def get_section_for_path(path):
    section = None
    for section, section_path in settings.SECTIONS.items():
        if path.startswith(section_path):
            return section
    raise Exeption()


class File(object):
    __solrConnection = None
    __extractionMethod = None

    def __init__(self, path, section=None):
        self.logger = logging.getLogger("File")
        abspath =  os.path.abspath(path)
        if section == None:
            self.section = get_section_for_path(path)
        else:
            self.section = section
        self.path = abspath.replace(settings.SECTIONS[self.section]+"/", "")
        self.id = u"%s?%s" %  (self.section, self.path.decode("utf-8"))
        stat = os.stat(abspath)
        self.logger.debug("File object inited %s" % str(self))
        self.fmodified = datetime.datetime.fromtimestamp(stat.st_mtime)
        self.fcreated = datetime.datetime.fromtimestamp(stat.st_ctime)
        self.faccessed = datetime.datetime.fromtimestamp(stat.st_atime)
        self.fsize = stat.st_size
        self.fowner = stat.st_uid
        self.fgroup = stat.st_gid
        self.author = ""
        self.creator = ""
        self.producer = ""
        self.content_type = ""
        self.text = ""
        self.date = ""

    def __str__(self):
        return "intrasol.File[section=%s, path=%s]" % (self.section, self.path)

    def __extract(self):
        if self.fsize < settings.EXTRACTION_MAX_FILESIZE:
            self.logger.debug("start extraction of file(%s)" % str(self))
            if File.__extractionMethod == None:
                method_parts = settings.EXTRACTION_METHOD.split(".")
                method_name = method_parts.pop()
                method_path = ".".join(method_parts)
                module = __import__(method_path)
                module = sys.modules[method_path]
                File.__extractionMethod = getattr(module, method_name)
            File.__extractionMethod(self)
            self.logger.debug("extraction of %s finished" % str(self))
        else:
            self.logger.debug("file is to big! skip extraction for %s" % str(file))

    def __solrConn(self):
        if File.__solrConnection == None:
            # get schema and init sunburnt connection
            #tmpfilename = os.tmpnam()
            #tmpfile = open(tmpfilename, mode="w+")
            #h = httplib2.Http()
            #resp, content = h.request(settings.SOLR_SCHEMA_PATH)
            #tmpfile.write(content)
            #tmpfile.close()
            File.__solrConnection = sunburnt.SolrInterface(settings.SOLR_URL, settings.SOLR_SCHEMA_PATH)
        return File.__solrConnection


    def update(self):
        try:
            self.__extract()
            self.logger.debug("updateing solr index with file(%s)" % str(self))
            conn = self.__solrConn()
            conn.add(self)
            conn.commit()
            self.logger.debug("updating of file(%s) finshed" % str(self))
        except:
            exc_info = sys.exc_info()
            self.logger.error("Error updating File: %s with Exception(%s: %s)" % (str(self), exc_info[0], exc_info[1]))




