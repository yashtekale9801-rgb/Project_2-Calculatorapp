# Product Requirements Document: Scientific Calculator

**Status:** Draft  
**Product:** Calculator  
**Document owner:** Product / Engineering  
**Last updated:** 2026-10-04

## 1. Summary

Evolve the current addition-only Streamlit prototype into a dependable scientific calculator for students and technical users. The product should support direct keypad entry and editable mathematical expressions, make angle and precision settings visible, and present results clearly with useful error feedback.

The first delivery remains a web application. The interface must adapt to small touch screens so the web experience is useful on mobile. A later native mobile application should reuse the same calculation rules and provide feature parity for the agreed core calculator workflow.

## 2. Current State

The repository currently contains:

- `main.py`: an `add(num1, num2)` function and a small command-line prompt.
- `app.py`: a Streamlit interface for entering two numbers and displaying their sum.
- `requirements.txt`: the Streamlit dependency.

There is no scientific expression parser, operation selection, calculation history, mobile-specific client, or automated test suite yet. The current implementation is a prototype and is not evidence that advanced mathematical behavior has been validated.

## 3. Problem and Opportunity

Users need a calculator that can handle common scientific expressions without obscuring how the answer was computed. As functionality grows, calculation behavior must remain predictable across interfaces, particularly for precedence, angle units, precision, and invalid expressions. Keeping the calculation engine independent from Streamlit will make it practical to add a mobile client later without duplicating mathematical rules.

## 4. Product Goals

1. Support common arithmetic and scientific calculations with explicit, consistent rules.
2. Let users enter expressions efficiently by keyboard, keypad, or touch.
3. Show enough context with each result to help users catch input and mode mistakes.
4. Work comfortably on desktop and mobile web layouts.
5. Keep calculation behavior in a reusable, well-tested core that can serve a future native mobile application.
6. Make errors understandable and recoverable without silently returning misleading results.

## 5. Non-Goals for the Initial Releases

- Computer algebra, symbolic simplification, or proof generation.
- Graphing, plotting, or equation solving.
- Spreadsheet, unit-conversion, or programming-language features.
- Cloud accounts, cross-device synchronization, or server-side storage of calculation history.
- Claims of suitability for safety-critical, financial, clinical, or regulated calculations.

These may be reconsidered after the core calculator is validated with users.

## 6. Target Users

- **Student:** performs coursework calculations and needs clear expressions, angle modes, and understandable errors.
- **Technical user:** performs repeated calculations and values keyboard entry, history, constants, and predictable precision.
- **Occasional user:** needs familiar arithmetic and a simple interface that does not expose unnecessary controls.

## 7. Product Principles

- **Show the work:** display the submitted expression and result together.
- **Make modes visible:** angle unit and display format must not be hidden or ambiguous.
- **Be explicit about limits:** distinguish invalid input, undefined operations, and display rounding.
- **Keep calculation rules portable:** UI code must not own mathematical semantics.
- **Design for touch and keyboard:** neither input method should be second-class.

## 8. Scope and Roadmap

### Phase 0: Reliable Calculation Foundation

- Move calculation behavior into a UI-independent module with an explicit operation API.
- Define numeric input limits, result formatting, and error behavior for the four basic arithmetic operations.
- Add automated tests for addition, subtraction, multiplication, division, and division by zero.
- Plan the constrained expression grammar and parser approach needed for Phase 2; do not use unrestricted `eval` or execute user-provided code.

**Exit criteria:** basic-operation tests pass; division by zero fails safely; the web interface calls the same core API as tests.

### Phase 1: Basic Calculator Web MVP

- Provide two numeric inputs and an explicit operation choice for addition, subtraction, multiplication, or division.
- Display the selected operation, both operands, and the result clearly.
- Handle division by zero without crashing or returning a misleading result; preserve entered operands so users can correct them.
- Provide clear/reset behavior and a responsive baseline suitable for desktop and narrow screens.

**Exit criteria:** all Phase 1 P0 requirements in Section 9 pass; all four operations and division-by-zero behavior are covered by tests.

### Phase 2: Scientific Calculator Web MVP

- Add editable mathematical expression entry and a scientific keypad, backed by a constrained parser.
- Support expression grouping, standard precedence, signs, powers, roots, absolute value, factorial, logarithms, trigonometric functions, and constants.
- Provide degree/radian mode, clear/delete, understandable domain and syntax errors, result formatting, and current-session history.
- Keep the scientific interface usable on desktop and narrow web viewports; defer the dedicated mobile-browser usability pass to Phase 3.

