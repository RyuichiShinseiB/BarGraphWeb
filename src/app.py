from io import BytesIO

import numpy as np
import numpy.typing as npt
import streamlit as st
from plot import plot_hist
from simpleeval import simple_eval
from widgets import create_textbox

st.title("Create Bar Graph!")


# 受け取った文字列から四則演算をする関数
def calc_expression(expression: str) -> float:
    try:
        result = simple_eval(expression)
        return float(result)
    except Exception as e:
        print(f"Error: {e}. Returned 1.0.")
        return 1.0


st.markdown("# Gpaph configuration")
with st.form(key="config_form"):
    # ファイルのアップロード
    st.markdown("## Upload your csv file")
    csv_path = st.file_uploader("csv file", type="csv")
    # ヘッダー（カラム名）を含むか
    has_header = st.checkbox(
        "Does the csv file include headers and columns?",
        key="has_header"
    )
    if csv_path is None:
        data: npt.NDArray[np.float64] | None = None
        filename: str | None = None
    else:
        # ヘッダー（カラム名）があれば一行目は削除する
        data = np.loadtxt(
            csv_path,
            delimiter=",",
            skiprows=1 if has_header else 0
        )
        filename = f"{csv_path.name.split('.')[0]}"

    st.markdown("## Unit conversion")
    unit_cvt_const = create_textbox(
        "The csv data is multiplied by this value",
        value_type=float,
        default_value="1",
        key="unit_cvt_const",
        cvt_func=calc_expression,
    )

    # configuration of x range
    st.markdown("## Set x-axis Configuration")
    cols_x_minmax = st.columns(2)
    with cols_x_minmax[0]:
        x_min = create_textbox(
            "x-min",
            float,
            default_value="nan",
            key="x_min"
        )

    with cols_x_minmax[1]:
        x_max = create_textbox(
            "x-max",
            float,
            default_value="nan",
            key="x_max",
        )
    histogram_step = create_textbox(
        "step",
        value_type=float,
        default_value="1",
        key="step",
    )
    bin_width = create_textbox(
        "width of bins",
        value_type=float,
        default_value="0.8",
        key="bin_width"
    )
    x_label = create_textbox(
        "label name for x-axis",
        value_type=str,
        default_value="x",
        key="x_label",
    )

    # configuration of y range
    st.markdown("## Set y-axis Configuration")
    cols_y_minmax = st.columns(2)
    with cols_y_minmax[0]:
        y_min = create_textbox(
            "y-min",
            value_type=float,
            default_value="nan",
            key="y_min"
        )
    with cols_y_minmax[1]:
        y_max = create_textbox(
            "y-max",
            value_type=float,
            default_value="nan",
            key="y_max"
        )
    y_label = create_textbox(
        "label name for y-axis",
        value_type=str,
        default_value="y",
        key="y_label",
    )

    st.markdown("## Optional configs")
    cols_legend = st.columns(2)
    with cols_legend[0]:
        is_showing_legend = st.checkbox(
            "Showing the legends",
            value=False,
            key="is_showing_legend",
        )
    with cols_legend[1]:
        legend = create_textbox(
            "legend",
            str,
            default_value="" if filename is None else filename,
            key="legend",
        )

    cols_xtickslabels = st.columns(2)
    with cols_xtickslabels[0]:
        is_set_xticklabels = st.checkbox(
            "changing the x-axis scale to classes",
            value=False,
            key="is_set_xticklabels",
        )

    with cols_xtickslabels[1]:
        label_angle = create_textbox(
            "Angle of label",
            float,
            default_value="0",
            key="label_angle",
        )

    is_created_fig = st.form_submit_button("create graph")

st.markdown("# Showing graph")
if data is None:
    st.caption("Please select valid csv file.")
else:
    fig = plot_hist(
        x=data * unit_cvt_const,
        xlim=(x_min, x_max),
        ylim=(y_min, y_max),
        step=histogram_step,
        bin_width=bin_width,
        x_label=x_label,
        y_label=y_label,
        label_angle=label_angle,
        legend=legend,
        is_set_xticklabels=is_set_xticklabels,
        is_showing_legend=is_showing_legend,
    )

    st.pyplot(fig)

    st.markdown("# Download configuration")
    with st.form("configuration of image"):
        # Select image formats
        image_format_options = ["png", "jpg", "svg", "pdf"]
        image_format = st.selectbox(
            label="image format",
            options=image_format_options
        )
        # Set resolution
        dpi = create_textbox(
            label="Dot per inch",
            value_type=float,
            default_value="500",
            key="dpi"
        )
        st.form_submit_button("Set configuration")

    if image_format in image_format_options:
        # Buffering figure as image
        buf = BytesIO()
        fig.savefig(buf, format=image_format, dpi=dpi)
        buf.seek(0)

        # Downloading buffered image
        st.download_button(
            label="save figure",
            data=buf,
            file_name=f"{filename}.{image_format}",
            mime=f"image/{image_format}",
        )
        buf.close()
    else:
        st.text("⚠️: Invalid value")
