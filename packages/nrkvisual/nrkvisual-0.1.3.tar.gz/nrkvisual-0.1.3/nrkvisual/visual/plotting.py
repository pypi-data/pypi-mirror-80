from functools import reduce, partial

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
from pandas import DataFrame, Series


class TrianglePlot:
    def __init__(self, data: DataFrame, data_column: str, tick=0.1, margin=0.05, n=5):

        self.data = data
        self.a = Series
        self.b = Series
        self.c = Series
        self.v = Series
        self.x = Series
        self.y = Series
        self.tick = tick
        self.margin = margin
        self.n = n
        self.T = None
        self.v = data.rename(columns=lambda x: x.lower())[data_column.lower()]
        self.axes = data.rename(columns=lambda x: x.lower()).drop(columns=[data_column.lower()])
        self.fig, self.ax = plt.subplots(1)
        self.ax.set_axis_off()

    def plot(self):
        self.cords()
        self.triangle()
        self.set_up()
        plt.show()

    @staticmethod
    def chain(function, series):
        mFunction = partial(function)
        return reduce(mFunction, series)

    def cords(self):
        self.a = self.axes[self.axes.columns[0]]
        self.b = self.axes[self.axes.columns[1]]
        self.c = self.axes[self.axes.columns[2]]

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
        self.annotate(f'{ln}-{rn}', [0.5, 0], [0.5, -0.09])
        self.annotate(f'{rn}-{tn}', [0.72, 0.5], [0.9, 0.55])
        self.annotate(f'{ln}-{tn}', [0.2, 0.5], [0.1, 0.55])
        plt.tricontourf(self.x, self.y, self.T.triangles, self.v)
        corners = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) * 0.576]])
        triangle = tri.Triangulation(corners[:, 0], corners[:, 1])
        refiner = tri.UniformTriRefiner(triangle)
        trimesh = refiner.refine_triangulation(subdiv=4)
        plt.triplot(trimesh, "k--")
        # cax = plt.axes([0.1, 0.25, 0.055, 0.6])
        plt.colorbar(ax=self.ax, shrink=0.6, aspect=10, format="%.3f")
        self.fig.tight_layout()

    def annotate(self, text, cord, textcord):
        self.ax.annotate(text, xy=cord, xytext=textcord, horizontalalignment='center', verticalalignment='top')

    def plot_ticks(self, start, stop, tick, offset=(0.0, 0.0)):
        r = np.linspace(0.1, 0.9, self.n + 1)
        x = start[0] * (1 - r) + stop[0] * r
        x = np.vstack((x, x + tick[0]))
        y = start[1] * (1 - r) + stop[1] * r
        y = np.vstack((y, y + tick[1]))
        plt.plot(x, y, "k", lw=1)
        # add tick labels
        for xx, yy, rr in zip(x[1], y[1], r):
            plt.text(xx + offset[0], yy + offset[1], f"{round(rr, 1)}")
