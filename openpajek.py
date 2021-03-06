import Tkinter
import igraph
import random

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.font_manager
import matplotlib.backends.backend_tkagg
import matplotlib.figure
import matplotlib.pyplot

import dialog
 
root = Tkinter.Tk()
ccs = []
apls = []
steps = 0
mlog=0

def transcoords(x,y,box):
    x = (x-box[0])/(box[2]-box[0])
    y = (y-box[1])/(box[3]-box[1])
    margin=.05
    return x*800*(1-margin*2)+800*margin,y*600*(1-margin*2)+600*margin

def updateview():
    global canvas
    global g,layout
    canvas.delete(Tkinter.ALL)
    box=layout.bounding_box()
    for c in layout:
        x,y=transcoords(c[0],c[1],box)
        drawcircle(canvas,x,y,5)
    for e in g.get_edgelist():
        x1,y1=transcoords(layout[e[0]][0],layout[e[0]][1],box)
        x2,y2=transcoords(layout[e[1]][0],layout[e[1]][1],box)
        canvas.create_line(x1,y1,x2,y2)

def getDegreeDist(g):
    maxd = 0
    for i in range(0,g.vcount()):
        maxd = max(g.degree(i),maxd)
    dist=[0]*(maxd+1)
    for i in range(0,g.vcount()):
        dist[g.degree(i)] = dist[g.degree(i)]+1
    return dist

def p_log():
    global mlog
    mlog=1
    replot()

def p_linear():
    global mlog
    mlog=0
    replot()

def replot():
    global canvas2,mlog
    f = matplotlib.pyplot.figure(1)
    f.clf()
    aplx = matplotlib.pyplot.subplot(3,1,1)
    matplotlib.pyplot.ylabel('apl')
    matplotlib.pyplot.xlabel('step')
    if len(apls)>1 and mlog == 1:
        aplx.set_xscale('log')
    aplx.plot(range(0,steps),apls)

    ccx = matplotlib.pyplot.subplot(3,1,2)
    matplotlib.pyplot.ylabel('cc')
    matplotlib.pyplot.xlabel('step')
    if len(apls)>1 and mlog == 1:
        ccx.set_xscale('log')
    ccx.plot(range(0,steps),ccs)

    dist = getDegreeDist(g)
    deg = matplotlib.pyplot.subplot(3,1,3)
    matplotlib.pyplot.ylabel('count')
    matplotlib.pyplot.xlabel('degree')
    if mlog == 1:
        deg.set_xscale('log')
        deg.set_yscale('log')
    deg.plot(range(0,len(dist)),dist)

    canvas2.show()

def erdos():
    global g,layout

    clearPlot()
    pars=dialog.show(root,['nodes','density'],['100','0.05'])

    g=igraph.Graph.Erdos_Renyi(int(pars[0]), float(pars[1]))
    layout = g.layout("fr", maxiter=100)

    updateview()
    measure()
    replot()

def lattice():
    global g,layout

    clearPlot()

    dim=dialog.show(root,['dimensions'],['5,5,5'])[0]
    dimi=[]
    for d in dim.split(','):
        dimi.append(int(d))

    g=igraph.Graph.Lattice(dim=dimi)
    layout = g.layout("fr", maxiter=100)

    updateview()
    measure()
    replot()

def barabasi():
    global g,layout

    clearPlot()

    pars=dialog.show(root,['number of vertices','number of outgoing edges generated for each vertex'],['100','5'])

    g=igraph.Graph.Barabasi(int(pars[0]), m=int(pars[1]))
    layout = g.layout("fr", maxiter=100)
    updateview()

def watts():
    global g,layout
    clearPlot()

    n=int(dialog.show(root,['number of vertices'],['100'])[0])

    g = igraph.Graph(n=n, directed=True)
    for i in range(0, n):
        g.add_edges((i, (i+1)%n))
        g.add_edges((i, (i+2)%n))

    layout = g.layout("circular", maxiter=100)
    updateview()

def clearPlot():
    global ccs,apls,steps
    ccs=[]
    apls=[]
    steps=0

def measure():
    global ccs,apls,steps
    ccs.append(g.transitivity_undirected())
    apls.append(g.average_path_length())
    steps=steps+1


def shortcut():
    global g,ccs,apls,steps
    e=random.randint(0, g.ecount()-1)
    g.delete_edges(e)
    i = random.randint(0, g.vcount()-1)
    j = random.randint(0, g.vcount()-1)
    while i==j or g.are_connected(i, j):
        i = random.randint(0, g.vcount()-1)
        j = random.randint(0, g.vcount()-1)
    g.add_edges((i, j))
    g.add_edges((j, i))

    measure()
    replot()
    updateview()

def neighbor():
    global g,ccs,apls,steps
    while True:
        e=g.get_edgelist()[random.randint(0, g.ecount()-1)]
        s=[]
        for i in g.neighbors(e[0]):
            for j in g.neighbors(i):
                if j != e[0] and j not in g.neighbors(e[0]):
                    s.append(j)
        if len(s) > 0:
            break
    g.delete_edges(e)
    r = s[random.randint(0, len(s))]
    g.add_edges((e[0], r))
    g.add_edges((r,e[0]))

    measure()
    replot()
    updateview()

