#!/usr/bin/env python
"""Ingest Generic Database tables using multi-value insert statements and multiprocessing.

Usage:
  %s <configFile> <inputFile>... [--table=<table>] [--bundlesize=<bundlesize>] [--nprocesses=<nprocesses>] [--loglocationInsert=<loglocationInsert>] [--logprefixInsert=<logprefixInsert>] [--loglocationIngest=<loglocationIngest>] [--logprefixIngest=<logprefixIngest>] [--types=<types>] [--skiphtm] [--nullValue=<nullValue>]
  %s (-h | --help)
  %s --version

Options:
  -h --help                                Show this screen.
  --version                                Show version.
  --table=<table>                          Target table name.
  --bundlesize=<bundlesize>                Group inserts into bundles of specified size [default: 1]
  --nprocesses=<nprocesses>                Number of processes to use - warning - beware of opening too many processes [default: 16]
  --loglocationInsert=<loglocationInsert>  Log file location [default: /tmp/]
  --logprefixInsert=<logprefixInsert>      Log prefix [default: inserter]
  --loglocationIngest=<loglocationIngest>  Log file location [default: /tmp/]
  --logprefixIngest=<logprefixIngest>      Log prefix [default: ingester]
  --types=<types>                          Column types.
  --skiphtm                                Don't bother calculating HTMs. They're either already done or we don't need them.
  --nullValue=<nullValue>                  Value of NULL definition (e.g. NaN, NULL, \\N, None) [default: \\N]

Example:
   %s /tmp/bile.csv.gz

"""
import sys
__doc__ = __doc__ % (sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0])
from docopt import docopt
import os, shutil, re
from gkutils.commonutils import Struct, cleanOptions, readGenericDataFile, dbConnect, which, splitList, parallelProcess
from datetime import datetime
from datetime import timedelta
import subprocess
#import MySQLdb
from cassandra.cluster import Cluster
import gzip
from collections import OrderedDict


def nullValue(value, nullValue = '\\N'):
   returnValue = nullValue

   if value and value.strip():
      returnValue = value.strip()

   return returnValue

def nullValueNULL(value):
   returnValue = None

   if value and not isinstance(value, int) and value.strip() and value != 'NULL':
      returnValue = value.strip()

   return returnValue

def boolToInteger(value):
    returnValue = value
    if value == 'true':
        returnValue = 1
    if value == 'false':
        returnValue = 0
    return returnValue

