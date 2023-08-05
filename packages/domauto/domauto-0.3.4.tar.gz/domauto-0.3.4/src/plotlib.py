#Plotting functions

import os, math, copy, glob
import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np

from .iolib import *
from .classlib import *

N_FLOORS = 19

def handle_fig( fig,
                name,
                save = True,
                show = False,
                dpi = None,
                dimensions = None,
                labelsize  = 'medium',
                titlesize  = 'medium',
                legendsize = 'medium',
                xticksize  = 'small',
                yticksize  = 'small',
                VERBOSE = False): #takes tuple
    if dimensions: fig.set_size_inches( dimensions )
    plt.tight_layout(pad=3.0)

    plt.rcParams.update({'axes.labelsize' : labelsize,
                         'axes.titlesize' : titlesize,
                         'legend.fontsize': legendsize,
                         'xtick.labelsize': xticksize,
                         'ytick.labelsize': yticksize})

    if save:
        for img_format in ['png', 'pdf']:
            plt.savefig( name + '.' + img_format,
                         dpi = dpi,
                         format=img_format)
            if VERBOSE: print( "Saved {0}".format( name + '.' + img_format ) )
    if show:
        plt.draw()
        plt.show()

    plt.cla()



            

def plot_scp_DOM_hist( scp_datagroup,
                       ax,
                       clb,
                       XRANGE,
                       XBINS = 100,
                       YBINS = 100,
                       title = '',
                       x_label = '',
                       y_label = '',
                       accent = False,
                       DATE_FORMAT = "%d/%m/%Y %H:%M"):
    """
    Plot histogram plot of a DOM in ax
    """
    
    raw_data_values = scp_datagroup.loc[:, 'DATA_VALUE'].values
    data_values = np.array([ value for value in raw_data_values if str(value) != 'nan' ] )
    data_min           = min(data_values)
    data_max           = max(data_values)
    data_values_mean   = data_values.mean()
    data_values_spread = data_values.std()
    if not data_values_spread: data_values_spread = 1.
    data_delta         = get_min_diff( data_values )
    if not data_delta: data_delta = 1.
    y_min   = data_min - data_values_spread / 2.
    y_max   = data_max + data_values_spread / 2.
    y_delta = y_max - y_min 
    y_bins  = int(np.ceil( YBINS if  y_delta / data_delta > YBINS else y_delta / data_delta ))

    ax.hist2d( scp_datagroup.loc[:, 'UNIXTIME'].values,
               raw_data_values,
               bins  = [XBINS, y_bins],
               range = [XRANGE, [y_min, y_max]])
    col = ['black', 'red'][accent]
    ax.set_title( title, color = col)
    if x_label: ax.set_xlabel( x_label, color = col)
    if y_label: ax.set_ylabel( y_label, color = col)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(md.DateFormatter( DATE_FORMAT ) )
    ax.set_xticks( get_run_starts( scp_datagroup ))
    ax.tick_params( axis = 'x', rotation = 8 )

    return 1

def plot_scp_DOM_scat( scp_datagroup,
                       ax,
                       clb,
                       XRANGE = None,
                       title = '',
                       x_label = '',
                       y_label = '',
                       accent = False,
                       DATE_FORMAT = "%d/%m/%Y %H:%M"):
    """
    Plot scatter plot of a DOM in ax
    """

    colormap = lambda i: plt.cm.gnuplot2(i/19.)
    scp_datagroup.plot(x = 'UNIXTIME',
                       y = 'DATA_VALUE',
                       ax = ax,
                       style=['.', '*'][accent],
                       legend=False,
                       color=[colormap(clb.floor), 'red'][accent],           
                       xlim = XRANGE )
    col = ['black', 'red'][accent]
    ax.set_title( title, color = col )
    if x_label: ax.set_xlabel( x_label, color = col )
    if y_label: ax.set_ylabel( y_label, color = col )
    ax.xaxis_date()
    ax.xaxis.set_major_formatter( md.DateFormatter( DATE_FORMAT ) )
    ax.grid( True, which = 'minor', axis = 'x')
    ax.set_xticks( get_run_starts( scp_datagroup ), minor = True )
    return 1