def preferential():
    global g,ccs,apls,steps
    e1=g.get_edgelist()[random.randint(0, g.ecount()-1)]
    g.delete_edges(e1)

    while True:
        e2=g.get_edgelist()[random.randint(0, g.ecount()-1)]
        n=random.randint(0, g.vcount()-1)
        if e2[0] != n and not g.are_connected(e2[0], n):
            break
    g.add_edges((e2[0], n))
    g.add_edges((n,e2[0]))

    measure()
    replot()
    updateview()

def newlayout(s):
    global g,layout
    layout = g.layout(s)
    updateview()

def l_circular():
    newlayout("circular")

def l_drl():
    newlayout("drl")

def l_fruchterman_reingold():
    newlayout("fruchterman_reingold")

def l_graphopt():
    newlayout("graphopt")

def l_grid_fruchterman_reingold():
    newlayout("grid_fruchterman_reingold")

def l_kamada_kawai():
    newlayout("kamada_kawai")

def l_large_graph():
    newlayout("large_graph")

def l_random():
    newlayout("random")

def l_reingold_tilford():
    newlayout("reingold_tilford")

def l_reingold_tilford_circular():
    newlayout("reingold_tilford_circular")

def l_star():
    newlayout("star")

# create a toplevel menu
menubar = Tkinter.Menu(root)

filemenu = Tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit (q)", command=root.quit)
menubar.add_cascade(label="file", menu=filemenu)

filemenu = Tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Erdos-Renyi", command=erdos)
filemenu.add_command(label="Lattice", command=lattice)
filemenu.add_command(label="Barabasi", command=barabasi)
filemenu.add_command(label="Watts", command=watts)
menubar.add_cascade(label="Generate Network", menu=filemenu)

# create more pulldown menus
editmenu = Tkinter.Menu(menubar, tearoff=0)
editmenu.add_command(label="Random (r)", command=shortcut)
editmenu.add_command(label="Neighbor (n)", command=neighbor)
editmenu.add_command(label="Preferential attachment (p)", command=preferential)
menubar.add_cascade(label="Simulate", menu=editmenu)

layoutmenu = Tkinter.Menu(menubar, tearoff=0)
layoutmenu.add_command(label="circular", command=l_circular)
layoutmenu.add_command(label="drl", command=l_drl)
layoutmenu.add_command(label="fruchterman_reingold", command=l_fruchterman_reingold)
layoutmenu.add_command(label="graphopt", command=l_graphopt)
layoutmenu.add_command(label="grid_fruchterman_reingold", command=l_grid_fruchterman_reingold)
layoutmenu.add_command(label="kamada_kawai", command=l_kamada_kawai)
layoutmenu.add_command(label="large_graph", command=l_large_graph)
layoutmenu.add_command(label="random", command=l_random)
layoutmenu.add_command(label="reingold_tilford", command=l_reingold_tilford)
layoutmenu.add_command(label="reingold_tilford_circular", command=l_reingold_tilford_circular)
#layoutmenu.add_command(label="star", command=l_star)
menubar.add_cascade(label="Layout", menu=layoutmenu)

layoutmenu = Tkinter.Menu(menubar, tearoff=0)
layoutmenu.add_command(label="by degree", command=l_drl)
layoutmenu.add_command(label="by eigenvector", command=l_drl)
layoutmenu.add_command(label="by betweenness", command=l_circular)
layoutmenu.add_command(label="by closeness", command=l_circular)
layoutmenu.add_command(label="by clustering coefficient", command=l_circular)
#menubar.add_cascade(label="Color", menu=layoutmenu)

layoutmenu = Tkinter.Menu(menubar, tearoff=0)
layoutmenu.add_command(label="log", command=p_log)
layoutmenu.add_command(label="linear", command=p_linear)
menubar.add_cascade(label="plot", menu=layoutmenu)

# display the menu
root.config(menu=menubar)


def drawcircle(canv,x,y,rad):
    canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='blue')
 
canvas = Tkinter.Canvas(width=800, height=600, bg='white')
#canvas.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)
canvas.grid(row=0, column=0, rowspan=1)
#canvas.create_text(50,10, text="tk test")


f = matplotlib.pyplot.figure(1)




canvas2 = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(f, master=root)
canvas2.get_tk_widget().grid(row=0, column=1)

#lattice()
#measure()
#replot()

def key(event):
    if event.char == event.keysym:
        msg = 'Normal Key %r' % event.char
        if event.char == 'r':
            shortcut()
        if event.char == 'n':
            neighbor()
        if event.char == 'p':
            preferential()
        if event.char == 'q':
            exit(0)
    elif len(event.char) == 1:
        msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
    else:
        msg = 'Special Key %r' % event.keysym
    #print msg
 
root.bind_all('<Key>', key)
root.mainloop()
