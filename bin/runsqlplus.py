#!/usr/bin/python

#
# Simple Python script using subprocess to query Oracle db.
# Pete
# 

from subprocess import Popen, PIPE
from os import chdir
import logging, re, sys

SQL_DIR = '/home/devuser/p1_script'

def get_sql_stmt( sql_filename ):
  fin = open(sql_filename, 'r')

  sql_stmt = ''  
  for line in fin.readlines():
    if line.find('spool') == -1:
      sql_stmt += line

  fin.close()
  return sql_stmt

def run_sqlplus( sql_filename ):
  (username, password, host, port, sid) = ("ETL_USER","acclcmips","LINDB48", '1521', 'CMIPSPROTO')
  chdir(SQL_DIR)
  conn_string = " %s/%s@%s:%s/%s " % (username, password, host, port, sid)
  session = Popen(['sqlplus', '-S', conn_string], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  logging.info("Starting sqlplus")

  sql_path_file = '%s/%s' % (SQL_DIR, sql_filename)
  logging.info("SQL file: " + sql_path_file)
  sql_stmt = get_sql_stmt( sql_filename )
  session.stdin.write(sql_stmt)

  return session.communicate()

def main():
  sql_filename = sys.argv[1]
  logging.basicConfig(filename='etl.log', level=logging.DEBUG)
  stdout, stderr = run_sqlplus( sql_filename )
  print stdout

if __name__ == "__main__":
  main()
