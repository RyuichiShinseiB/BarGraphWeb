import json
import re
from dataclasses import asdict, dataclass
from typing import TypeAlias

from streamlit.runtime.uploaded_file_manager import UploadedFile

JsonStr: TypeAlias = str


@dataclass
class GraphConf:
    has_header: bool = False
    unit_cvt_const: float = 1.0

    x_min: float | None = None
    x_max: float | None = None
    histogram_step: float = 1.0
    bin_width: float = 0.8
    x_label: str = "x"

    y_min: float | None = None
    y_max: float | None = None
    y_label: str = "y"

    is_showing_legend: bool = True
    legend: str = ""
    is_set_xticklabels: bool = False
    label_angle: float = 0.0

    @classmethod
    def from_json(cls, json_path: str | bytes | UploadedFile) -> "GraphConf":
        if isinstance(json_path, UploadedFile):
            _config = json.load(json_path)
        else:
            with open(json_path, "r") as f:
                _config = json.load(f)
        return cls(**_config)

    def to_json(self,) -> JsonStr:
        _json_text = json.dumps(asdict(self))
        return re.sub(r" Nan(,|})", r" null(,|})", _json_text)


if __name__ == "__main__":
    conf2 = GraphConf.from_json("./src/sample_data/default_graph_config.json")
    print(conf2)
    print(conf2.to_json())
