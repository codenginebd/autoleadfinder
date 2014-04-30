__author__ = 'Sohel'

import urllib2
from bs4 import BeautifulSoup

class Parser:
    def __init__(self):
        pass

    @staticmethod
    def extract_domain(email):
        index_of_at = email.find('@')
        if index_of_at != -1 and len(email) > 3:
            return email[email.index('@')+1:]

    @staticmethod
    def parse_search_result(page):
        search_results = []
        soup = BeautifulSoup(page)
        search_result_lis = soup.findAll('li',{'class':'g'})
        #print search_result_lis
        for each_li in search_result_lis:
            try:
                title_header_h3 = each_li.find('h3',{'class':'r'})
                header_title_anchor = title_header_h3.find('a')
                title_text = header_title_anchor.text
                data_url = header_title_anchor['href'].replace('/url?q=','')
                data_url = data_url[:data_url.index('&')]
                data_url = urllib2.unquote(data_url)
                temp = data_url[data_url.index('/')+2:]
                domain = temp[:temp.index('/')]
                domain_name = domain.replace('www.','')
                domain_name = domain_name[:domain_name.rindex('.')]
                search_results += [{'title':title_text,'url':data_url,'domain':domain,'domain_name':domain_name}]
            except Exception,msg:
                print 'Exception Occured Inside parse_search_result method'
                print msg
        return search_results

#f = open('page.html','r')
#page = f.read()
#f.close()
#print Parser.parse_search_result(page)


