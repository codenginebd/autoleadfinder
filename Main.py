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
    for index,each_lead in enumerate(lead_list):
        print 'Index %s' % str(index)
        print 'Entered to search for'
        print each_lead[1]
        if not each_lead[9]:
            print 'Web not found'
            search_results = []
            _start = 0
            keyword = each_lead[1].replace('"','')

            ###Check if email is there.
            email = each_lead[8]
            extracted_domain = Parser.extract_domain(email)
            if extracted_domain and not 'gmail' in extracted_domain and not 'yahoo' in extracted_domain:
                print 'A Valid Email Address Is Found'
                web_address = 'www.'+extracted_domain

                ###Validate the web address.
                #browser.OpenURL(google_search_link+web_address)
                #page = browser.GetPage()
                #result_links = Parser.parse_search_result(page)
                #if len(result_links) > 0:
                #    print 'Website is valid'
                #    pass
                #else:
                #    print 'Website Invalid.'

                row = (each_lead[0],each_lead[1],each_lead[2],each_lead[3],each_lead[4],each_lead[5],each_lead[6],each_lead[7],each_lead[8],web_address)
                db.update_lead_info(row)
                db.update_last_state(each_lead[0])

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

                matched_domain = None

                for each_result in search_results:
                    for word in company_name:
                        if word in each_result['domain_name'].lower() and len(word) > 2:
                            print 'Matches Found! Here it is'
                            print each_result['domain']
                            matched_domain = each_result['domain']
                            print 'Exiting inner loop'
                            break
                    if matched_domain:
                        print 'Match Found. Now exiting outer loop.'
                        break
                if matched_domain:
                    print 'Now save into db.'
                    row = (each_lead[0],each_lead[1],each_lead[2],each_lead[3],each_lead[4],each_lead[5],each_lead[6],each_lead[7],each_lead[8],matched_domain)
                    db.update_lead_info(row)
                    db.update_last_state(each_lead[0])



def main():
    import time
    start,count=0,20
    last_state = db.read_last_state()
    if last_state:
        start = last_state[0]
    while True:
        lead_info = db.read_lead_info(start,count)
        start_crawling(lead_info)
        if len(lead_info) < 20:
            break
        start += count
        time.sleep(2)


if __name__ == '__main__':
    import sys
    args = sys.argv
    if len(args) == 1:
        main()
    else:
        if args[1] == '-o':
            from CSVGenerator import *
            CSVGenerator().start_processing()
        elif args[1] == '-i':
            db.init_db()
        elif args[1] == '-r':
            db.reset_db()
    #main()