**Exit criteria:** all Phase 2 P1 scientific requirements in Section 9 pass; calculation behavior is covered by core tests and the web UI works at the agreed baseline viewports.

### Phase 3: Responsive Mobile Web

- Refine the web layout for narrow screens, touch targets, portrait orientation, and on-screen keyboard behavior.
- Validate supported mobile browsers and ensure the expression and result remain visible while editing.
- Collect user feedback on keypad layout, history, and advanced-function discoverability.

**Exit criteria:** usability review passes on agreed iOS and Android browser versions, with no horizontal overflow in core calculator flows.

### Phase 4: Native Mobile Application

- Choose a native or cross-platform implementation after confirming user demand and platform requirements.
- Reuse the calculation core or a behaviorally equivalent implementation verified against shared test vectors.
- Provide offline calculations and local history; do not require sign-in for core calculator use.
- Decide separately whether platform features such as widgets, haptics, or synchronization are valuable.

**Exit criteria:** release targets, distribution method, accessibility expectations, and calculation parity tests are agreed before implementation.

## 9. Functional Requirements

Priorities: **P0** required for the Phase 1 basic web MVP; **P1** required for the Phase 2 scientific web MVP; **P2** expected in later enhancement or mobile phases.

### Basic Calculation (Phase 1)

- **FR-01 (P0):** Users can enter two numeric operands and explicitly select addition, subtraction, multiplication, or division.
- **FR-02 (P0):** The calculator displays both operands, the selected operation, and the result together.
- **FR-03 (P0):** Users can clear/reset the inputs and correct either operand before recalculating.
- **FR-04 (P0):** Division by zero produces a clear error; it never crashes or silently returns zero or infinity.
- **FR-05 (P0):** Basic results are displayed with enough precision to avoid misleading users.

### Expression Entry and Scientific Operations (Phase 2)

- **FR-06 (P1):** Users can enter and edit a complete expression in a visible expression field and submit by keyboard or on-screen action.
- **FR-07 (P1):** The calculator evaluates parentheses and standard arithmetic precedence consistently, including unary positive and negative signs.
- **FR-08 (P1):** The calculator uses a constrained mathematical parser and never executes arbitrary Python, JavaScript, or other user-provided code.
- **FR-09 (P1):** Users can clear the full expression and delete the last entry.
- **FR-10 (P1):** Support powers, square roots, absolute value, factorial for valid non-negative integer inputs, `log10`, `ln`, and sine, cosine, and tangent.
- **FR-11 (P1):** Support the constants pi and e.
- **FR-12 (P1):** Provide a visible degree/radian setting for supported trigonometric calculations. Changing it must not silently rewrite the expression. If inverse-trigonometric functions are added later, their result convention must be documented and tested.

### Results, Errors, and History

- **FR-13 (P1):** Display the submitted expression and result together without misleading rounding; make displayed precision configurable or discoverable.
- **FR-14 (P1):** Handle invalid function domains, malformed expressions, overflow, and non-finite results with a concise message and a way to edit the expression.
- **FR-15 (P1):** Do not silently convert an invalid or undefined calculation to zero.
- **FR-16 (P1):** Keep a current-session history of expressions and results; selecting an entry restores its expression for editing or recalculation.
- **FR-17 (P2):** Let users choose standard, scientific, or engineering notation and configure displayed significant digits.
- **FR-18 (P2):** Support inverse and hyperbolic trigonometric functions, reciprocal, and percentage operations after their semantics are specified and tested.
- **FR-19 (P2):** Support calculation memory actions (store, recall, add, subtract, clear) if usability testing confirms they are needed.

### Usability and Platform

- **FR-20 (P0):** The Phase 1 web UI works on desktop and narrow mobile viewport widths without clipping essential controls or requiring horizontal scrolling.
- **FR-21 (P0):** Interactive controls have accessible labels and keyboard focus states; touch controls are usable on narrow screens.
- **FR-22 (P1):** The current angle mode and any result-format mode are visible whenever they affect calculation or interpretation.
- **FR-23 (P2):** Provide keyboard shortcuts for common actions where they do not conflict with normal text editing.
- **FR-24 (P2):** The future mobile app supports the core calculation, mode, result, and history workflows without network access.
- **FR-25 (P2):** The future mobile app uses shared calculation tests to verify parity with the web calculator.

## 10. Non-Functional Requirements

