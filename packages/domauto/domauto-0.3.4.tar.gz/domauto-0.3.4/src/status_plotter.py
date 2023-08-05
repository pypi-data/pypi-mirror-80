import os, pickle, glob

from .plotlib import *
from .iolib   import *

import km3pipe

class status_plotter:
    
    def __init__( self,
                  verbose = 0):
        
        self.verbose = verbose
        self.sds = km3pipe.db.StreamDS()

    def plot( self,
              detector,
              domsfile,
              runsfile,
              outpath = '',
              force_recreate = False ):

        try:
            df = open( domsfile, "rb" )
        except IOError:
            print( "ERROR: file {0} could not be found.".format( domsfile ) )
            raise IOError

        try:
            rf = open( runsfile, "rb" )
        except IOError:
            print( "ERROR: file {0} could not be found.".format( runsfile ) )
            raise IOError

        dominfo_dic = pickle.load( df )
        run_dic     = pickle.load( rf )
              
        detectors = get_detectors( detector,
                                   self.sds )

        for det in detectors:
            runtable = self.sds.runs( detid = DETID_to_OID( det, self.sds ) )
            runlist = list( runtable.loc[ runtable.loc[:, 'RUNSETUPNAME'].str.startswith( 'PHYS'), 'RUN' ].values )
            if not len( runlist ):
                continue


            print( "Plotting status of {}".format( det ), end = '')
            try:
                print( "({})...".format( DETID_to_OID( det, self.sds ) ) )
            except ValueError:
                print( " name error..." )

            outplot_name = "{}{}_status_PLOTINFO".format( outpath, DETID_to_OID( det, self.sds ) )

            title = "Status of DOMs of {0}".format( det )

            plot_status_DET( dominfo_dic,
                             runlist,
                             outplot_name,
                             badruns = run_dic['badruns'],
                             det_id  = det,
                             title   = title,
                             accent  = True,
                             force_recreate = force_recreate,
                             verbose = self.verbose)


#            PLOT_DIR = "plots/{0}/".format( det )
#            if not os.path.isdir( PLOT_DIR ):
#                make_plot_dirs( PLOT_DIR )
#            elif force_recreate:
#                for f in glob.glob( PLOT_DIR + "*status*.p*" ): os.remove( f )
