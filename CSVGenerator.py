from DBManager import DBWraper

__author__ = 'Codengine'
# - * - coding: UTF-8 - * -

import urllib2
from DBManager import *
import csv
import unicodecsv

class CSVGenerator:
    def __init__(self):
        self.db = DBWraper()

    def start_processing(self):
        lead_info_list = self.db.read_lead_info_all()
        details_list = [
            ['Full Name','Name 2','Name 3', 'Address One', 'Address Two', 'Telephone', 'Fax', 'Email', 'Website']
        ]
        for lead in lead_info_list:
            details_list += [
                [urllib2.unquote(lead[1].encode('latin-1','ignore')),urllib2.unquote(lead[2].encode('latin-1','ignore')),urllib2.unquote(lead[3].encode('latin-1','ignore')),urllib2.unquote(lead[4].encode('latin-1','ignore')),urllib2.unquote(lead[5].encode('latin-1','ignore')),lead[6],lead[7],lead[8],lead[9]]
            ]

        file_name = 'Lead_List_Output.csv'

        with open('Output/'+file_name, 'w') as fp:
            a = unicodecsv.writer(fp, delimiter=',')
            a.writerows(details_list)
