import os, ROOT, aa, argparse
import shutil 
from SC_PARAMETERS import SC_PARAMETER_DIC as SCPD


class webpage_maker:

    def __init__(self):

        self.DAU_DIR   = os.environ["DOM_AUTOPSY_DIR"]
        self.PLOTS_DIR = DAU_DIR + "/plots"
        self.WEB_DIR   = DAU_DIR + "/dom_autopsy_web"

    def publish( self, server = "jseneca@login.nikhef.nl:~/public_html" ):
        # you can now copy the webdir to a webserver -- for example
        cmd = ''
        if force_recreate:
            cmd = "scp -r {0} {1}".format( self.WEB_DIR, server )
        else:
            cmd = "scp -r {0} {1}".format( self.WEB_DIR + "/KM3NeT*", server + "/dom_autopsy_web" )

        os.system(cmd)



    def clean( self ):
        if not os.path.isdir( self.WEB_DIR ):
            print("ERROR: Directory {} not found.".format( self.WEB_DIR ) )
            raise ValueError
        else:
            shutil.rmtree( self.WEB_DIR )

    def make( self ):

        # The following puts root in batch mode; you will not see graphics
        # output on your screen.
        ROOT.gROOT.SetBatch( True )

        # We will use the WebFile object;
        # no need, compile, you can just include the .hh file...
        aa.include( os.environ['AADIR']+"/ana/histogrammer/WebFile.hh")


        if not os.path.isdir( self.WEB_DIR ):
            os.system('mkdir ' + self.WEB_DIR)

        W = ROOT.WebFile( self.WEB_DIR )

        W.write("<h1> DOM Autopsy <h1> <br> ")

        W.write("<h3> Folder structure: DET_IT > RUN_N > SC_PARAMETER <h3> <br> ")

        IMG_DIR = self.WEB_DIR + '/' + 'images'

        if not os.path.isdir( IMG_DIR ):
            os.mkdir( IMG_DIR )

        for det_obj in sorted( os.listdir( self.PLOTS_DIR ) ):

            DET_DIR     = self.PLOTS_DIR + '/' + det_obj
            WEB_DET_DIR = self.WEB_DIR  + '/' + det_obj
            if not os.path.isdir( DET_DIR ):
                continue
            if not os.path.isdir( WEB_DET_DIR ):
                os.mkdir( WEB_DET_DIR )

            W.write("<a href=\"{0}\">{1}</a> ".format(det_obj + "/" + det_obj + ".html", det_obj) )
            n_status_plots = 0
            n_run_folders  = 0

            Wdet = ROOT.WebFile( WEB_DET_DIR, det_obj + ".html")
            Wdet.write("<h1> Runs for detector {0} <h1> <br> ".format( det_obj ) )
            Wdet.write("<h3> LOOK UNDER AND RIGHT (I'm not good with html) <h3> <br> " )

            for run_obj in sorted( os.listdir( DET_DIR ), reverse = True ):
                RUN_DIR     = DET_DIR + '/' + run_obj
                WEB_RUN_DIR = WEB_DET_DIR + '/' + run_obj

                if os.path.isdir( RUN_DIR ):
                    if not os.path.isdir( WEB_RUN_DIR ):
                        n_run_folders += 1
                        os.mkdir( WEB_RUN_DIR )

                    Wdet.write("<a href=\"{0}\">{1}</a> <br>".format(run_obj + "/" + run_obj + ".html", run_obj) )
                    n_param_folders = 0

                    Wrun = ROOT.WebFile( WEB_RUN_DIR, run_obj + ".html")

                    Wrun.write("<h1> Slow Control parameters for (up to) run {0} <h1> <br> ".format( run_obj ) )

                    Wpars = {}
                    for par_obj in sorted( os.listdir( RUN_DIR ) ):

                        print("parobj: ", par_obj )
                        param = par_obj
                        param = param.replace('SCP__', '')
                        param = param.replace('SCP_', '')
                        param = param.replace('normlog_', '')
                        param = param.replace('norm_', '')
                        param = param.replace('log_', '')
                        param = param.replace('_D0', '_D_')
                        param = param[:param.find("_D_")]

                        PAR_DIR     =     RUN_DIR + '/' + param
                        WEB_PAR_DIR = WEB_RUN_DIR + '/' + param
                        print( "param:", param )
                        if not os.path.isdir( WEB_PAR_DIR ):
                            n_param_folders += 1
                            os.mkdir( WEB_PAR_DIR )

                            Wrun.write("<a href=\"{0}\">{1}</a> <br>".format(param + "/" + param + ".html", param) )
                            if par_obj[-4:-2] == '.p':
                                Wrun.write("{0} ({1})<br>".format( SCPD[param][1], SCPD[param][0] ) )

                            Wpars[param] = ROOT.WebFile( WEB_PAR_DIR, param + ".html")

                        if par_obj[-4:] == '.png':
                            print( "parobj inside:", par_obj )
                            Wpars[param].write_img_tag( '../../../images/' + par_obj, par_obj )
                            shutil.copyfile( RUN_DIR + '/' + par_obj, IMG_DIR + '/' + par_obj )
                            print( "Wrote {0}".format( IMG_DIR + '/' + par_obj ) )

                    del Wpars
                    #Wrun.write("<div>{0} plots</div> <br>".format( n_plots ) )
                    del Wrun
                    Wdet.write("<div>{0} parameter folders.</div> <br>".format( n_param_folders ) )

                elif run_obj[-4:] == '.png':
                    n_status_plots += 1
                    Wdet.write_img_tag( '../images/' + run_obj, run_obj )
                    shutil.copyfile( DET_DIR + '/' + run_obj, IMG_DIR + '/' + run_obj )
                    print( "Wrote {0}".format( IMG_DIR + '/' + run_obj ) )
                    continue
                del Wdet
                W.write("<div>{0} status plots, {1} run folders.</div> <br>".format( n_status_plots, n_run_folders ) )


        del W # destructor closes the file
