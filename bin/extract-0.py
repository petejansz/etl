from etlextract import EtlExtractBaseClass

class Extract0(EtlExtractBaseClass):

  def write_output_file(self):
    print "Wrote formatted result to %s." % self.output_filename
    
    
ex17 = Extract17('extract-17.sql', 'extract-17.del')
print ex17.sql_filename
ex17.write_output_file()