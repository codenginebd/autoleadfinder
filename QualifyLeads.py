__author__ = 'Codengine'

from FileHandler import *

class QualifyLeads:
    def __init__(self):
        kws = CSVFileReader.read_keywords()
        self.keywords = []
        for keyword in kws:
            unic = keyword.decode('utf_8','ignore')
            k = unic.encode('utf_8','ignore')
            self.keywords += [k]

    def start_processing(self):
        pass