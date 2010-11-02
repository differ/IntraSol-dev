# import commen modules
import os
import hashlib
import datetime
# import 3th party
import sunburnt
# import project modules
from intrasol.conf import settings

def get_section_for_path(path):
    section = None
    for section, section_path in settings.SECTIONS.items():
        if path.startswith(section_path):
            return section
    raise Exeption()

__solrConnection = None

@property
def SolrConnection():
    if __solrConnection == None:
        # init sunburnt connection
        __solrConnection = sunburnt.SolrInterface(settings.SOLR_URL, settings.SOLR_SCHEMA_PATH)
    return __solrConnection


__extractionMethod = None

class File(object):

    def __init__(self, path, section=None):
        self.logger = logging.getLogger("File")
        abspath =  os.path.abspath(path)
        if section == None:
            self.section = get_section_for_path(path)
        self.path = abspath.replace(settings.SECTIONS[self.section]+"/")
        self.id = "%s?%s" %  (self.section, self.path)
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

    def __str__(self):
        return "intrasol.File[section=%s, path=%s]" % (self.section, self.path)

    def __extract(self):
        self.logger.debug("start extraction of file(%s)" % str(file))
        if __extractionMethod == None:
            method_parts = settings.EXTRACTION_METHOD.split(".")
            method_name = method_parts.pop()
            method_path = ".".join(method_parts)
            module = __import__(module_path)
            __extractionMethod = getattr(module, method_name)
        __extractionMethod(self)
        self.logger.debug("extraction of %s finished" % str(self))

    def update(self):
        self.__extract()
        self.logger.debug("updateing solr index with file(%s)" % str(self))
        SolrConnection.add(self)
        SolrConnection.commit()
        self.logger.debug("updating of file(%s) finshed" % str(self))




