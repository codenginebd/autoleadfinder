#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Codengine
#
# Created:     25-04-2014
# Copyright:   (c) Codengine 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib2
from DBManager import *
from Browser import *
from Parser import *

db = DBWraper()

google_search_link = 'https://www.google.com.bd/?gws_rd=cr&ei=ymdaU7bSIM6VrgeC2oHACA#q='

def start_crawling(lead_list):
    print len(lead_list)
    browser = Browser()
    for each_lead in lead_list:
        if not each_lead[9]:
            search_results = []
            _start = 0
            keyword = each_lead[1].replace('"','')

            ###Check if email is there.
            email = each_lead[8]
            extracted_domain = Parser.extract_domain(email)
            if extracted_domain and not 'gmail' in extracted_domain and not 'yahoo' in extracted_domain:
                print 'A Valid Email Address Is Found'
                web_address = 'www.'+extracted_domain
                ###Now update in db.
                row = (each_lead[0],each_lead[1],each_lead[2],each_lead[3],each_lead[4],each_lead[5],each_lead[6],each_lead[7],web_address)
                db.update_lead_info(row)
            else:
                while True:
                    try:
                        #company_name_quoted = urllib2.encode('utf-8').quote(each_lead[1])
                        url = google_search_link+keyword+'&start='+str(_start)
                        print 'Entering url'
                        print url
                        browser.OpenURL(url)
                        page = browser.GetPage()

                        print 'Page Fetched'
                        print 'Found Length %s' % str(len(page))

                        #f = open('page.html','w')
                        #f.write(page)
                        #f.close()

                        search_results += Parser.parse_search_result(page)


                        if _start == 10:
                            print 'Done for url'
                            break
                        print 'Increment page counter'
                        _start += 10
                    except Exception,msg:
                        print 'Exception Occured.'
                        print 'Exception Msg'
                        print msg
                ###Now process the search result data here.
                print 'Search results to be processed %s' % str(len(search_results))

                """ Lower the keyword and split it """
                print keyword
                company_name = keyword.lower().split()
                print company_name

def main():
    lead_info = db.read_lead_info()
    start_crawling(lead_info)


if __name__ == '__main__':
    main()
