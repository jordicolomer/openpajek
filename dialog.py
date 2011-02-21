import Tkinter

class MyDialog:
    def __init__(self, parent, labels,defaults):
        self.top = top = Tkinter.Toplevel(parent)

        self.e = []
        for i in range(0,len(labels)):
            label = labels[i]
            default = defaults[i]

            Tkinter.Label(top, text=label).grid(row=i, column=0)

            #v = StringVar()
            a = Tkinter.StringVar()
            a.set(default)
            e = Tkinter.Entry(top, textvariable=a)
            #print default
            #e.set(default)
            e.grid(row=i, column=1)
            self.e.append(a)

        b = Tkinter.Button(top, text="OK", command=self.ok)
        b.grid(row=i+1, column=1)

    def ok(self):
        self.top.destroy()

def show(root,labels,defaults):
    d = MyDialog(root,labels,defaults)
    root.wait_window(d.top)
    ret = []
    for a in d.e:
        ret.append(a.get())
    return ret

def show1(root,label,default):
    return show(root,[label],[default])[0]
