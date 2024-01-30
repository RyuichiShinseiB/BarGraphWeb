import warnings
from typing import TypeGuard

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.figure import Figure
from type import GraphConf


def _is_not_none_or_nan(
    x: tuple[float, float] | None
) -> TypeGuard[tuple[float, float]]:
    return x is not None and not any(np.isnan(x))


def calc_hist(
    x: npt.NDArray,
    xlim: tuple[float, float] | None = None,
    step: float = 1.0
) -> tuple[npt.NDArray, npt.NDArray, list[str]]:
    if xlim is not None and len(xlim) > 2:
        warnings.warn(
            "A tuple with more than two elements has been entered"
            "but only the first two will be used.",
            UserWarning
        )
    x_min = xlim[0] if _is_not_none_or_nan(xlim) else x.min()
    x_max = xlim[1] if _is_not_none_or_nan(xlim) else x.max()
    bins = np.arange(np.floor(x_min), np.ceil(x_max) + step, step=step)
    xticks = np.convolve(bins, [1/2, 1/2], mode="valid")
    xlabels: list[str] = [
        f"[{bins[i]}, {bins[i + 1]})" for i in range(len(xticks))
        # f"[{i * step}, {(i + 1) * step})" for i in range(len(xticks))
    ]
    hist, _ = np.histogram(x, bins, range=(x_min, x_max))

    return hist, xticks, xlabels


def plot_hist(x: npt.NDArray, conf: GraphConf) -> Figure:
    hist, xticks, xlabels = calc_hist(
        x * conf.unit_cvt_const,
        (conf.x_min, conf.x_max),
        conf.histogram_step
    )

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.bar(xticks, hist, conf.bin_width, label=conf.legend, align="center")
    ax.set_xlabel(conf.x_label)
    ax.set_ylabel(conf.y_label)

    if _is_not_none_or_nan((conf.x_min, conf.x_max)):
        ax.set_xlim(left=conf.x_min, right=conf.x_max)

    if _is_not_none_or_nan((conf.y_min, conf.y_max)):
        ax.set_ylim(bottom=conf.y_min, top=conf.y_max)

    if conf.is_showing_legend:
        ax.legend()

    if conf.is_set_xticklabels:
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels, rotation=conf.label_angle)

    return fig


if __name__ == "__main__":
    x = np.random.uniform(0, 1, 100)
    fig = plot_hist(
        x,
        GraphConf(),
    )
    plt.show()
    plt.show()
