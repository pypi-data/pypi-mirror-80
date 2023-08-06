import operator
from functools import reduce, partial

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
from pandas import DataFrame, Series


class TrianglePlot:
    ERROR_CODES = {
        "NA": lambda x: f"Found empty data here {x}",
        "EMPTY": "We found no data",
        "SHAPE": lambda x: f"Expected at least 4 columns (3 Axes 1 Data + Optional Temperature) we found only the following columns in the data provided {x}",
        "DATA": lambda x: f"We couldn't find your data column in the provided data you provided {x or ' < NONE >'} as the data column"
    }
    errors = []
    critical = False

    def __init__(self, data: DataFrame, data_column: str, tick=0.1, margin=0.05, n=5):
        self.data = data
        self.data_column = data_column

        self.a = Series
        self.b = Series
        self.c = Series
        self.v = Series
        self.x = Series
        self.y = Series
        self.axes = DataFrame
        self.tick = tick
        self.margin = margin
        self.n = n
        self.T = None

        self.fig, self.ax = plt.subplots(1)
        self.ax.set_axis_off()

    @property
    def data_column(self):
        return self._data_column

    @property
    def data(self):
        return self._data

    @data_column.setter
    def data_column(self, value: str):
        value = value.strip().lower()
        if value not in self.data.rename(columns=lambda x: x.strip().lower()):
            self.errors.clear()
            self.errors.append(self.ERROR_CODES['DATA'](value))
            self.critical = True
        self._data_column = value

    @data.setter
    def data(self, d: DataFrame):
        if d.empty:
            self.errors.clear()
            self.errors.append(self.ERROR_CODES["EMPTY"])
            self.critical = True
        if d.isnull().values.any():
            self.errors.append(
                self.ERROR_CODES["NA"](d[d.isnull().any(axis=1)].index.values)
            )
            d = d.dropna()
        if d.shape[1] < 4:
            self.errors.clear()
            self.errors.append(self.ERROR_CODES["SHAPE"](d.columns.values))

            self.critical = True
        self._data = d

    @staticmethod
    def chain(function, series):
        mFunction = partial(function)
        return reduce(mFunction, series)

    def plot(self):
        if not self.critical:
            self.xy()
            self.cords()
            self.triangle()
            self.set_up()
            plt.show()
        else:
            return self.errors

    def xy(self):
        self.v = self.data.rename(columns=lambda x: x.lower())[self.data_column.lower()]
        self.axes = self.data.rename(columns=lambda x: x.lower()).drop(
            columns=[self.data_column.lower()]
        )
        self.axes = self.normalize(self.axes)

    def cords(self):

        self.a = self.axes[self.axes.columns[0]]
        self.b = self.axes[self.axes.columns[1]]
        self.c = self.axes[self.axes.columns[2]]

    @staticmethod
    def normalize(df):
        if (df.sum(axis=1) > 1.5).any():  # Accounting for input errors
            df = df.div(100)
        return df

    def triangle(self):
        under = self.chain(Series.add, [self.a, self.b, self.c])
        self.x = 0.5 * (self.b.mul(2).add(self.c)) / under
        self.y = self.c.mul(0.574 * np.sqrt(3)) / under
        self.T = tri.Triangulation(self.x, self.y)

    def set_up(self):
        left = np.r_[0, 0]
        right = np.r_[1, 0]
        top = np.r_[0.5, np.sqrt(3) * 0.576]
        tick = lambda x: (0.8264 * self.tick * x) / self.n
        self.plot_ticks(right, left, tick(right - top), offset=(0, -0.04))
        self.plot_ticks(left, top, tick(left - right), offset=(-0.06, -0.0))
        self.plot_ticks(top, right, tick(top - left))
        tn = self.c.name.capitalize()
        ln = self.a.name.capitalize()
        rn = self.b.name.capitalize()

        self.annotate(tn, [0.5, 1], [0.5, 1.09])
        self.annotate(ln, [0, 0], [-0.04, 0.02])
        self.annotate(rn, [1, 0], [1.04, 0.02])
        self.annotate(f"{ln}-{rn}", [0.5, 0], [0.5, -0.09])
        self.annotate(f"{rn}-{tn}", [0.72, 0.5], [0.9, 0.55])
        self.annotate(f"{ln}-{tn}", [0.2, 0.5], [0.1, 0.55])
        plt.tricontourf(self.x, self.y, self.T.triangles, self.v)
        corners = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) * 0.576]])
        triangle = tri.Triangulation(corners[:, 0], corners[:, 1])
        refiner = tri.UniformTriRefiner(triangle)
        trimesh = refiner.refine_triangulation(subdiv=4)
        plt.triplot(trimesh, "k--")
        plt.colorbar(ax=self.ax, shrink=0.6, aspect=10, format="%.3f")
        self.fig.tight_layout()

    def annotate(self, text, cord, textcord):
        self.ax.annotate(
            text,
            xy=cord,
            xytext=textcord,
            horizontalalignment="center",
            verticalalignment="top",
        )

    def plot_ticks(self, start, stop, tick, offset=(0.0, 0.0)):
        r = np.linspace(0.1, 0.9, self.n + 1)
        x = start[0] * (1 - r) + stop[0] * r
        x = np.vstack((x, x + tick[0]))
        y = start[1] * (1 - r) + stop[1] * r
        y = np.vstack((y, y + tick[1]))
        plt.plot(x, y, "k", lw=0.5)
        # add tick labels
        for xx, yy, rr in zip(x[1], y[1], r):
            plt.text(xx + offset[0], yy + offset[1], f"{round(rr, 1)}")
