#!/usr/bin/env python

import distutils.core

distutils.core.setup(
        name='intrasol',
        version='0.1-dev',
        description='easy to use intranet indexer',
        author='Oups It',
        author_email='oupsit@netmon.ch',
        packages=['intrasol', 'intrasol.extraction'],
        requires=['httplib2', 'sunburnt', 'simplejson', 'argparse'],
        scripts=['bin/intrasol-cli'],
        data_files = [
            ('/var/log/intrasol', ['data/error.log', 'data/intrasol.log']),
            ('/etc', ['data/intrasol.conf.py'])
        ]
    )
