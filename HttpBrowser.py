__author__ = 'Codengine'

import urllib2

class HttpBrowser:
    def __init__(self):
        pass
    @staticmethod
    def OpenURL(url_to_open,proxy=None):
        try:
            if proxy:
                proxy_handler = urllib2.ProxyHandler({'http': proxy})
                opener = urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)
            response  = urllib2.urlopen(url_to_open,timeout=60)
            return response.read()
        except Exception,msg:
            print msg
