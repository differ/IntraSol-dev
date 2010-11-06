import argparse
import logging

class Watcher:
    def __init__(self, subparsers):
        watch_parser = subparsers.add_parser("watch", help="runs in the background and applies changes to the solr index")
        watch_parser.add_argument("-nd", "--no-deamonize", default=False, action="store_false", dest="WATCH_DEAMONIZE", help="if the watch process shout be deamonized")
        watch_parser.add_argument("-d", "--deamonize", default=True, action="store_true", dest="WATCH_DEAMONIZE", help="deamonizes the watch prozess")
        watch_parser.add_argument("-p", "--pid", default="/var/run/intrasol_watch.pid", type=str, help="sets the location of the pid file for the process")
        watch_parser.set_defaults(func=self)

    def __call__(self, settings):
        #ToDo: implementation
        # what for changes
        print argv