def plot_scp_DU_hist( scp_datagroup,
                      clbm,
                      fig,
                      ax,
                      XRANGE,
                      XBINS = 100,
                      NORM = False,
                      LOG  = False,
                      title = '',
                      x_label = '',
                      y_label = '',
                      w_label = '',
                      ACCENT_DOMS = None,
                      VERBOSE = False):
    """
    Plot histogram plot of all DOMs in DU in ax
    """
    du = clbm.upis[ scp_datagroup.iloc[0, :].SOURCE_NAME ].du
    DU_floors = [None] * N_FLOORS
    for (idu, ifloor), clb in clbm.omkeys.items():
        if idu == du: DU_floors[ ifloor ] = "{0} ({1})".format( clb.upi, ifloor )


    map_times = np.linspace(*XRANGE, XBINS) 
    
    data_array    = np.empty((XBINS, N_FLOORS))
    data_array[:, :] = None
    norm_array    = np.zeros( data_array.shape )
    
    for index, entry in scp_datagroup.iterrows():

        itime = np.where( entry.get('UNIXTIME')    <= map_times )[0][0]
        clb_upi   = entry.get('SOURCE_NAME')
        clb_floor = clbm.upis[ clb_upi ].floor
        iclb      = clb_floor

        if math.isnan( data_array[itime, iclb] ):
            data_array[itime, iclb] = 0
            norm_array[itime, iclb] = 0
        data_array[itime, iclb] += entry.get('DATA_VALUE')
        norm_array[itime, iclb] += 1.
    
    norm_array[norm_array == 0] = 1.
    data_array /= norm_array

    if NORM:
        for dom_bin in range( data_array.shape[1] ):
            if not np.any( data_array[ :, dom_bin ] == data_array[ :, dom_bin ] ):
                continue
            row = data_array[ :, dom_bin ]
            clean_row = row[ ~np.isnan( row ) ]
            row_mean = np.mean( clean_row ) if np.mean( clean_row ) else 1
            data_array[ :, dom_bin ] /= row_mean

    if LOG:
        data_array = np.ma.log10( data_array )

    pos = ax.imshow( data_array.transpose(),
                     origin = 'lower',
                     aspect = 'auto',
                     extent = [*XRANGE, 0, N_FLOORS] )
    
    ax.set_yticks(np.arange( N_FLOORS ) + 0.5)
    ax.set_yticklabels( DU_floors )
    ax.set_xticks( get_run_starts( scp_datagroup ))
    plt.setp(ax.get_xticklabels(), rotation=10, ha = 'right')
    if ACCENT_DOMS:
        for accent_dom in ACCENT_DOMS:
            ax.get_yticklabels()[ accent_dom ].set_color('red') 

    ax.set_title( title )
    if x_label: ax.set_xlabel( x_label )
    if y_label: ax.set_ylabel( y_label )
    ax.xaxis_date()
    ax.xaxis.set_major_formatter( md.DateFormatter("%d/%m/%Y %H:%M") )

    cbar = fig.colorbar(pos, ax=ax )
    cbar.set_label( w_label, rotation=90)
    #cbar.set_label((["<{0}>", "log10<{0}>"][LOG] + " ({1})").format( PARAM_MEANING, PARAM_UNIT), rotation=90)

def plot_scp_DU_scat( scp_datagroup,
                      DU_omkeys,
                      ax,
                      XRANGE  = None,
                      NORM    = False,
                      LOG     = False,
                      title = '',
                      x_label = '',
                      y_label = '',
                      ACCENT_DOMS = None,
                      VERBOSE = False):
    """
    Plot scatter plot of all DOMs in DU in ax
    """

    colormap = lambda i: plt.cm.gnuplot2(i/19.)
    clbs = DU_omkeys.values()
    if ACCENT_DOMS:
        for accent_dom in ACCENT_DOMS:
            accent_clb = DU_omkeys.pop( ( list( DU_omkeys.keys() )[0][0], accent_dom) )
            clbs = list( DU_omkeys.values() ) + [accent_clb]
    else:
        ACCENT_DOMS = []
        
    for clb in clbs:

        scp_clb_datagroup = scp_datagroup.loc[scp_datagroup.loc[:, 'SOURCE_NAME'] == clb.upi].copy()
        
        if NORM:
            scp_clb_datagroup.loc[:, 'DATA_VALUE'] /= scp_clb_datagroup.DATA_VALUE.mean()
        try:
            scp_clb_datagroup.plot(
                x = 'UNIXTIME',
                y = 'DATA_VALUE',
                ax=ax,
                label = "Floor{1}:{2}".format(clb.du,
                                              clb.floor,
                                              clb.dom_id),
                style=['.', '*'][clb.floor in ACCENT_DOMS],
                ms   = 10, #marker size
                logy = LOG,
                xlim = XRANGE,
                legend=True,
                color=[colormap(clb.floor), 'red'][clb.floor in ACCENT_DOMS])

        except TypeError as e: #no data to plot
            if VERBOSE: print("Error for floor {0}: {1}".format(clb.floor, e))
            continue

    ax.set_title( title )
    if x_label: ax.set_xlabel( x_label )
    if y_label: ax.set_ylabel( y_label )
    ax.xaxis_date()
    ax.xaxis.set_major_formatter( md.DateFormatter("%d/%m/%Y %Hh") )
    ax.legend(loc=3,fontsize=8)
    ax.grid( True, which = 'minor', axis = 'x')
    ax.set_xticks( get_run_starts( scp_datagroup ), minor = True )