def calculate_htm_name_bulk(generateHtmNameBulk, htmLevel, tempRaDecFile):
    # Call the C++ HTM ID calculator
    htmIDs = []

    p = subprocess.Popen([generateHtmNameBulk, str(htmLevel), tempRaDecFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate()

    if output.strip():
        htmIDs = output.strip().split('\n')

    return htmIDs


# Use INSERT statements so we can use multiprocessing
def executeLoad(session, table, data, bundlesize = 100, types = None):

    rowsUpdated = 0

    if len(data) == 0:
        return rowsUpdated

    keys = list(data[0].keys())
    typesDict = OrderedDict()

    i = 0
    for k in keys:
        typesDict[k] = types[i]
        i += 1

    formatSpecifier = ','.join(['%s' for i in keys])

    chunks = int(1.0 * len(data) / bundlesize + 0.5)
    if chunks == 0:
        subList = [data]
    else:
        bins, subList = splitList(data, bins = chunks, preserveOrder = True)


    for dataChunk in subList:
        try:
            sql = "insert into %s " % table
            sql += "(%s)" % ','.join(['%s' % k for k in keys])
            sql += " values "
            sql += ',\n'.join(['('+formatSpecifier+')' for x in range(len(dataChunk))])
            sql += ';'

            values = []
            for row in dataChunk:
                for key in keys:
                    value = nullValueNULL(boolToInteger(row[key]))
                    if value is not None:
                        value = eval(typesDict[key])(value)
                    values.append(value)

            session.execute(sql, tuple(values))


        except Exception as e:
            print("EXCEPTION", e)
            #print "Error %d: %s" % (e.args[0], e.args[1])

    return


def workerInsert(num, db, objectListFragment, dateAndTime, firstPass, miscParameters):
    """thread worker function"""
    # Redefine the output to be a log file.
    options = miscParameters[0]
    sys.stdout = open('%s%s_%s_%d.log' % (options.loglocationInsert, options.logprefixInsert, dateAndTime, num), "w")
    cluster = Cluster()
    session = cluster.connect()
    session.set_keyspace(db['keyspace']) 

    types = options.types.split(',')

    # This is in the worker function
    objectsForUpdate = executeLoad(session, options.table, objectListFragment, int(options.bundlesize), types=types)

    print("Process complete.")
    cluster.shutdown()
    print("Connection Closed - exiting")

    return 0

def ingestData(options, inputFiles):

    if options.skiphtm is None:
        generateHtmNameBulk = which('generate_htmname_bulk')
        if generateHtmNameBulk is None:
            sys.stderr.write("Can't find the generate_htmname_bulk executable, so cannot continue.\n")
            exit(1)

    import yaml
    with open(options.configFile) as yaml_file:
        config = yaml.safe_load(yaml_file)

    username = config['cassandra']['local']['username']
    password = config['cassandra']['local']['password']
    keyspace = config['cassandra']['local']['keyspace']
    hostname = config['cassandra']['local']['hostname']

    db = {'username': username,
          'password': password,
          'keyspace': keyspace,
          'hostname': hostname}

    currentDate = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
    (year, month, day, hour, min, sec) = currentDate.split(':')
    dateAndTime = "%s%s%s_%s%s%s" % (year, month, day, hour, min, sec)

    for inputFile in inputFiles:
        print("Ingesting %s" % inputFile)
        if 'gz' in inputFile:
            # It's probably gzipped
            f = gzip.open(inputFile, 'rb')
            print(type(f).__name__)
        else:
            f = inputFile
    
        data = readGenericDataFile(f, delimiter=',', useOrderedDict=True)
        pid = os.getpid()
    
        if options.skiphtm is None:
            tempRADecFile = '/tmp/' + os.path.basename(inputFile) + 'radec_' + str(pid)
            tempLoadFile = '/tmp/' + os.path.basename(inputFile) + '_' + str(pid) + '.csv'
    
            with open(tempRADecFile, 'wb') as f:
                for row in data:
                    f.write('%s %s\n' % (row['ra'], row['dec']))
    
            htm16Names = calculate_htm_name_bulk(generateHtmNameBulk, 16, tempRADecFile)
    
            os.remove(tempRADecFile)

            # For Cassandra, we're going to split the HTM Name across several columns.
            # Furthermore, we only need to do this once for the deepest HTM level, because
            # This is always a subset of the higher levels.  Hence we only need to store
            # the tail end of the HTM name in the actual HTM 16 column.  So...  we store
            # the full HTM10 name as the first 12 characters of the HTM 16 one, then the
            # next 3 characters into the HTM 13 column, then the next 3 characters (i.e.
            # the last few characters) the HTM 16 column
            # e.g.:
            # ra, dec =      288.70392, 9.99498
            # HTM 10  = N02323033011
            # HTM 13  = N02323033011 211
            # HTM 16  = N02323033011 211 311

            # Incidentally, this hierarchy also works in binary and we should seriously
            # reconsider how we are currently using HTMs.

            # HTM10 ID =    13349829 = 11 00 10 11 10 11 00 11 11 00 01 01
            # HTM13 ID =   854389093 = 11 00 10 11 10 11 00 11 11 00 01 01  10 01 01
            # HTM16 ID = 54680902005 = 11 00 10 11 10 11 00 11 11 00 01 01  10 01 01  11 01 01


            for i in range(len(data)):
                # Add the HTM IDs to the data
                data[i]['htm10'] = htm16Names[i][0:12]
                data[i]['htm13'] = htm16Names[i][12:15]
                data[i]['htm16'] = htm16Names[i][15:18]
    
    
        nprocesses = int(options.nprocesses)
    
        if len(data) > 0:
            nProcessors, listChunks = splitList(data, bins = nprocesses, preserveOrder=True)
    
            print("%s Parallel Processing..." % (datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))
            parallelProcess(db, dateAndTime, nProcessors, listChunks, workerInsert, miscParameters = [options], drainQueues = False)
            print("%s Done Parallel Processing" % (datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))


    
def workerIngest(num, db, objectListFragment, dateAndTime, firstPass, miscParameters):
    """thread worker function"""
    # Redefine the output to be a log file.
    options = miscParameters[0]
    sys.stdout = open('%s%s_%s_%d.log' % (options.loglocationIngest, options.logprefixIngest, dateAndTime, num), "w")

    # This is in the worker function
    objectsForUpdate = ingestData(options, objectListFragment)

    print("Process complete.")

    return 0

def ingestDataMultiprocess(options):

    currentDate = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
    (year, month, day, hour, min, sec) = currentDate.split(':')
    dateAndTime = "%s%s%s_%s%s%s" % (year, month, day, hour, min, sec)

    nProcessors, fileSublist = splitList(options.inputFile, bins = int(options.nprocesses), preserveOrder=True)
    
    print("%s Parallel Processing..." % (datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))
    parallelProcess([], dateAndTime, nProcessors, fileSublist, workerIngest, miscParameters = [options], drainQueues = False)
    print("%s Done Parallel Processing" % (datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))


def main(argv = None):
    opts = docopt(__doc__, version='0.1')
    opts = cleanOptions(opts)

    # Use utils.Struct to convert the dict into an object for compatibility with old optparse code.
    options = Struct(**opts)
    ingestDataMultiprocess(options)
    #ingestData(options)


if __name__=='__main__':
    main()


