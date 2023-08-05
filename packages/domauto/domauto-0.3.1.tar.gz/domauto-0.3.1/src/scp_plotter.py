import os, glob

from .plotlib import *
from .iolib   import *
from .SC_PARAMETERS import *

import km3pipe


class scp_plotter:

    def __init__( self,
                  verbose = 0):

        self.verbose = verbose
        if self.verbose >= 2: print("Fetching database streams...", end='')
        self.sds = km3pipe.db.StreamDS()
        if self.verbose >= 2: print(" done.")
        
        
    def fetch( self,
               DETECTOR,
               PARAM_NAME,
               MINRUN,
               MAXRUN ):


        scp_dataframe = self.sds.get( 'datalognumbers',
                                      detid          = DETECTOR,
                                      minrun         = MINRUN,
                                      maxrun         = MAXRUN,
                                      parameter_name = PARAM_NAME )
        
        try:
            if scp_dataframe.size < 1:
                print("ERROR: No data found for detector {0}, runs {1}-{2} parameter {3}.".format( DETECTOR, MINRUN, MAXRUN, PARAM_NAME ) )
                raise ValueError
        except AttributeError:
            print("ERROR: No data found for detector {0}, runs {1}-{2} parameter {3}.".format( DETECTOR, MINRUN, MAXRUN, PARAM_NAME ) )
            raise ValueError

        return scp_dataframe


    
        
    def plot( self,
              KM3NET_DETECTOR,
              MINRUN,
              MAXRUN,
              OUTPATH = None,
              PARAM_NAME    = "",
              PARAM_UNIT    = "",
              PARAM_MEANING = "",
              ACCENT = [],
              HISTOGRAM = False,
              SCATTER   = False,
              CACHE     = False,
              REWRITE   = False,
              SAVE_FIG  = True ):
        """
        Script to create plots of a given detector for a given parameter
        
        """
                
        DETECTOR        = DETID_to_OID( KM3NET_DETECTOR, self.sds )
        DETECTOR_TYPE   = DETECTOR.split("_")[-1]

        print("Fetching CLB map...", end='')
        clbm = km3pipe.db.CLBMap( DETECTOR )
        print(" done.")

        
        if not HISTOGRAM and not SCATTER:
            print("No plotting type was chosen. Please run code again with -histogram, -scatter or both. Aborting.")
            raise ValueError

        print("Fetching data from database (this can take a while)...", end = '')        
        scp_dataframe = self.fetch( DETECTOR,
                                    PARAM_NAME,
                                    MINRUN,
                                    MAXRUN )
        print(" done.")


        
        print("Making DOM plots...", end='')

        outpath_doms = '{}{}_DOMS_SCP_{}_runs{}-{}'.format( OUTPATH,
                                                            DETECTOR,
                                                            PARAM_NAME,
                                                            MINRUN,
                                                            MAXRUN )
            
        plot_DET_DOMs( scp_dataframe,
                       clbm,
                       MINRUN,
                       MAXRUN,
                       PARAM_NAME,
                       PARAM_UNIT,
                       PARAM_MEANING,
                       OUTPATH   = outpath_doms,
                       DETECTOR = DETECTOR,
                       ACCENT = ACCENT,
                       HIST = True,
                       SCAT = True,
                       SAVE_FIG = SAVE_FIG,
                       VERBOSE = self.verbose )

        print(" done.")


        

        print( "Making DU plots..." )

        for norm, log in [(False, False), (False, True), (True, False), (True, True)]:

            print( "Plotting for " + ["no ", ""][norm] + "norm and " + ["no ", ""][log] + "log...", end = '' )

            outpath_dus = '{}{}_DUS_SCP_{}_runs{}-{}_{}{}'.format( OUTPATH,
                                                                   DETECTOR,
                                                                   PARAM_NAME,
                                                                   MINRUN,
                                                                   MAXRUN,
                                                                   ['', 'norm'][norm],
                                                                   ['', 'log'][log] )
            
            plot_DET_DUs( scp_dataframe,
                          clbm,
                          MINRUN,
                          MAXRUN,
                          PARAM_NAME,
                          PARAM_UNIT,
                          PARAM_MEANING,
                          OUTPATH = outpath_dus,
                          DETECTOR = DETECTOR,
                          ACCENT = ACCENT,
                          HIST = HISTOGRAM,
                          SCAT = SCATTER,
                          NORM = norm,
                          LOG = log,
                          SAVE_FIG = SAVE_FIG,
                          VERBOSE = self.verbose)

        print(" done.")




        
    def batch_plot( self,
                    RUN_LIST,
                    OUTPATH,
                    SCP_KEYWORD,
                    RUN_RANGE = [0, 0],
                    REWRITE = False): 

        """
        Create plots of a given detector for a list of parameters

        ENTER LIST AS -l <KM3NeT_detector_name> <run_n1> <run_n2> ...
        """

        try:
            PARAMETER_LIST = SC_PARAMETERS[ SCP_KEYWORD ]
        except KeyError:
            PARAMETER_LIST = [ param_tuple for param_tuple in SC_PARAMETERS[ 'LONG' ] if SCP_KEYWORD.upper() in param_tuple[0].upper() ]

        print( "Run list: " )
        for run in RUN_LIST: print( run )
        print( "Slow Control Parameter list: ")
        for param in PARAMETER_LIST: print( param )

        for run, omkey_list  in RUN_LIST:

            MINRUN = run.n - RUN_RANGE[0]
            MAXRUN = run.n + RUN_RANGE[1] if RUN_RANGE[1] else run.n

            for parameter in PARAMETER_LIST:

                print("\n\n- - - running plot_scp.py for {0} {1}-{2} with parameter {3} - - -\n".format( run.det_id, MINRUN, MAXRUN, parameter[0] ) )

                try:
                    self.plot( run.det_id,
                               MINRUN,
                               MAXRUN,
                               OUTPATH,
                               PARAM_NAME    = parameter[0],
                               PARAM_UNIT    = parameter[1],
                               PARAM_MEANING = parameter[2],
                               ACCENT    = omkey_list,
                               HISTOGRAM = True,
                               SCATTER   = True,
                               CACHE     = False,
                               REWRITE   = REWRITE,
                               SAVE_FIG  = True )
                except ValueError:
                    print( " ... continuing." )
                    continue
        print(" done.")