def plot_DET_DOMs( scp_dataframe,
                   clbm,
                   MINRUN,
                   MAXRUN,
                   PARAM_NAME,
                   PARAM_UNIT,
                   PARAM_MEANING,
                   OUTPATH,
                   DETECTOR,
                   ACCENT = None, #list of omkeys
                   HIST = True,
                   SCAT = True,
                   VERBOSE = False,
                   SAVE_FIG = True,
                   SHOW_FIG = False):
    """
    Create all DOM plots for a detector
    """

    len_dataframe = scp_dataframe.loc[:, 'SOURCE_NAME'].value_counts()[0]
    x_bins = int( len_dataframe if len_dataframe < 200 else len_dataframe / 20 )

    date_start = np.sort( md.epoch2num( scp_dataframe.loc[:, 'UNIXTIME'].values / 1000.))[0]
    date_end   = np.sort( md.epoch2num( scp_dataframe.loc[:, 'UNIXTIME'].values / 1000.))[-1]

    for idu, du in enumerate( get_live_DUs( scp_dataframe, clbm ) ):
        plt.cla()
        plt.clf()
        dom_fig, dom_axs = plt.subplots(nrows=19, ncols=2)
        if VERBOSE: print("\nDU:{0}".format(du), end='')
        for (omkey, clb) in sorted( clbm.omkeys.items() ):
            if clb.du != du:
                continue
            try:
                scp_datagroup = get_DOM_datagroup( scp_dataframe, clb )
            except ValueError as e: #no data
                if VERBOSE: print(" Error for dom {0}: {1}".format(clb.floor, e))
                continue

            if( scp_datagroup.size < 1 ):
                print("ERROR: datagroup empty! Skipping")
                continue
            if VERBOSE:
                print( "Plotting datagroup of size {0}".format( scp_datagroup.size ) )

            accent_this = False
            if ACCENT and omkey in ACCENT:
                accent_this = True

            if HIST:

                h_title = '{0} for DOM{1} (DU{2} Floor{3}) from run {4} to run {5}'.format(
                    PARAM_MEANING,
                    clb.dom_id,
                    clb.du,
                    clb.floor,
                    MINRUN,
                    MAXRUN)
                hx_label = ''
                hy_label = '{0} ({1})'.format( PARAM_MEANING, PARAM_UNIT )

                plot_scp_DOM_hist( scp_datagroup,
                                   dom_axs[clb.floor, 0],
                                   clb,
                                   XRANGE = [date_start, date_end],
                                   XBINS = x_bins,
                                   title = h_title,
                                   x_label = hx_label,
                                   y_label = hy_label,
                                   accent = accent_this)

            if SCAT:
                s_title  = '{0} for DOM{1} (DU{2} Floor{3}) from run {4} to run {5}'.format(
                    PARAM_MEANING,
                    clb.dom_id,
                    clb.du,
                    clb.floor,
                    MINRUN,
                    MAXRUN)
                sx_label = ''
                sy_label = '{0} ({1})'.format( PARAM_MEANING, PARAM_UNIT )
                plot_scp_DOM_scat( scp_datagroup,
                                   dom_axs[clb.floor, 1],
                                   clb,
                                   [date_start, date_end], #XRANGE
                                   title = s_title,
                                   x_label = sx_label,
                                   y_label = sy_label,
                                   accent = accent_this)
        
        handle_fig( dom_fig,
                    OUTPATH,
                    save = SAVE_FIG,
                    show = SHOW_FIG,
                    dimensions = (35, 65) )

        plt.close( dom_fig )

