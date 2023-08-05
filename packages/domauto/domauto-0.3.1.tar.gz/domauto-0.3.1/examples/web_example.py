import os, ROOT, aa

# The following puts root in batch mode; you will not see graphics
# output on your screen.
ROOT.gROOT.SetBatch( True )

# Make directory to put the files
dr = "web_scp"
os.system('mkdir ' + dr)

# We will use the WebFile object;
# no need, compile, you can just include the .hh file...
aa.include( os.environ['AADIR']+"/ana/histogrammer/WebFile.hh")
W = ROOT.WebFile( dr )

# make a canvas with some plot
c = ROOT.TCanvas('c','title', 600,600 )
h = ROOT.TH1D("h","hist",100,0,1)
for i in range(101) : h.SetBinContent( i, ( i - 50 )**2 )
h.SetFillColor(5)
h.Draw()


# You can write bare html
W.write("<h1> This is the Title <h1> <br> ")

# You can write a root canvas like so:
W.write( c )
h.SetFillColor(4)
h.Draw()
c.SetName("c2") # this is important since the name of the .png file is based the canvas Name
W.write(c)

# If you have a png / gif you can add it like this:
h.SetFillColor(2)
h.Draw()
c.SaveAs(dr + "/plot.png")     # put it in the webdir
W.write_img_tag( 'plot.png','')

del W # destructor closes the file

# you can now copy the webdir to a webserver -- for example
cmd = "scp -r " + dr + +" jseneca@login.nikhef.nl:~/public_html"
os.system(cmd)
# it will be viewable here : https://www.nikhef.nl/~t61/webdir/

