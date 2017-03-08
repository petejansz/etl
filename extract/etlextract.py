#
#
# Pete Jansz, CGI, Sacramento
#

from abc import ABCMeta, abstractmethod

class EtlExtractBaseClass(object):
  def __init__(self, sql_filename, output_filename):
    self._sql_filename = sql_filename
    self._output_filename = output_filename

  __metaclass__ = ABCMeta
  
  @property
  def sql_filename(self):
    return self._sql_filename
    
  @sql_filename.setter
  def sql_filename(self, value):
    self._sql_filename = value
    
  @property
  def output_filename(self):
    return self._output_filename
    
  @output_filename.setter
  def output_filename(self, value):
    self._output_filename = value
    
  @abstractmethod
  def write_output_file(self):
    pass
