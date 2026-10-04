# Project Summary: Calculator

**Current delivery:** Phase 0 foundation and Phase 1 basic web calculator  
**Status:** Phase 1 implemented; Phase 2 not started  
**Related documents:** [Product requirements](PRD.md) · [Implementation plan](IMPLEMENTATION_PLAN.md)

## What the Project Does Today

The project is a Streamlit web calculator for two-operand arithmetic. Users enter two numbers, choose Add, Subtract, Multiply, or Divide, and submit to see the operands, operation, and result together. Clear resets the inputs and operation. Division by zero displays a recoverable error and retains the entered operands. The page has explicit contrast styling for operation labels and the Clear button.

The existing command-line entry point still supports addition through `main.py`.

## Implementation Overview

- [calculator_core.py](calculator_core.py) contains the UI-independent arithmetic API. `calculate()` accepts two finite real operands and an `Operation`; `add()` preserves the original addition helper. Structured calculator errors distinguish invalid operands, unsupported operations, division by zero, and non-finite results.
- Results are calculated using Python floating-point numbers and formatted to 12 significant digits by default, configurable up to 17 through `format_result()`.
- [app.py](app.py) implements the Streamlit interface and delegates all arithmetic to the core.
- [main.py](main.py) preserves the original command-line addition flow.
- [test_calculator_core.py](test_calculator_core.py) covers arithmetic and result formatting. [test_app.py](test_app.py) covers operation selection, displayed equations, division-by-zero recovery, and clearing.
- [requirements.txt](requirements.txt) declares Streamlit. The tests use Python's standard-library `unittest` and Streamlit's included AppTest API.

## Run and Verify

Start the web app from the project directory:

```powershell
python -m streamlit run app.py
```

Run the core and UI tests:

```powershell
python -m unittest -v test_calculator_core test_app
```

The last recorded test run passed 15 tests. Streamlit AppTest may print harmless `missing ScriptRunContext` warnings while running in bare test mode.

## Current Scope and Limitations

- The web UI handles one operation on two operands at a time; it does not parse full expressions or support parentheses and precedence.
- Scientific functions, constants, angle modes, calculation history, and memory controls are not implemented.
- Mobile web received a basic responsive layout, but Phase 3 device/browser usability validation has not been completed.
- There is no native mobile client, offline mobile workflow, account, or cross-device synchronization.
- Floating-point arithmetic can have normal binary64 precision limits; displayed rounding is separate from the internal result.

## Recommended Next Work: Phase 2

Use Phase 2 in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) as the source of truth:

1. Decide expression semantics before coding: precedence, unary signs, function syntax, implicit multiplication, factorial boundaries, percentage behavior, and numeric/resource limits.
2. Choose and document a constrained parser approach. Never evaluate user expressions with unrestricted `eval`.
3. Extend the calculation core with expression parsing and scientific operations: powers, roots, absolute value, factorial, logarithms, trigonometric functions, and pi/e.
4. Add visible degree/radian mode, editable expression and keypad input, specific syntax/domain/overflow feedback, and current-session history.
5. Verify core behavior with shared test vectors and automated tests; add UI integration tests for modes, errors, keypad/keyboard behavior, and history.
6. Reassess whether Streamlit supports the expression editor and keypad interaction before investing in the Phase 2 UI.

Keep graphing, symbolic algebra, synchronization, and native mobile work deferred until their later planned phases and product decisions.