def plot_DET_DUs( scp_dataframe,
                  clbm,
                  MINRUN,
                  MAXRUN,
                  PARAM_NAME,
                  PARAM_UNIT,
                  PARAM_MEANING,
                  OUTPATH,
                  DETECTOR,
                  ACCENT = None, #list of omkeys
                  HIST = True,
                  SCAT = True,
                  NORM = False,
                  LOG = False,
                  VERBOSE = False,
                  SAVE_FIG = True,
                  SHOW_FIG = False):
    """
    Create all DU plots for a detector
    """

    len_dataframe = scp_dataframe.loc[:, 'SOURCE_NAME'].value_counts()[0]
    x_bins = int( len_dataframe if len_dataframe < 200 else len_dataframe / 20 )

    date_start = np.sort( md.epoch2num( scp_dataframe.loc[:, 'UNIXTIME'].values / 1000.))[0]
    date_end   = np.sort( md.epoch2num( scp_dataframe.loc[:, 'UNIXTIME'].values / 1000.))[-1]

    live_DUs = get_live_DUs( scp_dataframe, clbm )

    du_fig, du_axs = plt.subplots( len( live_DUs ), 2 )
    du_axs.reshape( len( live_DUs), 2 )
    print( live_DUs)
    for idu, du in enumerate( live_DUs ):
        
        if VERBOSE: print("\nDU: {0} ".format(du), end='')                                                                          
        DU_omkeys = get_DU_omkeys( [du], clbm.omkeys, ignore_base = False)
        
        try:
            scp_datagroup = get_DU_datagroup( scp_dataframe, [du], DETECTOR )
        except ValueError as e: #no data
            if VERBOSE: print(" ERROR: DU {0}: {1}. Skipping this DU.".format(du, e))
            continue

        if scp_datagroup.size < 1 :
            if VERBOSE: print(" ERROR: DU {0} datagroup empty! Skipping this DU.".format(du) )
            continue
        if VERBOSE:
            print( "Plotting datagroup of size {0}".format( scp_datagroup.size ) )

        title = '{0} for {1}-DU{2} from run {3} to run {4}'.format(
            PARAM_MEANING,
            DETECTOR,
            du,
            MINRUN,MAXRUN)
        x_label = '',

        p_m = (["{0}", "log10{0}"][LOG]).format( PARAM_MEANING )
        p_u = ([[" ({0})", " (log_10 {0})"][LOG], ""][NORM]).format(PARAM_UNIT)


        if len( du_axs.shape ) == 1:
            #du_axs reshapes to 
            du_ax = du_axs
        else:
            du_ax = du_axs[idu]

        ACCENT_DOMS = None
        if ACCENT and du == ACCENT[0]:
            ACCENT_DOMS = ACCENT[1]

        if HIST:
            hy_label = 'CLB upi (Floor)'
            w_label= ["<" + p_m + ">_bin", "<" + p_m + ">_bin" + "/<" + p_m + ">_DOM"][NORM] + p_u

            plot_scp_DU_hist( scp_datagroup,
                              clbm,
                              du_fig,
                              du_ax[0],
                              [date_start, date_end],
                              XBINS = len_dataframe,
                              NORM = NORM,
                              LOG  = LOG,
                              title   = title,
                              x_label = x_label,
                              y_label = hy_label,
                              w_label = w_label,
                              ACCENT_DOMS = ACCENT_DOMS,
                              VERBOSE = VERBOSE)

        if SCAT:
            sy_label= [p_m, p_m + "/<" + p_m + ">_DOM"][NORM] + p_u
            plot_scp_DU_scat( scp_datagroup,
                              DU_omkeys,
                              du_ax[1],
                              [date_start, date_end],
                              NORM = NORM,
                              LOG  = LOG,
                              title = title,
                              x_label = x_label,
                              y_label = sy_label,
                              ACCENT_DOMS = ACCENT_DOMS,
                              VERBOSE = VERBOSE)
            
    handle_fig( du_fig,
                OUTPATH,
                save = SAVE_FIG,
                show = SHOW_FIG,
                dimensions = (24, 12 * len( live_DUs )),
                labelsize  = 'x-large',
                titlesize  = 'x-large',
                legendsize = 'large',
                xticksize  = 'large',
                yticksize  = 'large' )
    plt.close( du_fig )


    
