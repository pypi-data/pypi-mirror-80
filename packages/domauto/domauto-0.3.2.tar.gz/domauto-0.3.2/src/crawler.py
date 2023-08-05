import glob, os, pickle 
from numpy import random

from fs.sshfs import SSHFS
from fs.osfs import OSFS

from .iolib    import *
from .classlib import *
from .clean_files import *

import km3pipe

#Produces run_dic, a dictionary of all bad runs, and interesting runs (such as death runs)
#dominfo_dic, a dictionary of all doms, containing information on their status over runs

import platform
import getpass
print(platform.python_version())

class crawler:
    
    def  __init__(self,
                  JRA_DIR = "/sps/km3net/repo/data/raw/quality/root/",
                  verbose = 0):

        self.verbose = verbose
        self.JRA_DIR = JRA_DIR

        if os.path.isdir( self.JRA_DIR ):
            self.my_fs = OSFS( self.JRA_DIR )
        elif all(v in os.environ for v in ["LYON_USERNAME", "LYON_PASSWORD"] ):
            self.my_fs = SSHFS( host = "cca.in2p3.fr",
                                user = os.environ["LYON_USERNAME"],
                                passwd = os.environ["LYON_PASSWORD"],
                                timeout = 60 )
        else:
            self.my_fs = SSHFS( host = "cca.in2p3.fr",
                                user = input( "Lyon username: " ),
                                passwd = getpass.getpass(),
                                timeout = 60)

        self.run_dic = {}
        self.dominfo_dic = {}    # key will be a (line,floor) tupledominfo_dic = {}

        if verbose >= 2: print( "Fetching database streams...", end='' )
        self.sds = km3pipe.db.StreamDS()
        if verbose >= 2: print( " done." )

        if verbose >= 2: print( "Made crawler." )
        

    def crawl( self,
               detector,
               OUTRUNS,
               OUTDOMS,
               death_threshold   = 10,  #minimum amount of dead runs to be counted as "dead"
               coma_threshold    = 30,   #minimum amount of dead runs to be counted as "coma"
               passout_threshold = 1 ): #minimum amount of dead runs to be counted as "passout"

        files = {}
            
        for dir_detector in sorted( self.my_fs.listdir( '.' ) ):
            if( detector in DETID_to_OID( dir_detector, self.sds ) ) or ( dir_detector in detector ):
                if self.verbose >= 2: print(" found detector directory: {0}".format(dir_detector))
                files[dir_detector] = []
                for f in self.my_fs.glob( "{}/*/KM3NeT*root".format( dir_detector ) ):
                    files[dir_detector].append( f.path )
                self.run_dic['goodruns']  = [] #list of good JRA runs
                self.run_dic['badruns']   = [] #list of bad JRA runs
                self.run_dic['comaruns']  = {} #dictionary of key: run, value: list of omkeys of comadoms
                self.run_dic['deathruns'] = {} #dictionary of key: run, value: list of omkeys of deathdoms


        if not len( files.items() ):
            if self.verbose >= 1: print("ERROR: no files found.")
            raise ValueError

        # read the jra files
        for det, fdic in files.items():
            print( "detector {0}, total {1} files".format( det, len( fdic ) ) )
            for i, jrafile in enumerate( fdic ):
                if self.verbose >= 2: print( "detector {} file {} of {}".format( det, i, len(fdic) ) )
                process_jra_file( self.JRA_DIR + jrafile, det,
                                  self.run_dic,
                                  self.dominfo_dic,
                                  self.verbose )

        R = getruns( self.dominfo_dic )[-passout_threshold]
        print( "\nThe following were once alive, but are dead in the last {0} runs; i.e since at least run {1}:".format( passout_threshold, R.string() ) )




        #Categorize runs
        for dom_info in sorted( self.dominfo_dic.values(), key = lambda obj: obj.index ):

            dom_info.init_status_runs( death_threshold = death_threshold,
                                       passout_threshold = passout_threshold )
            if dom_info.is_empty():
                print( "DU{0}DOM{1}, empty".format(dom_info.du, dom_info.floor) )
                continue
            if not len( dom_info.live_runs ) :
                print( "DU{0}DOM{1}, always dead".format(dom_info.du, dom_info.floor) )
                continue
            try:
                if last_run( dom_info.live_runs ).index < R.index :
                    death_run = dom_info.get_death_run( death_threshold )
                    print( "DU{0}DOM{1}, dead since {2}".format(dom_info.du, dom_info.floor, death_run.string() ) )
                    death_run.add_note( "DU{0}DOM{1} death".format( dom_info.du, dom_info.floor ) )
                    if death_run in self.run_dic['deathruns']:
                        self.run_dic['deathruns'][death_run].append( (dom_info.du, dom_info.floor) )
                    else:
                        self.run_dic['deathruns'][death_run] = [ (dom_info.du, dom_info.floor) ]

            except AttributeError as ae:
                print( "ERROR: {0}".format( ae ) )

            #Define coma as a very long passout
            coma_runs = dom_info.get_passout_runs( coma_threshold )
            for coma_run in coma_runs:
                if coma_run in self.run_dic['comaruns']:
                    self.run_dic['comaruns'][coma_run].append( (dom_info.du, dom_info.floor) )
                else:
                    self.run_dic['comaruns'][coma_run] = [ (dom_info.du, dom_info.floor) ]
                    
        outfile_runs = open( OUTRUNS, 'wb')
        outfile_doms = open( OUTDOMS, 'wb')
        pickle.dump( self.run_dic, outfile_runs )
        pickle.dump( self.dominfo_dic, outfile_doms )
        outfile_runs.close()
        outfile_doms.close()

        return 0
        
    def pront_dominfo( dominfo_dic ):
        pront( dominfo_dic )

    def pront( self ):
        print( "runs with bad jra files : ", [ obj.string() for obj in self.run_dic['badruns'  ] ] )
        print( "runs with coma : ",          [ obj.string() for obj in self.run_dic['comaruns' ] ] )
        print( "runs with deaths : ",        [ obj.string() for obj in self.run_dic['deathruns'] ] )
        print( "dead  in all runs : ", sorted( [ d for d in self.dominfo_dic if not len( self.dominfo_dic[d].live_runs ) ] ) )
        print( "alive in all runs : ", sorted( [ d for d in self.dominfo_dic if self.dominfo_dic[d].alive_in_runs( getruns( self.dominfo_dic ) ) ]) )



    def print_missing_runs(self,
                           detector,
                           RUNSFILE,
                           OUTFILE ):

        print( 'detector: ',  detector )
        try:
            runsfile = open( RUNSFILE, "rb" )
        except IOError:
            print( "ERROR: file {0} could not be found.".format( RUNSFILE ) )
            raise IOError

        run_dic = pickle.load( runsfile )

        outfile_runlist = open( OUTFILE, 'w')

        detectors = None
        if detector and detector[1:] == 'RCA':
            detectors = [ OID_to_DETID( det_name ) for det_name in self.sds.detectors().OID.values if detector in det_name ]
        else:
            print( 'Detector argument not recognized. Loading all detector configurations.' )
            detectors = [ OID_to_DETID( det_name ) for det_name in self.sds.detectors().OID.values ]

        print( "Finding mising runs for {0}".format( detectors ) )


        for det in detectors:

            print( "\nDetector {0}".format( det ) )
            outfile_runlist.write( "\nDetector {0}:\n".format( det ) )

            try:
                runtable = self.sds.runs( detid = DETID_to_OID( det ) )
            except ValueError as Verr:
                print( Verr )
                print( 'Continuing...' )
                continue

            if runtable is None:
                print( "Empty runtable, continuing." )
                continue

            runlist = list( runtable.loc[ runtable.loc[:, 'RUNSETUPNAME'].str.startswith( 'PHYS'), ['RUN', 'JOBTARGET'] ].values )

            if not len( runlist ):
                continue

            goodruns = get_det_id_runs( run_dic['goodruns'], det )
            badruns  = get_det_id_runs( run_dic['badruns'], det )

            missing_runs = []
            on_runs      = []
            off_runs     = []
            other_runs   = []
            for run, job_target in runlist:
                if job_target == 'On':
                    if run in [ run.n for run in goodruns ] + [ run.n for run in badruns ]:
                        print('On run in goodruns or badruns')
                    on_runs.append( run )
                elif job_target == 'Off':
                    if run in [ run.n for run in goodruns ] + [ run.n for run in badruns ]:
                        print('Off run in goodruns or badruns')
                    off_runs.append( run )
                elif job_target != 'Run':
                    if run in [ run.n for run in goodruns ] + [ run.n for run in badruns ]:
                        print('Run run in goodruns or badruns')
                    other_runs.append( run )
                elif job_target == 'Run' and run not in [ run.n for run in goodruns ] + [ run.n for run in badruns ]:
                    missing_runs.append( run )

            print( "n total PHYS runs: ", len( runlist ) )
            print( ">   n    good runs: ", len( goodruns ) )
            print( ">   n bad JRA runs: ", len( badruns ) )
            print( ">   n    'on' runs: ", len( on_runs ) )
            print( ">   n   'off' runs: ", len( off_runs ) )
            print( ">   n 'other' runs: ", len( other_runs ) )
            print( ">   n missing runs: ", len( missing_runs ) )

            outfile_runlist.write( "Badruns:\n" )
            print( "\nBad runs: " )
            for badrun in sorted( badruns ):
                outfile_runlist.write( str( badrun.n ) + "\n")
                print( " - {0}".format( badrun.n ), end = '')
            outfile_runlist.write( "Missing runs:\n" )
            print( "\nMissing runs: " )
            for missing_run in sorted( missing_runs ):
                outfile_runlist.write( str( missing_run ) + "\n")
                print( " - {0}".format( missing_run ), end = '')

        outfile_runlist.close()
