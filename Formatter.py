from __future__ import division
__author__ = 'Codengine'

import re
import nltk, re, pprint

class Formatter:
    def __init__(self):
        pass
    @staticmethod
    def _refine_page(page):
        formatted_page = re.sub(r'<script(.+?)</script>',' ',page)
        formatted_page = re.sub(r'/*(.+?)*/',' ',formatted_page)
        formatted_page = re.sub(r'<style(.+?)</style>',' ',formatted_page)
        formatted_page = re.sub(r'<(.+?)>',' ',formatted_page)
        formatted_page = re.sub(r'(\s+)',' ',formatted_page)
        return formatted_page.strip()

    @staticmethod
    def refine_page(page):
        raw_data = nltk.clean_html(page)
        data = re.sub(r'(\s+)',' ',raw_data)
        return data
