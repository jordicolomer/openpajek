import Tkinter
import igraph
import random
 
root = Tkinter.Tk()

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

def erdos():
    global g,layout
    g=igraph.Graph.Erdos_Renyi(100, 0.05)
    layout = g.layout("fr", maxiter=100)
    updateview()

def lattice():
    global g,layout
    g=igraph.Graph.Lattice(dim=[3,3,3])
    layout = g.layout("fr", maxiter=100)
    updateview()

def barabasi():
    global g,layout
    g=igraph.Graph.Barabasi(27, m=81)
    layout = g.layout("fr", maxiter=100)
    updateview()

def shortcut():
    global g
    e=random.randint(0, g.ecount()-1)
    g.delete_edges(e)
    i = random.randint(0, g.vcount()-1)
    j = random.randint(0, g.vcount()-1)
    while i==j or g.are_connected(i, j):
        i = random.randint(0, g.vcount()-1)
        j = random.randint(0, g.vcount()-1)
    g.add_edges((i, j))
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
filemenu.add_command(label="Erdos-Renyi", command=erdos)
filemenu.add_command(label="Lattice", command=lattice)
filemenu.add_command(label="Barabasi", command=barabasi)
#filemenu.add_command(label="SW")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Random", menu=filemenu)

# create more pulldown menus
editmenu = Tkinter.Menu(menubar, tearoff=0)
editmenu.add_command(label="Shortcut (random link)", command=shortcut)
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
menubar.add_cascade(label="Color", menu=layoutmenu)

# display the menu
root.config(menu=menubar)


def drawcircle(canv,x,y,rad):
    canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='blue')
 
canvas = Tkinter.Canvas(width=800, height=600, bg='white')  
canvas.pack(expand=Tkinter.YES, fill=Tkinter.BOTH) 
#canvas.create_text(50,10, text="tk test")
 
def key(event):
    if event.char == event.keysym:
        msg = 'Normal Key %r' % event.char
        if event.char == 'n':
            shortcut()
    elif len(event.char) == 1:
        msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
    else:
        msg = 'Special Key %r' % event.keysym
    #print msg
 
root.bind_all('<Key>', key)

root.mainloop()
