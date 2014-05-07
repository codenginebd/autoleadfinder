__author__ = 'Codengine'

import eventlet
from eventlet.green import urllib2
from eventlet.green.httplib import HTTPException
from HttpBrowser import *
from Parser import *
import time
from random import randint
from DBManager import *
from Formatter import *

proxies = [
    '89.47.28.61:8800',
    '173.208.46.100:8800',
    '173.208.46.104:8800',
    '173.234.181.253:8800',
    '173.234.181.141:8800',
    '173.234.59.194:8800',
    '173.208.46.182:8800',
    '173.234.59.72:8800',
    '89.47.28.157:8800'
    '173.208.46.111:8800'
]

class PageFetcher:
    def __init__(self):
        self.db = DBWraper()

    def start_crawling(self):
        # Return the HTML Source per URL
        def web_ReturnHTML(lead_detail):
            if lead_detail[9] and lead_detail[9].startswith('www.') or lead_detail[9].startswith('http://') or lead_detail[9].startswith('https://'):
                try:
                    page_url = lead_detail[9]
                    if lead_detail[9].startswith('www.'):
                        page_url = 'http://'+lead_detail[9]
                    page = ''
                    print "Entered URL ", page_url
                    with eventlet.Timeout(60, False):
                        try:
                            page = urllib2.urlopen(page_url).read()
                        except (HTTPException,urllib2.URLError) as e:
                            web_ReturnHTML(lead_detail)
                    return (lead_detail[0],page)
                except Exception,msg:
                    time.sleep(10)
                    print "UrlError"
                    print msg
                    web_ReturnHTML(lead_detail)

        last_fetched_page = self.db.read_last_page_fetched_state()
        start,count=0,20
        if last_fetched_page:
            start = int(last_fetched_page[0])
        while True:
            lead_details = self.db.read_info_page_not_fetched(start=start,count=count)
            if len(lead_details) == 0:
                break
            parallel_thread_count = 3

            pool = eventlet.GreenPool(parallel_thread_count)

            for page in pool.imap(web_ReturnHTML, lead_details):
                if page and page[1]:
                    refined_page = Formatter.refine_page(page[1])
                    print 'Entered %s to save info.' % str(page[0])
                    print "Refined Page: ", len(page[1])
                    content_tuple = (0L,refined_page,page[1],page[0])
                    self.db.save_page_content(content_tuple)
                    self.db.save_last_page_fetched_state(page[0])
                    self.db.mark_lead_as_read(page[0])
                    print "Saved and updated."
                    #print page[1]
                    #print len(page[1])
                    #print page[0]
                    print 'Done.'
            start += count



#PageFetcher().start_crawling()

