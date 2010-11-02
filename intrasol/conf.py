
class SettingsDefaults(object):
    VERBOSE = False
    CONFIG_FILE = "/etc/intrasol.conf.py"
    LOG_LEVEL = "INFO"
    LOG_FILE = "/var/log/intrasol/intrasol.log"
    ERROR_LOG = "/var/log/intrasol/error.log"
    EXTRACTION_METHOD = "intrasol.extraction.solrcell.extract"
    SECTION = "ALL"
    # this shout be overwriten!!!
    SECTIONS = {
        "srv": "/srv",
        "www": "/var/www"
    }
    # Action settings
    WATCH_DEAMONIZE = True
    WATCH_PID = "/var/run/intrasol.pid"
    INDEX_CACHE_FILE = "/var/cache/intrasol.db"
    # solr settings
    SOLR_URL = "http://solr.netmon.ch:8080"
    SOLR_SCHEMA_PATH = "http://solr.netmon.ch:8080/solr/admin/file/?file=schema.xml"
    SOLR_CELL_URL = "http://solr.netmon.ch:8080/solr/update/extract"


class Settings(object):
    def __init__(self, settings_object):
        self.apply(settings_object)

    def apply(self, settings_object):
        for setting in dir(settings_object):
            if setting == setting.upper():
                setattr(self, setting, getattr(settings_object, setting))

settings = Settings(SettingsDefaults)