def plot_status_DU( x,
                    y,
                    w,
                    run_bins,
                    outplot,
                    title = "",
                    accent_runs = [], #list of (run_n, floor) tuples
                    aspect_ratio = 11.5):

    """
    Plot live status of doms for a single DU
    """

    fig, ax = plt.subplots()
    ax.set_aspect( aspect_ratio )

    h = ax.hist2d( x,
                   y,
                   weights = w,
                   bins = [ run_bins, np.arange( 19 + 1 ) ],
                   cmap = 'Set2',
                   vmin = 0, #This fits with the cmap.
                   vmax = 9) #

    x_scale = run_bins[-1] - run_bins[0]
    x_spacing = 10 if x_scale > 100 else 1
    ax.set_xticks(      np.array( run_bins[0::x_spacing] ) + x_spacing / 2 )
    ax.set_xticks(      np.array( run_bins )               +           0.5, minor = True )
    ax.set_xticklabels( np.array( run_bins[0::x_spacing] ).astype( int ) + int( x_spacing / 2 ),
                         rotation=90,
                         ha="right",
                         va="center",
                         rotation_mode="anchor" )

    ax.set_yticks(      np.arange( 19 ) + 0.5) #0.5, ..., 18.5
    ax.set_yticks(      np.arange( 19 ), minor = True) #0, ..., 18
    ax.set_yticklabels( np.arange( 19 ) ) #0, ..., 18
    for run_tuple in accent_runs:
        ax.set_xticks( list( ax.get_xticks() ) + [run_tuple[0] + x_spacing / 2] )
        ax.get_xticklabels()[ int( ( run_tuple[0] - run_bins[0] + 0.5 ) / x_spacing ) ].set_color('red') 
        ax.get_yticklabels()[ run_tuple[1] ].set_color('red') 

    plt.tick_params(
        axis  = 'both',
        which = 'both',
        bottom= True,  # ticks along the bottom edge are on
        top   = False,    # ticks along the top edge are off
        left  = True,
        right = False,
        direction = 'out')


    plt.xlabel("Run n")
    plt.ylabel("Floor #")
    plt.title( title )
    cbar = plt.colorbar( h[3], ticks = [0.5, 1.6, 2.8, 5.1, 6.2, 8.4] )
    cbar.ax.set_yticklabels(['absent', 'death', 'dead', 'healthy', 'passout', 'bad run'])
    plt.grid( axis='x', linewidth='0.1', color = 'black', which = 'major')
    plt.grid( axis='y', linewidth='0.1', color = 'black', which = 'minor')

    handle_fig( fig,
                outplot,
                save = True,
                dpi = 100,
                dimensions = ( ( x_scale + 55 ) / 50,  (19 + 7) * aspect_ratio / 50 ),
                labelsize  = 'large',
                titlesize  = 'large',
                legendsize = 'large',
                xticksize  = 'small',
                yticksize  = 'medium' )
    plt.close( fig )

