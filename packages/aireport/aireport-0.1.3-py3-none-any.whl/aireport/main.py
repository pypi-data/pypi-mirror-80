from tkinter import *
from tkinter import filedialog
from aireport.tools import lazy_lims_new, reshape_spectral_csv


class CheckBar(Frame):
    def __init__(self, parent=None, picks=None, side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        if picks is None:
            picks = {}
        self.vars = []
        for pick in picks.keys():
            var = IntVar()
            chk = Checkbutton(master=self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append((var, picks[pick]))

    def state(self):
        return filter(
            None, map(lambda var: var[1] if var[0].get() else None, self.vars)
        )


class Browse(Frame):
    def __init__(self, parent=None, label=None, anchor=S, side=LEFT):
        Frame.__init__(self, parent)
        self.directory = ""
        if not label:
            self.label = Label(parent, font=("Helvetica", 9), fg="red")
        self.btn = Button(
            parent, text="Browse", command=lambda: self.browsefunc()
        ).pack(anchor=anchor, side=side)

    def browsefunc(self):
        self.directory = filedialog.askdirectory()
        self.label.config(text=self.directory.split("/")[-1])
        self.label.pack()

    def get(self):
        return self.directory


class OkButton(Frame):
    def __init__(
        self,
        parent=None,
        label=None,
        anchor=S,
        side=RIGHT,
        function=None,
        *args,
        **kwargs
    ):
        Frame.__init__(self, parent)
        self.ok = Button(
            parent, text="Ok", command=lambda: function(*args, **kwargs)
        ).pack(anchor=anchor, side=side)
        self.label = label


def tools_ui():
    root = Tk()
    functions_name = {
        "Lims and Sample Name": lazy_lims_new,
        "EDS Convert": reshape_spectral_csv,
    }
    lng = CheckBar(root, functions_name)
    lng.pack(side=TOP, fill=X)
    br = Browse(root)
    br.pack()
    ok = OkButton(root, function=c, lng=lng, directory=br, root=root)
    ok.pack()
    root.mainloop()


def c(lng, directory, root):
    directory = directory.get()
    for function in list(lng.state()):
        function(directory)
    root.destroy()


if __name__ == "__main__":
    tools_ui()
