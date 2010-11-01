__author__ = 'ixtix'

import os
import simplejson
import urllib2
import mimetypes
from conf import settings


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
    abspath = os.path.join(settings.SECTIONS[file.section], file.path)
    request = urllib2.Request(setttings.SOLR_CELL_URL + "?extractOnly=true&wt=json")
    request.add_data(open(abspath).read())
    # add mimetype .. based on the mimetypes package
    mimetypes.init()
    request.add_header("Content-type", mimtypes.guess_type(abspath)[0])
    try:
        json_response = urllib2.urlopen(request).read()
        result = simplejson.loads(json_response)
        file.author = result['author']
        file.creator = result['creator']
        file.generator = result['generator']
        file.date = result['date']
        file.content_type = result['Content-Type']
        file.content = result['text']
    except:
        #log extraction failed..
        pass

