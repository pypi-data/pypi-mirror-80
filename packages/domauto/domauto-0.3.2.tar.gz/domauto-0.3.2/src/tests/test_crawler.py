import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from unittest import TestCase
from src.crawler import crawler

__author__ = "Jordan Seneca"
__credits__ = []
__license__ = "MIT"
__maintainer__ = "..."
__email__ = "jseneca@km3net.de"

class TestCrawler( TestCase ):

    def test_null( self ):
        
        assert 1

    def setUp( self ):

        self.crawler = crawler()

        assert 1

    def test_crawler( self ):

        OUTDOMS = 'DOMINFO_DIC_TEST.pickle'
        OUTRUNS = 'RUNINFO_DIC_TEST.pickle'
    
        mycrawler = crawler()
        
        assert 1
        
        #assert 0 == mycrawler.crawl( 'ORCA',
        #                             OUTRUNS,
        #                             OUTDOMS )
