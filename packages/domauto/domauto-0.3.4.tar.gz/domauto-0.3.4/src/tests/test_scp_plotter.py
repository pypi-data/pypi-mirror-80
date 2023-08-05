import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from unittest import TestCase
from src.scp_plotter import scp_plotter

__author__ = "Jordan Seneca"
__credits__ = []
__license__ = "MIT"
__maintainer__ = "..."
__email__ = "jseneca@km3net.de"

class TestClasses( TestCase ):

    def test_null( self ):
        
        assert 1

    def setUp( self ):

        self.scp_plotter = scp_plotter()
    
    def test_scp_plotter( self ):

        self.plotter = scp_plotter()

        assert 1

    def make_scp_plot( self ):
        self.plotter.plot( 'KM3NeT_00000043', 4300, 4302 )

        assert 1
