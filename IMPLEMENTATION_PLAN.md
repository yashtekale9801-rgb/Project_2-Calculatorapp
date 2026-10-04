# Scientific Calculator: Implementation Plan

**Status:** Draft  
**Last updated:** 2026-10-04  
**Product requirements:** [PRD.md](PRD.md)

This plan converts the PRD into an ordered delivery sequence. It intentionally has no calendar estimates because team size, platform choices, and release targets have not been agreed. Complete each phase's exit gate before expanding scope into the next phase.

## Delivery Overview

| Phase | Outcome | Main dependency |
|---|---|---|
| 0. Foundation | Tested, UI-independent arithmetic core | Agree on basic-operation and numerical semantics |
| 1. Basic web MVP | Addition, subtraction, multiplication, and division | Phase 0 exit gate |
| 2. Scientific web MVP | Expression parser and scientific operations | Phase 1 exit gate; web technology decision |
| 3. Mobile web | Validated touch-first responsive experience | Phase 2 MVP and target-device matrix |
| 4. Native mobile | Offline mobile client with calculation parity | Mobile demand, platform, and distribution decisions |

## Phase 0: Reliable Calculation Foundation

**Goal:** Establish correct, testable basic arithmetic behavior before expanding the user interface.

### Work items

1. **Resolve basic-operation semantics.** Document behavior for addition, subtraction, multiplication, division, numeric input limits, result formatting, and division by zero. Defer expression syntax and scientific conventions to Phase 2 planning.
2. **Separate the calculation core.** Move calculation rules out of the Streamlit page into a UI-independent module. Define a small API for two operands, an operation, a result, and structured calculation errors.
3. **Preserve existing behavior.** Keep the current addition workflow available through the core and avoid breaking the command-line entry point unless that change is deliberate.
4. **Build the basic test baseline.** Add unit tests for all four operations, positive/negative/fractional operands, zero, division by zero, and result formatting. Add shared basic-operation examples for later clients.
5. **Prepare for Phase 2.** Record the open parser and expression semantics that must be settled before implementing scientific expression entry. Never evaluate user input as executable Python or JavaScript.

### Deliverables

- Documented basic-operation conventions.
- UI-independent arithmetic module and structured errors.
- Automated unit tests and initial shared test vectors.

### Exit gate

- Addition, subtraction, multiplication, and division pass automated tests.
- Division by zero returns an explicit error without crashing or returning a misleading numeric value.
- The Phase 1 web UI can call the core API without owning calculation semantics.
- Basic numeric input and result-format behavior are documented.

## Phase 1: Basic Calculator Web MVP

**Goal:** Extend the current addition prototype to support the four basic arithmetic operations.

### Work items

1. **Add operation selection.** Provide two numeric inputs and an explicit choice of add, subtract, multiply, or divide.
2. **Connect the UI to the core.** Route each selected operation through the Phase 0 API; do not duplicate arithmetic inside UI event handlers.
3. **Show operands and operation.** Present both entered values, the selected operation, and the result together so users can verify the calculation.
4. **Handle division by zero.** Show a clear, recoverable error and keep the entered operands available for correction.
5. **Add clear and repeat behavior.** Let users reset inputs, change either operand or operation, and calculate again without stale results.
6. **Meet baseline interaction requirements.** Ensure labels, keyboard navigation, contrast, and narrow-screen layout work for the basic form.
7. **Add UI integration tests.** Verify all four operations, input preservation, reset behavior, and division-by-zero feedback; keep arithmetic assertions in core tests.

### Deliverables

- Basic web calculator supporting addition, subtraction, multiplication, and division.
- Core unit tests and web UI integration tests.
- Documented division-by-zero behavior and supported browser baseline.

### Exit gate

- Addition, subtraction, multiplication, and division produce correct results for representative integer, decimal, negative, and zero operands.
- Division by zero shows an error, preserves the inputs, and does not crash or display a false result.
- The selected operation and both operands are visible with the result.
- Users can change operands, change operations, clear, and recalculate successfully.
- Keyboard navigation, accessible labels, and desktop/narrow-screen layouts pass the Phase 1 checks.

### Deferred to Phase 2 or later

- Expression parsing, scientific functions, angle modes, constants, and calculation history.
- Graphing, symbolic algebra, accounts, and synchronization.

## Phase 2: Scientific Calculator Web MVP

**Goal:** Add safe expression entry and the scientific operations defined for the scientific web MVP.

### Work items

1. **Lock expression semantics.** Specify tokens, grouping, precedence, associativity, unary signs, function syntax, factorial boundaries, angle behavior, and numeric limits. Explicitly decide whether implicit multiplication and percent are supported.
2. **Implement the constrained parser.** Parse only the documented math grammar; enforce expression length, nesting, and computational limits. Do not use unrestricted `eval`.
3. **Add expression and keypad input.** Support direct editing, keyboard submission, keypad entry, clear, and delete-last. Keep the input intact after calculation and errors.
4. **Add scientific operations.** Implement powers, square roots, absolute value, factorial for valid non-negative integers, `log10`, `ln`, sine, cosine, tangent, pi, and e in the calculation core.
5. **Add angle mode.** Make degree/radian state visible and apply it consistently to trig functions without rewriting the expression.
6. **Present results and errors.** Show expression and result together; handle malformed syntax, division by zero, invalid domains, overflow, and non-finite values without discarding input.
7. **Add session history.** Keep a current-session list of expressions/results; selecting an item restores its expression for editing or recalculation. Do not add accounts or synchronization.
8. **Revisit the web technology decision.** Use the Phase 0 prototype and Phase 1 delivery experience to decide whether Streamlit supports the required expression editing/keypad interaction. If changing UI technology, preserve the calculation-core API and tests.
9. **Add integration and regression tests.** Verify parser/core results, UI state, angle mode, error recovery, keypad and keyboard equivalence, and history.

