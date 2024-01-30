from dataclasses import dataclass


@dataclass
class GraphConf:
    has_header: bool = False
    unit_cvt_const: float = 1.0

    x_min: float = 0.0
    x_max: float = 100.0
    histogram_step: float = 1.0
    bin_width: float = 0.8
    x_label: str = "x"

    y_min: float = 0.0
    y_max: float = 20.0
    y_label: str = "y"

    is_showing_legend: bool = True
    legend: str = ""
    is_set_xticklabels: bool = False
    label_angle: float = 0.0
