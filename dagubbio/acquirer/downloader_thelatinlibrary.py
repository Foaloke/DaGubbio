'''
Created on 15 Aug 2017

@author: mtonnicchi
'''

import collections
from bs4 import BeautifulSoup
import urllib
import dagubbio.utils.sourceutils as su
import lxml.html as html
from lxml import etree
from lxml.html.clean import Cleaner
import requests
from tidylib import tidy_document
from lxml.etree import ParserError


class Downloader_LatinLibrary(object):


    def __init__(self, url, storage_folder):
        self.url = url
        self.storage_folder = storage_folder
    
    
    def download(self):
        raw_html = requests.get(self.url).content
        text_urls = []
        for option in self.get_main_options(raw_html):
            self.depth_text_search(self.url+option)


    def get_main_options(self, raw_html):
        return self.parse_html_as_etree(self.tidy_html(raw_html)).xpath('//table[2]//a/@href')


    def depth_text_search(self, page_url):
        if su.file_exists(self.storage_folder, self.name_file(page_url)):
            print("File exists: "+page_url)
            return
        
        print(page_url.decode('utf-8'))
       
        response = requests.get(page_url)
        if response.status_code != 200:
            print("WARNING! "+page_url+" returned status code "+str(response.status_code))
            return
        
        try:
            tidied_html = self.tidy_html(response.content, page_url)
        except ParserError:
            print("ERROR while parsing: "+response.content)
            return

        links = self.parse_html_as_etree(tidied_html).xpath('//a/@href')
        for link in links:
            next_page_url = page_url[0:(page_url.rfind('/')+1)]
            self.depth_text_search(next_page_url+link.decode('utf-8'))

        if len(links) == 0:
            print("INFO: Saving "+page_url)
            su.save_source(self.storage_folder, self.name_file(page_url), tidied_html)


    def tidy_html(self, raw_html, page_url=''):
        corrected_html = html.tostring(html.fromstring(raw_html), encoding='utf-8').decode('utf-8', 'ignore')
        corrected_html = self.remove_empty_attributes(corrected_html)
        document, errors = tidy_document(corrected_html, options={"doctype": 'omit', "output-xhtml": 0, "tidy-mark": 0, "char-encoding": "utf8"})  
        document = self.keep_relevant_tags(document)
        document = self.remove_footer(document, page_url)
        document = self.remove_self_refs(document)
        document = BeautifulSoup(document, "html.parser").prettify()
        return document


    def create_html_cleaner(self):
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        cleaner.remove_tags = ['br', 'hr', 'img', 'basefont', 'area', 'base', 'col', 'embed', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']
        return cleaner


    def remove_self_refs(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        for link in soup.find_all("a"):
            if 'href' in link.attrs:
                if "#" in link.attrs['href'][0]:
                    link.decompose()
        return str(soup)
    
    def remove_empty_attributes(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        for tag in soup.findAll(True):
            tag.attrs = \
                collections.OrderedDict(\
                    [(attr,value) for attr,value in tag.attrs.items() if value != ''])
        return str(soup)


    def empty_attribute(self, attribute):
        return attribute.value == ''


    def keep_relevant_tags(self, html_text):
        html_parsed = self.parse_html_as_etree(html_text)
        cleaner = self.create_html_cleaner()
        cleaned_html = cleaner.clean_html(etree.tostring(html.fromstring(html.tostring(html_parsed))))
        return cleaned_html

    def parse_html_as_etree(self, raw_html):
        return etree.HTML(raw_html, parser=etree.HTMLParser(encoding="utf-8"))

    def remove_footer(self, html_text, page_url):
        footer_found = False
        soup = BeautifulSoup(html_text, "html.parser")

        for footer_element in soup.find_all("div", {'class': 'main_footer'}):
            footer_element.decompose()
            footer_found = True
        for footer_element in soup.find_all("div", {'class': 'footer'}):
            footer_element.decompose()
            footer_found = True
            
        for scan_elem in [] + soup.find_all("table") + soup.find_all("center"):
            footer_links = [] \
                + scan_elem.find_all("a", {'href': 'http://thelatinlibrary.com/index'})\
                + scan_elem.find_all("a", {'href': '/index.html'})\
                + scan_elem.find_all("a", {'href': 'index.html'})\
                + scan_elem.find_all("a", {'href': '#top'})
            if len(footer_links) > 0:
                scan_elem.decompose()
                footer_found = True
        
        if not footer_found:
            print("WARNING: no footer found while processing page at "+page_url)

        return str(soup)
    

    def xpath_search(self, html_text, xpath_search):
        return self.parse_html_as_etree(html_text).xpath(xpath_search)
    
    def name_file(self, page_url):
        return urllib.quote_plus(page_url)+'.html'