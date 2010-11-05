__author__ = 'ixtix'

import sys
import os
import simplejson
import urllib2
import mimetypes
import logging
from intrasol.conf import settings


def extract(file):
    """
       enter the file object.. and it inserts what he nows..
       working python code:
       >>> req = urllib2.Request("http://solr.netmon.ch:8080/solr/update/extract?extractOnly=true&wt=json")
       >>> req.add_data(open("ReferenceCard.pdf").read())
       >>> req.add_header("Content-type", "application/pdf")
       >>> ret = urllib2.urlopen(req)
       >>> import simplejson
       >>> result = simplejson.loads(ret.read())
    """
    #ToDo: logging and error handling
    try:
        logger = logging.getLogger("SolrCell")
        logger.debug("prepare for extraction of file: %s" % file)
        abspath = os.path.join(settings.SECTIONS[file.section], file.path)
        url = settings.SOLR_CELL_URL + "?extractOnly=true&wt=json"
        request = urllib2.Request(url)
        request.add_data(open(abspath).read())
        # add mimetype .. based on the mimetypes package
        mimetypes.init()
        mimetype = mimetypes.guess_type(abspath)[0]
        request.add_header("Content-type", mimetype)
        logger.debug("file has content-type: %s" % mimetype)
        logger.debug("open request to url with file content")
        json_response = urllib2.urlopen(request).read()
        logger.debug("load response")
        result = simplejson.loads(json_response)
        logger.debug("file up the result: in to the file object")
        file.author = result.get('author', '')
        file.creator = result.get('creator', '')
        file.generator = result.get('generator', '')
        file.date = result.get('date', '')
        file.content_type = mimetype
        file.text = result.get('', '')
    except:
        #log extraction failed..
	exc_info = sys.exc_info()
        logger.error("could not extract file: %s" % str(file))
        logger.error("extraction exception: %s value: %s" % (exc_info[0], exc_info[1]))

