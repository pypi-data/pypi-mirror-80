**Welcome to the DOMAuto repository, with Auto standing for Autopsy and Automatic!**

Thanks to Tamas Gal, Rodrigo Garcia, and Daan van Eijk for their codes and help that enabled this project.

The programs in this repository are intended to be used for performing post-mortem analyses of DOMs in the detector.

*domauto -h* for immediate help on how to use DOMAuto.

* *crawl* scan JRA files to find runs in which DOMs die or exhibit other interesting behavior, and to find runs which are present in the database but which have missing JRA files.

* *plot-status* plot the statuses of each DOM over the lifetime of all detectors.

* *plot-scp* plot the slow control parameters for each DOM and each DU for chosen runs.

* *auto* find interesting runs, plot all DOM statuses, plot all slow control parameters for interesting runs, and publish all plots on a website.

* In *./web*, compile all created plots into a website and send for publication on a public server.

* *./DOMAuto_notebook.ipynb* is a jupyter notebook which provides basic interaction with the database, and possibility of producing slow control parameter plots for a chosen detector, run and du.