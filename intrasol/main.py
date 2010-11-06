#!/usr/bin/env python
import sys
import os
import argparse
import imp
import logging
import logging.handlers
# import local files
import index, watch
import conf
from conf import SettingsDefaults, settings

def main(argv):
    parser = argparse.ArgumentParser(
                                    description='Indexes Directories to Solr',
                                    epilog="IntraSol roules the Intranet")
    parser.add_argument("-v", "--verbose", default=SettingsDefaults.VERBOSE, action="store_true", dest="VERBOSE")
    parser.add_argument("-c", "--config", default=SettingsDefaults.CONFIG_FILE, type=str, dest="CONFIG_FILE", help="sets the configuration file of intrasol")
    parser.add_argument("-s", "--section", default=SettingsDefaults.SECTION, type=str, dest="SECTION", help="sets the categorie for the action")
    parser.add_argument("-p", "--path", default=None, type=str, dest="PATH", help="overrides the path to index, care full this can create many mistakes")
    parser.add_argument("-ll", "--loglevel", default=SettingsDefaults.LOG_LEVEL, type=str, dest="LOG_LEVEL", help="sets the loglevel")
    parser.add_argument("-lf", "--logfile", default=SettingsDefaults.LOG_FILE, type=str, dest="LOG_FILE", help="defines a log file for the output")
    parser.add_argument("-el", "--errorlog", default=SettingsDefaults.ERROR_LOG, type=str, dest="ERROR_LOG", help="defines where the errorlog shout be")
    parser.add_argument("-e", "--extraction", default=SettingsDefaults.EXTRACTION_METHOD, type=str, dest="EXTRACTION_METHOD", help="defines the used extraction method")
    subparsers = parser.add_subparsers( title="main commands",
                                        description="the main command and option types",
                                        help="commands")
    # create subcommands
    index.Indexer(subparsers)
    watch.Watcher(subparsers)
    # parse args
    args = parser.parse_args(argv)
    # set argument namespace to conf CommandSettings
    setattr(conf, "CommandSettings", args)
    # set configuration values in conf file to conf.FileSettings
    setattr(conf, "FileSettings", imp.load_source("conf.FileSettings", args.CONFIG_FILE ))
    # merge them with the settings.. direction is importent!!
    settings.apply(conf.FileSettings)
    settings.apply(conf.CommandSettings)
    # setup logging
    logging.basicConfig(    level=getattr(logging, settings.LOG_LEVEL),
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=settings.LOG_FILE,
                            filemode='w')
    errorLogger = logging.handlers.TimedRotatingFileHandler(settings.ERROR_LOG, 'midnight', backupCount=7)
    errorLogger.setLevel(logging.ERROR)
    # get root logger add errorLogger
    logger = logging.getLogger('')
    logger.addHandler(errorLogger)
    if settings.VERBOSE:
        verboseLogger = logging.StreamHandler()
        verboseLogger.setLevel(getattr(logging, settings.LOG_LEVEL))
        # create formatter and add it to the handlers
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        verboseLogger.setFormatter(formatter)
        logger.addHandler(verboseLogger)
    # call for action
    logger.info("IntraSol initialized, calling the action function")
    args.func(settings)
    logger.info("IntraSol action finished, closing IntraSol")


