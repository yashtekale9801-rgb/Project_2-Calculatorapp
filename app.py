import streamlit as st

from calculator_core import CalculatorError, Operation, calculate, format_result


st.set_page_config(page_title="Calculator", page_icon="+", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at 15% 5%, rgba(198, 232, 102, .22), transparent 34%),
            #f5f6ef;
        color: #19221b;
    }
    .block-container {
        max-width: 680px;
        padding-top: 4rem;
        padding-bottom: 3rem;
    }
    .kicker {
        color: #54634e;
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .12em;
        text-transform: uppercase;
    }
    h1 {
        color: #19221b;
        font-size: 3.2rem !important;
        letter-spacing: 0 !important;
        margin: .35rem 0 .25rem !important;
    }
    .intro {
        color: #667064;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, .76);
        border: 1px solid #dfe4d7;
        border-radius: 8px;
        padding: 1.5rem;
    }
    div[data-testid="stNumberInput"] label {
        color: #465344;
        font-weight: 600;
    }
    div[data-testid="stNumberInput"] input {
        background: #fff;
        color: #19221b !important;
        caret-color: #19221b;
    }
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] [data-testid="stWidgetLabel"] p {
        color: #19221b !important;
        opacity: 1 !important;
    }
    div[data-testid="stFormSubmitButton"] button {
        background: #c6e866;
        border: 0;
        border-radius: 6px;
        color: #19221b;
        font-weight: 700;
        min-height: 2.8rem;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background: #b4d952;
        border: 0;
        color: #19221b;
    }
    div[data-testid="stButton"] button {
        background: #fff;
        border: 1px solid #cbd3c4;
        border-radius: 6px;
        color: #19221b !important;
    }
    div[data-testid="stButton"] button p {
        color: #19221b !important;
    }
    div[data-testid="stButton"] button:hover {
        background: #e9eddf;
        border-color: #aeb9a5;
    }
    .answer {
        background: #19221b;
        border-radius: 8px;
        color: #f5f6ef;
        margin-top: 1.25rem;
        padding: 1.35rem 1.5rem;
    }
    .answer-label {
        color: #c6e866;
        font-size: .75rem;
        font-weight: 700;
        letter-spacing: .1em;
        text-transform: uppercase;
    }
    .answer-value {
        font-size: 2.4rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: .35rem;
        overflow-wrap: anywhere;
    }
    .answer-equation {
        color: #c5cbbd;
        font-size: .95rem;
        margin-top: .4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="kicker">A simple calculator</div>', unsafe_allow_html=True)
st.title("Calculate.")
st.markdown(
    '<div class="intro">Add, subtract, multiply, or divide two numbers.</div>',
    unsafe_allow_html=True,
)


def clear_calculator() -> None:
    st.session_state["first_operand"] = 0.0
    st.session_state["second_operand"] = 0.0
    st.session_state["operation"] = Operation.ADD


st.session_state.setdefault("first_operand", 0.0)
st.session_state.setdefault("second_operand", 0.0)
st.session_state.setdefault("operation", Operation.ADD)

with st.form("calculator_form"):
    left, right = st.columns(2)
    with left:
        num1 = st.number_input(
            "First number",
            value=None,
            step=1.0,
            format="%.12g",
            key="first_operand",
        )
    with right:
        num2 = st.number_input(
            "Second number",
            value=None,
            step=1.0,
            format="%.12g",
            key="second_operand",
        )
    operation = st.radio(
        "Operation",
        options=list(Operation),
        format_func=lambda choice: choice.value.title(),
        horizontal=True,
        key="operation",
    )
    submitted = st.form_submit_button("Calculate", use_container_width=True)

st.button("Clear inputs", on_click=clear_calculator, type="secondary")

if submitted:
    try:
        result = calculate(num1, num2, operation)
    except CalculatorError as error:
        st.error(str(error))
    else:
        equation = (
            f"{format_result(num1)} {operation.symbol} "
            f"{format_result(num2)} = {format_result(result)}"
        )
        st.markdown(
            f'<div class="answer"><div class="answer-label">Your result</div>'
            f'<div class="answer-value">{format_result(result)}</div>'
            f'<div class="answer-equation">{equation}</div></div>',
            unsafe_allow_html=True,
        )