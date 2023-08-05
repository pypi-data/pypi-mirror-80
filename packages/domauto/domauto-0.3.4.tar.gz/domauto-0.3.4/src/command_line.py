#!/usr/bin/env python3

"""
DomAuto.

Usage:
     domauto auto        [ -o=<outpath>  -d=<detector>                               -t=<threshold> -v=<v> -F ]
     domauto crawl       [               -d=<detector> -f=<doms_file> -r=<runs_file> -t=<threshold> -v=<v> -F ]
     domauto plot-status [ -o=<outpath>  -d=<detector> -f=<doms_file> -r=<runs_file>                -v=<v> -F ]
     domauto plot-scp    [ -o=<outpath>  -d=<detector>                -r=<runs_file> -p=<parameter> -v=<v> -F ]
     domauto webpage     [               -d=<detector>                                              -v=<v> -F ]
     domauto plot-scp <start> [ <end> -o=<outpath> -d=<detector>                     -p=<parameter> -v=<v> -F ]


-f --doms_file=<doms_file>        Pickle dom info file
-r --runs_file=<runs_file>        Pickle run info file
-d --detector=<detector>          Detector code, ORCA, or ARCA [default: ORCA].
-o --outpath=<outpath>            Output path [default: ]
-p --parameter=<parameter>        Will use all hits on parameter keyword, or use short, long, all for whole lists [default: short].
-F --force                        Force recreate
-t --threshold=<threshold>        Set overall threshold in # of runs, or death, coma, passout separated by spaces [default: 10 30 1].
-v --verbose=<v>                  Verbose [default: 0]
-h --help                         Display this screen
"""        
    
def main():

    import docopt
    args = docopt.docopt( __doc__ )
    verbose = int( args['--verbose'] )
    if verbose >= 2: print( "args: ", args )

    import pickle, os
    from .crawler        import crawler
    from .status_plotter import status_plotter
    from .scp_plotter    import scp_plotter
    from .classlib       import Run
    from .iolib          import get_detectors

    if not args['<start>']:
        OUTDOMS = args['--doms_file'] if args['--doms_file'] else 'DOMINFO_DIC_{0}.pickle'.format( args['--detector'] )
        OUTRUNS = args['--runs_file'] if args['--runs_file'] else 'RUNINFO_DIC_{0}.pickle'.format( args['--detector'] )
    
        print( "Added for detector {} outdoms file {}, and outruns file {}.".format( args['--detector'],
                                                                                     OUTDOMS,
                                                                                     OUTRUNS ) )

    thresholds = args['--threshold'].split(' ') if ' ' in args['--threshold'] else [ args['--threshold'] ] * 3

    #################    

    if args['crawl'] or args['auto']:
        

        #if args['--force']:
        #    clean_files( args['--detector'].split(' ') )
        #elif os.path.isfile( OUTRUNS ) and os.path.isfile( OUTDOMS ):
        #    print( "Files for {0} already exist, continuing.".format( args['--detector'] ) )
        #    if not args['auto']: exit()

        mycrawler = crawler( verbose = verbose )

        mycrawler.crawl( args['--detector'],
                         OUTRUNS,
                         OUTDOMS,
                         death_threshold   = int( thresholds[0] ),
                         coma_threshold    = int( thresholds[1] ),
                         passout_threshold = int( thresholds[2] ) )

        mycrawler.pront()
        mycrawler.print_missing_runs( args['--detector'],
                                      OUTRUNS,
                                      args['--detector'] + "missing_runs.txt")




    #######################

    if args['plot-status'] or args['auto']:

        myplotter = status_plotter( verbose = verbose )

        if not os.path.isfile( OUTRUNS ):
            print( "{0} not found, exiting.".format( OUTRUNS ) )
            exit()

        if not os.path.isfile( OUTDOMS ):
            print( "{0} not found,exiting.".format( OUTDOMS ) )
            exit()
            
        myplotter.plot( args['--detector'],
                        OUTDOMS,
                        OUTRUNS,
                        args['--outpath'],
                        args['--force'] )
        
        print( "Status plotting over." )






    ##########################

    if args['plot-scp'] or args['auto']:

        if args['<start>']:
            import km3pipe
            sds = km3pipe.db.StreamDS()
            
            if 'RCA' in args['--detector']:
                if args['--detector'][1:] == 'RCA' and verbose >= 1: print("WARNING: you did not select a detector configuration. Will print run number for all detectors.")
                detectors = get_detectors( args['--detector'], sds )
            else:
                detectors = [ args['--detector'] ] 

            print( detectors )
            start = int( args['<start>'] )
            end   = int( args['<end>'] ) if args['<end>'] else start
            RUN_LIST =  [ ( Run( det, start ), [] ) for det in detectors]
            RUN_RANGE = [ 0, end - start ]

        #----------------------------------

        else:

            if not os.path.isfile( OUTRUNS ):
                print( "{0} not found, exiting.".format( OUTRUNS ) )
                exit()
                
            RUN_DIC = pickle.load( open( OUTRUNS, 'rb' ) )
            
            RUN_LIST = []
            RUN_LIST.extend( RUN_DIC['deathruns'].items() )
            RUN_LIST.extend( RUN_DIC['comaruns'].items() )
            RUN_RANGE = [5, 2]
            #RUN_APPENDIX = [ ( dacl.Run( det_id = MAN_RUN_LIST[0], n = int(run_n) ), [(-1, -1)] ) for run_n in MAN_RUN_LIST[1:] ] if MAN_RUN_LIST else []
            #RUN_LIST.extend( RUN_APPENDIX )
        
        KEYWORD = args['--parameter'].upper()
        if KEYWORD == 'ALL': KEYWORD = 'LONG'
    
        myplotter = scp_plotter( verbose = verbose )

        myplotter.batch_plot( RUN_LIST,
                              OUTPATH = args['--outpath'],
                              SCP_KEYWORD = KEYWORD,
                              RUN_RANGE = RUN_RANGE,
                              REWRITE   = args['--force'])





    ###################

    if args['webpage'] or args['auto']:
        if args['--force']:
            web_maker.clean()


        self.OUTDIR = "{0}/RUN{1}".format( self.PLOTS_DIR + "/" + self.detector, MAXRUN ) 
        make_plot_dirs( self.OUTDIR )


        if len( glob.glob( self.OUTDIR + "/*{0}*".format( PARAM_NAME) ) ) >= 5 and not args['--force']:
            print( "Directory exist and has been filled. Aborting." )
            raise ValueError


        DET_DIR = PLOTS_DIR + "/" + run.det_id 
        outfile = open( DET_DIR + "/runs_notes.md", 'a')
        for note in run.notes:
            outfile.write("RUN{0}:".format( run.n ) + note + "\n" )
        outfile.close()
        OUTDIR = "{0}/RUN{1}".format( DET_DIR, run.n ) 
        make_plot_dirs( OUTDIR )
        run.dump_notes( OUTDIR )





if __name__ == '__main__':
    main()


            #        PLOTS_DIR = './plots'
            #        if not os.path.isdir( PLOTS_DIR ):
            #            print("Plots directory not found.")
            #            raise ValueError
