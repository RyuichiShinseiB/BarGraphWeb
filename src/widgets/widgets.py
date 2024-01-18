import numpy as np
import streamlit as st


def create_textbox(
    label: str,
    default_value: str = "",
    key: str | None = None
) -> float:
    input_tmp = st.text_input(label, value=default_value, key=key)
    # TODO: `default_value`の型と出力の型を合わせるようにする
    # TODO: `except`が起きた場合、`default_value`を出力するようにする
    try:
        return float(input_tmp)
    except ValueError:
        st.markdown("Set a Numerical value")
        return np.nan