- **Correctness:** Define and test operator precedence, function domains, angle conversion, factorial limits, overflow behavior, and rounding. Use a documented floating-point strategy; distinguish displayed rounding from the stored calculation value.
- **Performance:** For normal calculator expressions, return results without perceptible delay on supported devices. Establish a measurable latency target after the implementation platform is selected.
- **Reliability:** Calculation errors must not crash the application or discard the expression being edited.
- **Accessibility:** Meet WCAG 2.2 AA for the web interface where applicable, including contrast, labels, focus order, and non-color-only feedback. Test screen-reader use for expression entry and result announcements.
- **Privacy:** Keep scientific calculation history local to the current session for the web MVP. Do not send expressions to analytics or external services by default.
- **Security:** Parse a constrained mathematical grammar; limit expression length, nesting depth, and computationally expensive operations.
- **Compatibility:** Document supported desktop and mobile browsers before release. Native platform support is to be decided in Phase 4.

## 11. UX Requirements

- Keep the active expression and result visually distinct and easy to scan.
- Keep essential arithmetic and delete/clear controls prominent; expose advanced functions without making the layout dense on small screens.
- Preserve the expression after successful evaluation so users can inspect or edit it.
- Show the active angle mode near trigonometric controls and results.
- Present errors next to the expression, state what needs correction, and preserve user input.
- On mobile, prioritize a stable keypad and expression area above optional history and secondary settings.

## 12. Technical Direction

The implementation should be organized into three responsibilities:

1. **Calculation core:** parsing, evaluation, numeric/error behavior, and shared test vectors; independent of Streamlit and mobile UI frameworks.
2. **Web presentation:** expression input, keypad, settings, history display, and responsive behavior.
3. **Mobile presentation (later phase):** native interaction and platform integration, consuming the same core contract or conforming to its shared tests.

The current Streamlit UI can serve as a prototype and early web delivery. Before introducing scientific expressions, engineering should decide whether Streamlit remains suitable for the interaction and responsive requirements or whether the web presentation should move to a framework better suited to a custom keypad. That decision must not entangle or duplicate the calculation core.

## 13. Success Measures

Targets below are proposed and must be validated with users before being treated as commitments:

- At least 95% of representative Phase 1 basic and Phase 2 scientific calculation tasks completed without assistance in usability testing.
- No known P0 calculation correctness failures in the release test suite.
- At least 90% of tested users correctly identify the active angle mode and the expression that produced a result.
- Core calculation workflow completes on target mobile browsers without clipped controls or horizontal scrolling.
- For a future native release, shared test vectors produce equivalent results and errors across web and mobile implementations.

## 14. Risks and Mitigations

- **Ambiguous math conventions:** specify precedence and behavior for implicit multiplication, unary signs, percentages, and factorial before coding; test boundary cases.
- **Floating-point surprises:** explain displayed precision and add tests for small, large, and repeating values; consider arbitrary-precision decimal support only if user needs justify it.
- **Unsafe expression evaluation:** use a constrained parser and resource limits; prohibit unrestricted `eval`.
- **Streamlit interaction limits:** prototype expression editing and touch layout early; revisit the web UI technology before investing in a large keypad interface.
- **Platform divergence:** define a calculation API and shared conformance vectors before starting the mobile client.
- **Overexpansion:** defer graphing, symbolic algebra, synchronization, and advanced modes until core scientific use is validated.

## 15. Open Product Decisions

1. Which users and education levels are the primary launch audience?
2. Which web technology should own the scientific keypad and expression editor: Streamlit for the MVP, or a dedicated frontend?
3. Should percentage follow standard calculator button behavior, or be expression-based only?
4. Is standard floating-point precision sufficient, or is arbitrary precision required for the target audience?
5. Which mobile platforms and distribution channels are required for the native phase?
6. Should history persist beyond a browser session, and if so, where should it be stored?
7. Are there accessibility, localization, or offline requirements beyond those in this draft?

## 16. Release Readiness Checklist

- P0 functional and non-functional requirements are implemented and tested.
- Calculation grammar, precedence, angle behavior, precision, and error semantics are documented.
- Automated tests cover normal cases, edge cases, and invalid expressions.
- Desktop and mobile web usability checks pass on the agreed browser/device matrix.
- Accessibility and security checks are complete for the supported release scope.
- Known limitations are visible to users and documented for support.
- Native mobile scope is not committed until the Phase 4 decisions are resolved.
