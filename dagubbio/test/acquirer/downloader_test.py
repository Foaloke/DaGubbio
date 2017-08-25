'''
Created on 15 Aug 2017

@author: mtonnicchi
'''

import unittest

import dagubbio.utils.config as cfg
import dagubbio.acquirer.downloader_thelatinlibrary as dl
import dagubbio.utils.sourceutils as su

class TestDownloader(unittest.TestCase):

    def setUp(self):
        self.config = cfg.Config('../../config.ini')
        self.downloader = dl.Downloader_LatinLibrary(None, None)
        self.thelatinlibrary_main = su.load_source('../../resources/test/thelatinlibrary_samples', 'thelatinlibrary_main.html')
        self.thelatinlibrary_main_tidy = su.load_source('../../resources/test/thelatinlibrary_samples', 'thelatinlibrary_main_tidy.html')
        self.thelatinlibrary_anchors = su.load_source('../../resources/test/thelatinlibrary_samples', 'thelatinlibrary_anchors.html')
        self.thelatinlibrary_anchors_tidy = su.load_source('../../resources/test/thelatinlibrary_samples', 'thelatinlibrary_anchors_tidy.html')
        self.thelatinlibrary_self_refs = su.load_source('../../resources/test/thelatinlibrary_samples', 'thelatinlibrary_self_refs.html')
        self.thelatinlibrary_self_refs_tidy = su.load_source('../../resources/test/thelatinlibrary_samples', 'thelatinlibrary_self_refs_tidy.html')
        self.thelatinlibrary_links = su.load_source('../../resources/test/thelatinlibrary_samples', 'thelatinlibrary_links.html')
        self.thelatinlibrary_links_tidy = su.load_source('../../resources/test/thelatinlibrary_samples', 'thelatinlibrary_links_tidy.html')
        self.utf8_html = su.load_source('../../resources/test/thelatinlibrary_samples', 'utf8_html.html')
        self.utf8_html_tidy = su.load_source('../../resources/test/thelatinlibrary_samples', 'utf8_html_tidy.html')
        self.thelatinlibrary_encoding_tag_problems = su.load_source('../../resources/test/thelatinlibrary_samples', 'thelatinlibrary_encoding_tag_problems.html')
        self.thelatinlibrary_encoding_tag_problems_tidy = su.load_source('../../resources/test/thelatinlibrary_samples', 'thelatinlibrary_encoding_tag_problems_tidy.html')
        self.expected_options = \
            ['ammianus.html',\
            'apuleius.html',\
            'aug.html',\
            'victor.html',\
            'caes.html',\
            'cato.html',\
            'catullus.shtml',\
            'cic.html',\
            'claudian.html',\
            'curtius.html',\
            'enn.html',\
            'eutropius.html',\
            'florus.html',\
            'frontinus.html',\
            'gellius.html',\
            'sha.html',\
            'hor.html',\
            'justin.html',\
            'juvenal.html',\
            'liv.html',\
            'lucan.html',\
            'lucretius.html',\
            'martial.html',\
            'nepos.html',\
            'ovid.html',\
            'persius.html',\
            'petronius.html',\
            'phaedrus.html',\
            'plautus.html',\
            'pliny1.html',\
            'pliny.html',\
            'prop.html',\
            'quintilian.html',\
            'sall.html',\
            'seneca.html',\
            'sen.html',\
            'silius.html',\
            'statius.html',\
            'suet.html',\
            'sulpicia.html',\
            'tac.html',\
            'ter.html',\
            'tib.html',\
            'valeriusflaccus.html',\
            'valmax.html',\
            'varro.html',\
            'vell.html',\
            'verg.html',\
            'vitruvius.html',\
            'ius.html',\
            'misc.html',\
            'christian.html',\
            'medieval.html',\
            'neo.html']

    def testWhenAPageIsSentForTidying_thenResultIsCorrect(self):
        main_tidied = self.downloader.tidy_html(self.thelatinlibrary_main)
        self.assertEqual(self.thelatinlibrary_main_tidy, main_tidied)

    def testWhenAPageWithAnchorsIsSentForTidying_thenResultIsCorrect(self):
        main_anchors_tidied = self.downloader.tidy_html(self.thelatinlibrary_anchors)
        self.assertEqual(self.thelatinlibrary_anchors_tidy, main_anchors_tidied)

    def testWhenAPageWithEncodingAndTagProblemsIsSentForTidying_thenResultIsCorrect(self):
        thelatinlibrary_encoding_tag_problems_tidied = self.downloader.tidy_html(self.thelatinlibrary_encoding_tag_problems)
        self.assertEqual(self.thelatinlibrary_encoding_tag_problems_tidy, thelatinlibrary_encoding_tag_problems_tidied)

    def testWhenAPageWithSelfNavigationIsSentForTidying_thenResultIsCorrect(self):
        self_refs_tidied = self.downloader.tidy_html(self.thelatinlibrary_self_refs)
        self.assertEqual(self.thelatinlibrary_self_refs_tidy, self_refs_tidied)

    def testWhenAPageWithLinksAndFooterIsSentForTidying_thenResultIsCorrect(self):
        links_tidied = self.downloader.tidy_html(self.thelatinlibrary_links)
        self.assertEqual(self.thelatinlibrary_links_tidy, links_tidied)

    def testWhenMainPageOptionsAreLookedFor_optionsAreCorrectlySelected(self):
        options = self.downloader.get_main_options(self.thelatinlibrary_main)
        self.assertItemsEqual(self.expected_options, options)

    def testWhenAPageWithEncodingMixedWithEntitiesIsSentForTidying_thenResultIsCorrect(self):
        utf8_html_tidied = self.downloader.tidy_html(self.utf8_html)
        self.assertEqual(self.utf8_html_tidy, utf8_html_tidied)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()