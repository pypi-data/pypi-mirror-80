

class Run( object ):

    def __init__( self, det_id, n, note = ''):
        self.det_id = det_id
        self.n      = n  
        self.notes  = [note]
        self.index  = self.get_index()

    def __hash__(self):
        return hash( self.index )

    def __eq__(self, other):
        return other and self.index == other.index

    def __ne__(self, other):
        return not other or self.index != other.index

    def __lt__(self, other):
        return self.index < other.index

    def __gt__(self, other):
        return self.index > other.index

    def string( self ):                
        return '{0}_{1}'.format( self.det_id, self.n )

    def get_index( self ): #int value to sort easily
        """
        function to return a string that can be use to nicely sort runs
        """
        return int( self.det_id.split('_')[-1] + str(self.n).zfill(5) )

    def add_note( self, note ):
        self.notes.append( note )
        
    def dump_notes( self, path ):
        outfile = open( path + "/RUN{0}_notes".format( self.n ), 'w')
        for note in self.notes:
            outfile.write( note + "\n" )
        outfile.close()

    def __repr__( self ):
        return "{} - {} - {}".format( self.det_id, self.n, self.notes ) 

    



class DomInfo( object ):

    def __init__( self, du, floor ):
        self.du        = du
        self.floor     = floor
        self.index  = self.get_index()

        self.detectors = []
        self.live_runs = [] #Runs with data
        self.dead_runs = [] #Runs with no data

        self.passout_runs = []   #Live runs followed by temporary death
        self.death_run    = None #Last live run followed by permanent death (only dead runs)
        self.healthy_runs = []   #Live runs which are not passout nor death runs

    def init_status_runs( self,
                          death_threshold,
                          passout_threshold,
                          det_id = None):
        self.death_run    = self.get_death_run(      death_threshold, det_id)
        self.passout_runs = self.get_passout_runs( passout_threshold, det_id) 
        self.healthy_runs = [ run for run in self.live_runs if ( ( not det_id or run.det_id == det_id )
                                                                 and run not in self.passout_runs
                                                                 and run != self.death_run ) ]

    def get_passout_runs(self,
                         threshold = 1,
                         det_id = None):
        self.live_runs = get_time_sorted_runs( self.live_runs )
        passout_runs = []
        for irun, run in enumerate( self.live_runs ):
            if ( not det_id or run.det_id == det_id )\
            and run.index + 1 in get_sorted_indices( self.dead_runs )\
            and run != self.death_run\
            and run.index < self.live_runs[irun + 1].index - threshold:
                passout_runs.append( run )
        return passout_runs

    def get_death_run( self, threshold = 1, det_id = None):
        if not self.dead_runs:
            return None
        last_live_run = last_run( self.live_runs, det_id )
        if not last_live_run:
            return None
        return  last_live_run if last_live_run.index < last_run( self.dead_runs, det_id ).index - threshold else None 

    def is_empty(self):
        return len(self.live_runs) == 0 and len(self.dead_runs) == 0

    def alive_in_runs ( self, runlist ):
        return all( run in self.live_runs for run in runlist )

    def filter_det( self, det_id = None ):
        if det_id == None:
            return self

        self.live_runs = get_time_sorted_runs( self.live_runs, det_id )
        self.dead_runs = get_time_sorted_runs( self.dead_runs, det_id )
        if self.is_empty():
            return None
        
        self.passout_runs = get_time_sorted_runs( self.passout_runs, det_id )
        self.healthy_runs = get_time_sorted_runs( self.healthy_runs, det_id )
        if not self.death_run or self.death_run.det_id != det_id:
            self.death_run = None
        return self

    def filter_runs( self, runlist = [] ):
        if not len( runlist ):
            return self

        self.live_runs = [run for run in self.live_runs if run.n in runlist]
        self.dead_runs = [run for run in self.dead_runs if run.n in runlist]
        if self.is_empty():
            return None
        
        self.passout_runs = [run for run in self.passout_runs if run.n in runlist]
        self.healthy_runs = [run for run in self.passout_runs if run.n in runlist]
        if not self.death_run or self.death_run.det_id not in runlist:
            self.death_run = None
        return self

    def get_index( self ):
        """
        function to return a string that can be use to nicely sort doms
        """
        return int (str( self.du ).zfill( 3 ) + str( self.floor ).zfill( 2 ) )

def get_det_id_runs( runs, det_id ):
    """
    Get the sublist of runs which have det_it
    """
    return [ run for run in runs if run.det_id == det_id ]


def get_sorted_indices( da_objects ):
    """
    Get indices of a list of objects, sorted
    """
    indices = []
    for obj in da_objects:
        indices.append( obj.index )
    return sorted( indices )

def get_sorted_run_n( runs ):
    """
    Get run numbers of a list of runs, sorted
    """
    run_ns = []
    for run in runs:
        run_ns.append( run.n )
    return sorted( run_ns )


def get_time_sorted_runs( runs, det_id = None):
    out_runs = runs
    if det_id:
        out_runs = get_det_id_runs( runs, det_id )
    return sorted( out_runs, key=lambda obj: obj.index )

               
def last_run( runs, det_id = None):
    if runs:
        last_run = get_time_sorted_runs( runs )[-1]
        return last_run if ( not det_id or last_run.det_id == det_id ) else None
    else:
        return None