def plot_status_DET( dom_infos,
                     runlist,
                     outplot_name,
                     badruns = [],
                     det_id = None,
                     title = '',
                     accent = False,
                     force_recreate = False,
                     verbose = 0):
    """
    Call plot_DU for whole detector
    """

    death_threshold = 10
    passout_threshold = 2

    x_times    = []
    y_floors   = []
    w_statuses = []

    run_bins = runlist + [runlist[-1] + 1]
    plot_data = {}

    for (du, floor), dom in dom_infos.items():

        #Get only physics runs for this detector
        det_dom = copy.deepcopy( dom ).filter_det( det_id )
        if not det_dom:
            continue
        phys_dom = det_dom.filter_runs( runlist )
        if not phys_dom:
            continue

        badruns = get_det_id_runs( badruns, det_id )
        phys_dom.init_status_runs( death_threshold,
                                   passout_threshold,
                                   det_id )

        if du not in plot_data:
            plot_data[ du ] = {'x': [],
                               'y': [],
                               'w': []}
            
        healthy_runs = phys_dom.healthy_runs
        passout_runs = phys_dom.passout_runs
        death_run    = phys_dom.death_run
        dead_runs    = phys_dom.dead_runs
        deaths = [] #run_n, floor

        if verbose >= 2:
            print( "DU{0} badruns {1}".format( du, len( badruns ) ), end = '' )
            print( " - DOM{0}, healthy {1}, dead {2}, passout {3}, death {4}".format( floor,
                                                                                      len(healthy_runs),
                                                                                      len(dead_runs),
                                                                                      len(passout_runs),
                                                                                      bool( death_run ) ))

        #blue = dead
        plot_data[ du ]['x'].extend( np.array( get_sorted_run_n( dead_runs ) ) + 0.5 )
        plot_data[ du ]['y'].extend( ( np.ones( len(dead_runs) ) * floor )       + 0.5 )
        plot_data[ du ]['w'].extend(   np.zeros( len(dead_runs) ) + 3 )

        #green = healthy
        plot_data[ du ]['x'].extend( np.array( get_sorted_run_n( healthy_runs ) ) + 0.5 )
        plot_data[ du ]['y'].extend( ( np.ones( len(healthy_runs) ) * floor )       + 0.5 )
        plot_data[ du ]['w'].extend(  np.zeros( len(healthy_runs) ) + 5 )

        #yellow = passout
        plot_data[ du ]['x'].extend( np.array( get_sorted_run_n( passout_runs ) ) + 0.5 )
        plot_data[ du ]['y'].extend( ( np.ones( len(passout_runs) ) * floor ) + 0.5 )
        plot_data[ du ]['w'].extend( np.zeros( len(passout_runs) ) + 6             )


        #orange = death
        if death_run:
            plot_data[ du ]['x'].append( death_run.n + 0.5 )
            plot_data[ du ]['y'].append( floor + 0.5 )
            plot_data[ du ]['w'].append( 2 )
            
            deaths.append( (death_run.n, floor) )

    for du in plot_data:

        #grey = bad run
        plot_data[ du ]['x'].extend( np.repeat( get_sorted_run_n( badruns ), 19 ) + 0.5 )
        plot_data[ du ]['y'].extend( np.tile( np.arange(19), len(badruns) )       + 0.5 )
        plot_data[ du ]['w'].extend( np.zeros( len(badruns) * 19 ) + 9                  )
        
        outplot = outplot_name.replace( "PLOTINFO", "DU%i_runs%i-%i" %( du,
                                                                        min(plot_data[du]['x']),
                                                                        max(plot_data[du]['x']) ) )

        if not len( plot_data[ du ]['x'] ):
            continue

        plot_exists = False
        for plot_file in glob.glob( outplot + "*" ):
            plot_exists = False
            if force_recreate:
                os.remove( plot_file )
            else:
                plot_exists = True
        if plot_exists:
            print( "File already exists, continuing." )
            continue

        print("Making {0}".format( outplot ) )
        if len( plot_data[ du ]['x'] ):
            plot_status_DU( plot_data[ du ]['x'],
                            plot_data[ du ]['y'],
                            plot_data[ du ]['w'],
                            run_bins,
                            outplot,
                            title = title + " DU{0}".format( du ),
                            accent_runs = [ None, deaths ][accent])
        else:
            print( "No data found! Skipping." )




def get_min_diff( array ):
    sorted_array = np.unique( array )
    if len(sorted_array) < 2: return 0 #the array could contain the same value multiple times!
    min_diff = abs( sorted_array[1] - sorted_array[0] )
    for i, j in enumerate( sorted_array ):
        if i == len(sorted_array) - 1:
            break
        min_diff = sorted_array[i + 1] - j if sorted_array[i + 1] - j < min_diff else min_diff
    return min_diff

def get_run_starts( scp_datagroup,
                    VERBOSE  = False):
    run_starts = []
    for runid in scp_datagroup.loc[:, 'RUN'].unique():
        start = sorted( scp_datagroup.loc[ scp_datagroup.loc[:, 'RUN'] == runid, 'UNIXTIME' ].values )[0]
        run_starts.append( start )
    return run_starts
