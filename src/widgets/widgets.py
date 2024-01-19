import streamlit as st
from typing import TypeVar

T = TypeVar("T", str, int, float)


def create_textbox(
    label: str,
    value_type: type[T],
    default_value: str = "",
    key: str | None = None,
) -> T:
    input_tmp = st.text_input(label, value=default_value, key=key)
    try:
        return value_type(input_tmp)
    except ValueError:
        st.markdown("Set a Numerical value")
        return value_type(default_value)
