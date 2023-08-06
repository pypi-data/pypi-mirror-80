from tkinter import *
from tkinter import filedialog
from nrkvisual.visual.plotting import TrianglePlot
from pandas import read_excel
import io


class EntryBar(Frame):
    def __init__(self, parent=None, picks=None, side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        if picks is None:
            picks = []
        self.vars = []
        for pick in picks:
            row = Frame(parent)
            label = Label(row, width=10, text=pick, anchor=anchor)
            entry = Entry(row)
            row.pack(side=TOP, fill=X, padx=1, pady=1)
            label.pack(side=side)
            entry.pack(side=RIGHT, expand=YES, fill=X)
            self.vars.append((pick, entry))

    def state(self):
        return map(lambda var: (var[0], var[1].get()), self.vars)

    def get(self, string):
        return filter(None, map(lambda var: var[1].get() if string == var[0] else None, self.vars))


class Browse(Frame):
    def __init__(self, parent=None, label=None, anchor=S, side=LEFT):
        Frame.__init__(self, parent)
        self.file = ""
        if not label:
            self.label = Label(parent, font=("Helvetica", 9), fg="red")
        self.btn = Button(
            parent, text="Browse", command=lambda: self.browsefunc()
        ).pack(anchor=anchor, side=side)

    def browsefunc(self):
        self.file = filedialog.askopenfiles(mode='rb')
        self.label.config(text=self.file[0].name.split('/')[-1])
        self.label.pack()

    def get(self):
        return self.file


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


def main():
    root = Tk()
    lng = EntryBar(root, picks=['Left', 'Right', 'Top', 'Data', 'Temp (opt)'])
    br = Browse(root)
    br.pack()
    ok = OkButton(root, function=c, file=br, root=root, columns=lng)
    ok.pack()
    root.mainloop()


def c(file, root, columns):
    file = file.get()
    for f in file:
        data, col = handle_data(f, columns)
        for frame in data:
            a = TrianglePlot(data=frame, data_column=list(filter(lambda x: x[0] == 'Data', col))[0][1])
            a.plot()
    root.destroy()


### Useful for later given csv encoding but for now we'll stick to binary file reads
# def encoding(iofile: io.TextIOWrapper, n):
#     codes = ['latin1', 'utf8', 'ascii']
#     try:
#         data = read_excel(iofile, sheet_name=n)
#         return data
#     except UnicodeDecodeError:
#         pass
#     for code in codes:
#         try:
#             iofile.reconfigure(encoding=code)
#             data = read_excel(iofile, sheet_name=n)
#             return data
#         except UnicodeDecodeError:
#             pass


def handle_data(file, columns):
    n = 0
    bad = True
    error = None
    data = None
    frame_list = []
    cols = list(columns.state())
    t = columns.get('Top')
    working_cols = {x[1].lower() for x in cols if x[1] != ''}  # This needs to be evaluated here
    while bad:
        try:
            data = read_excel(file, sheet_name=n, usecols=lambda x: x.lower().strip() in working_cols)
        except IndexError as e:
            error = e
            bad = False
        if working_cols.issubset(data.columns.map(lambda x: x.lower())):
            bad = False
        n += 1
    if temp := list(columns.get('Temp (opt)')):
        temp = temp[0]
        data = data.groupby(temp)
        for n, d in data:
            frame_list.append(d)
    else:
        frame_list.append(data)

    return frame_list, cols


if __name__ == "__main__":
    main()
