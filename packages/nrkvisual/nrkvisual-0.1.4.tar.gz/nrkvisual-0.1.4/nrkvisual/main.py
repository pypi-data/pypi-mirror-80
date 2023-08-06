from tkinter import *

from pandas import read_excel

from nrkvisual.tkhelper import EntryBar, Browse, OkButton, Popup
from nrkvisual.visual import TrianglePlot


def main():
    root = Tk()
    lng = EntryBar(root, picks=["Left", "Right", "Top", "Data", "Temp (opt)"])
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
            a = TrianglePlot(
                data=frame,
                data_column=list(filter(lambda x: x[0] == "Data", col))[0][1],
            )
            r = a.plot()
            for error in r:
                Popup(parent=root, text=error)

    root.destroy()


def handle_data(file, columns):
    n = 0
    bad = True
    error = None
    data = None
    frame_list = []
    cols = list(columns.state())
    t = columns.get("Top")
    working_cols = {
        x[1].lower() for x in cols if x[1] != ""
    }  # This needs to be evaluated here
    while bad:
        try:
            data = read_excel(
                file, sheet_name=n, usecols=lambda x: x.lower().strip() in working_cols
            )
        except IndexError as e:
            error = e
            bad = False
        if working_cols.issubset(data.columns.map(lambda x: x.lower())):
            bad = False
        n += 1
    if temp := list(columns.get("Temp (opt)")):
        temp = temp[0]
        data = data.groupby(temp)
        for n, d in data:
            frame_list.append(d)
    else:
        frame_list.append(data)

    return frame_list, cols


if __name__ == "__main__":
    main()