### Deliverables

- Scientific web MVP for Phase 2 requirements in [PRD.md](PRD.md).
- Constrained parser, expanded calculation tests, and shared test vectors.
- Current-session history and documented scientific behavior/limitations.

### Exit gate

- All Phase 2 P1 requirements in [PRD.md](PRD.md) pass on desktop and agreed baseline viewports.
- Tests cover precedence, grouping, signs, functions, angle modes, domain boundaries, malformed input, division by zero, and formatting.
- No user input is executed as code; parser resource limits and error paths are tested.
- Keyboard and keypad entry yield equivalent expressions; failures preserve the expression.
- History restores prior expressions; angle mode is visible and has verified behavior.

## Phase 3: Responsive Mobile Web

**Goal:** Make the scientific web calculator comfortable for repeated touch use and reliable on target mobile browsers.

### Work items

1. **Define the device/browser matrix.** Select representative iOS and Android devices, viewport sizes, orientations, and browser versions based on intended users.
2. **Review mobile interaction with users.** Test keypad discoverability, expression visibility, mode visibility, error recovery, and history access. Record usability findings and prioritize fixes.
3. **Refine small-screen layout.** Keep expression and result readable while editing; make primary keys reachable; move history and secondary settings so they do not crowd the keypad.
4. **Test keyboard behavior.** Check soft-keyboard appearance, focus movement, viewport resizing, submit behavior, and whether the custom keypad and device keyboard can be used without conflict.
5. **Verify accessibility and resilience.** Recheck contrast, focus, labels, zoom/reflow, screen-reader announcements, slow rendering, and reconnect/reload behavior. Do not promise offline web calculation unless it is separately implemented and tested.
6. **Fix and retest.** Turn usability findings into tracked issues; rerun the same test flows across the device matrix after fixes.

### Deliverables

- Mobile-web usability findings and resolved P0/P1 issues.
- Responsive scientific calculator verified against the agreed matrix.
- Updated supported-browser and known-limitations documentation.

### Exit gate

- Core basic and scientific calculation flows complete on agreed iOS and Android browsers.
- No horizontal overflow, clipped primary controls, or loss of expression during viewport changes.
- Users can enter, submit, inspect, edit, and recover from errors using touch.
- Accessibility checks for the agreed mobile scope pass.

## Phase 4: Native Mobile Application

**Goal:** Deliver a native or cross-platform mobile client only after platform and distribution needs are known, while preserving calculation parity.

### Entry decisions

Resolve target operating systems, native versus cross-platform approach, distribution channel, accessibility bar, minimum device support, privacy expectations, and whether persistent history is required. Confirm the product need for a separate app rather than assuming that responsive web is insufficient.

### Work items

1. **Choose the calculation reuse strategy.** Reuse a portable calculation library where feasible; otherwise implement the same documented contract and run the shared conformance vectors against both clients.
2. **Define the mobile application architecture.** Keep UI, local history/storage, and calculation behavior separated. Core calculations must not need a network connection or account.
3. **Implement the parity workflow.** Support expression entry, keypad, scientific functions, angle and display modes, results, errors, and local history as agreed for mobile.
4. **Implement mobile-specific behavior.** Validate system keyboard interaction, accessibility services, rotation/resizing, app lifecycle, local persistence, and platform navigation.
5. **Validate privacy and security.** Keep calculation data local by default. Document and obtain explicit product approval before adding analytics, backups, sync, or account features involving expressions/history.
6. **Release progressively.** Use internal/device testing before public distribution; collect feedback and resolve calculation or data-loss defects before broad release.

### Deliverables

- Approved mobile technical decision record.
- Native/cross-platform application with offline core workflow.
- Shared calculation conformance results and device test report.
- Release, privacy, and support documentation.

### Exit gate

- Shared test vectors match expected values, errors, and mode behavior on web and mobile.
- Core calculator workflows function offline without sign-in.
- Local history behavior matches the agreed product decision and survives expected app lifecycle events.
- Accessibility, privacy, security, and distribution checks for target platforms pass.

## Cross-Phase Engineering Practices

- **Definition of done:** implementation, automated tests, error states, accessibility labels, responsive behavior for the phase, and user-facing documentation are complete before an item is considered done.
- **Calculation test vectors:** maintain a versioned set of expressions, modes, expected outcomes, and expected errors. Use it in every client and after every core change.
- **Test layers:** calculation-core unit tests; parser boundary/security tests; UI integration tests; browser/device acceptance tests; accessibility checks.
- **Change control:** changes to precedence, angle conventions, percentage behavior, precision, or stored history are product behavior changes. Update the PRD, test vectors, and user-facing behavior together.
- **Release safety:** do not use passing UI snapshots as evidence of mathematical correctness. Mathematical correctness must be asserted by core tests and independent expected values.
- **Scope control:** complete the current phase's exit gate before starting deferred capabilities, unless product priorities are explicitly revised.

## Initial Backlog (Next Work)

1. Agree on Phase 0 basic-operation semantics and division-by-zero behavior.
2. Create the UI-independent calculation module and tests for addition, subtraction, multiplication, and division while preserving current addition behavior.
3. Add the Phase 1 operation selector and result display, then verify all four operations and error recovery.
4. Prototype expression editing and keypad behavior to decide whether Streamlit remains suitable for Phase 2.
5. Define the scientific expression grammar and shared test vectors before implementing the Phase 2 parser.
