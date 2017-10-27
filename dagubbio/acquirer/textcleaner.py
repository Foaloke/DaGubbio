'''
Created on 15 Aug 2017

@author: mtonnicchi
'''

import os
import re
from bs4 import BeautifulSoup
import utils.sourceutils as su

class TextCleaner(object):


    def __init__(self, allowed_non_literal):
        self.allowed_non_literal = allowed_non_literal
    
    
    def clean_and_save_all_html_files(self, sources_dirs, storage_folder):
        for source_dir in sources_dirs.split(','):
            for source_file in os.listdir(source_dir):
                if su.file_exists(storage_folder, source_file):
                    print("File exists: "+source_file)
                else:
                    cleaned_text = self.clean_text_from_html_file_at(source_dir, source_file)
                    su.save_source(storage_folder, source_file, cleaned_text)
    
    
    def clean_text_from_html_file_at(self, html_file_dir, html_file_name):
        html_text = su.load_source(html_file_dir, html_file_name)
        return self.clean_text_from_html_file(html_text)
    
    
    def clean_text_from_html_file(self, html_text):

        if '&#194;' in html_text:
            print("WARNING: Found entity that may occur from invalid char conversion!")
            html_text = html_text.replace('&#194;','')
            
        # Remove alphanumeric flags
        alphanumeric_flags_regex = re.compile(r'(\[[0-9]+[A-Z]{0,2}\])')
        html_text = re.sub(re.compile(alphanumeric_flags_regex), '', html_text)

        html_doc = BeautifulSoup(html_text, "html.parser").find('body')
        
        # Remove tags containing only numbers
        only_numbers = re.compile('^[0-9\s]+$')
        for tag in html_doc.find_all():
            if only_numbers.search(tag.get_text()):
                tag.decompose()

        extracted_text = html_doc.get_text()
        if extracted_text == '':
            print("WARNING: Empty text after parsing \n"+html_text)
            return extracted_text

        cleaned = self.clean(extracted_text)
        if cleaned == '':
            print("WARNING: Empty text after cleaning \n"+extracted_text)
            return cleaned

        return cleaned
    
    
    def clean(self, text):

        cleaned_text = text

        # F Reference
        f_ref = "\/f\.[0-9]{1}[a-z]{2}\/"
        cleaned_text = re.sub(re.compile(f_ref), '', cleaned_text)

        # Keep only allowed characters
        cleaned_text = filter(self.isAllowedChar, cleaned_text)

        # Take out roman literals at the beginning of lines
        roman_number_regex = "(\s*M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.{0,1}\s+)"
        cleaned_text = re.sub(re.compile('\n'+roman_number_regex), ' ', '\n'+cleaned_text)
        
        # TABULA [ROMAN_NUMBER]
        #tabula_regex = "TABULA "+roman_number_regex
        #cleaned_text = re.sub(re.compile(tabula_regex), '', cleaned_text)

        # Remove numbers at the end of a line
        end_numbers = "[0-9]+$"
        cleaned_text = re.sub(re.compile(end_numbers), '', cleaned_text)

        # Remove error info
        cleaned_text.replace("an error occurred while processing this directive ",'')

        # Compress whitespaces
        cleaned_text = cleaned_text.replace('\xc2\xa0'.decode('utf-8'), '')
        cleaned_text = cleaned_text.replace('\r\n', ' ')
        cleaned_text = cleaned_text.replace('\n', ' ')
        cleaned_text = re.sub('\s+', ' ', cleaned_text ).strip()
        
        # Remove title, if all uppercase
        #title_regex = "^\s*([A-Z\.,\/#!$%\^&\*;:{}=\-_`~()\s]+)([A-Z])"
        #cleaned_text = re.sub(re.compile(title_regex), r'\2', cleaned_text)
        
        # Remove copyright info
        copy_regex = "Latin edition and English translation Copyright .*"
        cleaned_text = re.sub(re.compile(copy_regex), '', cleaned_text)

        return cleaned_text
    
    
    def isAllowedChar(self, char):
        return char.isalpha() or char.isspace() or char in [allowed for allowed in self.allowed_non_literal]
