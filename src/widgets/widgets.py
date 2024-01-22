from typing import Callable, TypeVar

import streamlit as st

T = TypeVar("T", str, int, float)


def create_textbox(
    label: str,
    value_type: type[T],
    default_value: str = "",
    key: str | None = None,
    cvt_func: Callable[[str], T] | None = None,
) -> T:
    input_tmp = st.text_input(label, value=default_value, key=key)
    try:
        if cvt_func is None:
            return value_type(input_tmp)
        else:
            return cvt_func(input_tmp)
    except ValueError:
        st.markdown("Set a Numerical value")
        return value_type(default_value)
