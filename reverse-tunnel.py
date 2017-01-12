#!/usr/bin/python

import os
import sys, getopt
import json
from subprocess import check_output

version = '1.0'
filename = ''
develop = ''

def info_main():
   print "Usage: %s [OPTIONS]" % os.path.basename(sys.argv[0])
   print "example: %s -i config.json -u alex" % os.path.basename(sys.argv[0])
   print ""
   print('Where OPTIONS:')
   print('-i config.json    Config file for register ex: config.json')
   print('-u developer      Developer name ex: alex')
   print ""

def read_config(arg):
    filename = arg
    try:
        if os.path.exists(filename) == True:
            txt = open(filename)
            resp = json.loads(txt.read())
            # print resp
        else:
            print "bonk give correct config_file"
    except Exception as e:
        print "Bonk...got error in read_config function"

def registry_dotunnel(filename,develop):
    try:
        txt = open(filename)
        resp = json.loads(txt.read())

      #   get servet value
        get_server = (resp['server'])
        server = {}
        server.update(get_server)

      #   GET developers value
        get_developer = (resp['developers'])
        developers = {}
        developers.update(get_developer)
        # Exit if developer name is not exists
        if not developers.has_key(develop):
            print "Developer name '%s' not found." % develop
            exit(1)

        currentDev = developers[develop]
        currentServer = server['user'] + '@' + server['host']

        print 'Creating tunnel for %s at %s (%s) to %s...' % (currentDev['name'], server['host'], currentDev['remote_bind'], currentDev['dev_bind'])
        output = check_output(['ssh', '-N', '-R', currentDev['remote_bind'] + ':' + currentDev['dev_bind'], currentServer])
        print output

        exit(0)

    except Exception as e:
        print "Bonk...got error in registry_dotunnel function"

def main(argv):
   if len(sys.argv) == 1:
       info_main()
   try:
      opts, args = getopt.getopt(argv,"h:i:u:v")
   except getopt.GetoptError:
      info_main()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print "usage: %s -i <config_file.ini>" % os.path.basename(sys.argv[0])
         sys.exit()
      elif opt in ("-v"):
          print 'Version:', version
      elif opt in ("-i"):
          filename = arg
          read_config(filename)
      elif opt in ("-u"):
          develop = arg
          registry_dotunnel(filename,develop)

if __name__ == "__main__":
   main(sys.argv[1:])
