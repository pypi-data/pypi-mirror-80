import os
import glob
FILES_DIR = "files"

def clean_files( detector = '' ):

    if not os.path.isdir( FILES_DIR ):
        os.mkdir( FILES_DIR )
    else:
        for fp in glob.glob( FILES_DIR + '*_INFO_*' + detector + '.pickle' ):
            os.remove( fp )
            print( "Removed {}".format( fp ) )
