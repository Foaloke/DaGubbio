'''
Created on 15 Aug 2017

@author: mtonnicchi
'''

import unittest
import dagubbio.utils.config as cfg
import dagubbio.utils.sourceutils as su
import dagubbio.acquirer.textcleaner as tc

class TextCleaner_Text(unittest.TestCase):


    def setUp(self):
        self.config = cfg.Config('../../config.ini')        
        allowed_non_literal = self.config.read_symbol_list(self.config.section('TEXT_CLEANING')['allowed_non_literal'])   
        self.text_cleaner = tc.TextCleaner(allowed_non_literal)
        self.text_before_cleaning = su.load_source('../../resources/test/text_cleaner_samples', 'text_before_cleaning.txt')
        self.text_cleaned = su.load_source('../../resources/test/text_cleaner_samples', 'text_cleaned.txt')
        self.html_text = su.load_source('../../resources/test/text_cleaner_samples', 'html_text.html')
        self.html_text_cleaned = su.load_source('../../resources/test/text_cleaner_samples', 'html_text_cleaned.txt')
        self.utf8_html = su.load_source('../../resources/test/text_cleaner_samples', 'utf8_html.html')
        self.utf8_html_text = su.load_source('../../resources/test/text_cleaner_samples', 'utf8_html_text.txt')


    def testWhenCleaning_thenCleaningIsCorrect(self):
        cleaned = self.text_cleaner.clean(self.text_before_cleaning)
        self.assertEqual(self.text_cleaned, cleaned)
        
        
    def testWhenCleaningHTML_thenCleaningIsCorrect(self):
        cleaned = self.text_cleaner.clean_text_from_html_file(self.html_text)
        print(cleaned)
        self.assertEqual(self.html_text_cleaned, cleaned)


    def testWhenCleaningUTF8AndEntitiesEncodedHTML_thenCorrectCharactersIsPreserved(self):
        cleaned = self.text_cleaner.clean_text_from_html_file(self.utf8_html)
        self.assertEqual(self.utf8_html_text, cleaned)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()