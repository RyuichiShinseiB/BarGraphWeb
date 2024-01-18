import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import streamlit as st
from io import BytesIO
from src.widgets import create_textbox

st.title("Create Bar Graph!")

st.markdown("# Gpaph configuration")
with st.form(key="config_form"):
    # ファイルの選択
    st.markdown("### Upload your csv file")
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

    st.markdown("### Unit conversion")
    nm_per_px = st.text_input("unit: nm / pixel", value="1", key="nm_per_px")

    # configuration of x range
    st.markdown("### Set x-axis range")
    cols_x_minmax = st.columns(2)
    with cols_x_minmax[0]:
        x_min = create_textbox("x-min", default_value="nan", key="x_min")
    with cols_x_minmax[1]:
        x_max = create_textbox("x-max", default_value="nan", key="x_max")

    # configuration of y range
    st.markdown("### Set y-axis range")
    cols_y_minmax = st.columns(2)
    with cols_y_minmax[0]:
        y_min = create_textbox("y-min", default_value="nan", key="y_min")
    with cols_y_minmax[1]:
        y_max = create_textbox("y-max", default_value="nan", key="y_max")

    is_created_fig = st.form_submit_button("create graph")

# TODO: ヒストグラムの間隔やヒストグラムを求める計算を行う関数を実装する

st.markdown("# Showing graph")
if data is None:
    st.caption("Please select valid csv file.")
else:
    # TODO: 上で設定したやつを適応する
    # Display figure
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(data[:, 0], data[:, 1])
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
