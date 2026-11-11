---
name: verification-loop
description: Comprehensive six-phase verification loop for KiCad hardware and schematic engineering. Enforces strict quality gates before completing any task — file integrity, electrical connectivity, ERC CLI execution, PDF/SVG visual render inspection, drawing rules compliance, and diff regression checks. Produces a formal PASS/FAIL verification report. Never claim DONE, PASSED, FINAL, or READY without running this verification.
metadata:
  origin: ECC
---

# verification-loop — KiCad Hardware & Schematic Verification

Six-phase verification engine adapted from ECC `skills/verification-loop/SKILL.md` for KiCad schematic engineering and hardware validation.

## Core Mandate
**Never claim `DONE`, `PASSED`, `FINAL`, or `READY` until verification has actually executed.**  
A task is never complete merely because an edit was written. Every claim of completion requires evidence across all six verification phases.

## The Six Verification Phases

### Phase 1: File Integrity & Lock Safety
- Verify that the target schematic file is valid and readable.
- Check that no active KiCad lock file (`*.lck`) exists in the directory.
- Verify that a backup copy was captured before edits began.
- Ensure S-expression parenthetical balance is valid if modified programmatically.

### Phase 2: Electrical Connectivity & Pin Integrity
- Inspect modified pins and net labels for proper electrical types (`input`, `output`, `power_in`, `passive`, `no_connect`).
- Verify no pins are left floating unintentionally.
- Confirm all unused real module pins have explicit `no_connect` symbols.
- Ensure power pins follow vertical orientation: positive power (`VBUS`, `VBAT`, `5V_SYS`, `3V3_SYS`) near top, `GND` at bottom, horizontal exit.
- Verify ESP32 GPIO pins are not treated or wired as peripheral power sources.

### Phase 3: KiCad CLI ERC Execution
- Run KiCad CLI Electrical Rules Check:
  ```powershell
  kicad-cli sch erc --output erc_report.rpt --format json "AIOT_BLACKBOX_PRESENTATION.kicad_sch"
  ```
- Parse the output:
  - Report total errors and warnings.
  - Investigate any electrical errors (shorts, undriven nets, pin conflicts).
  - Confirm all errors are resolved (zero blocking errors).

### Phase 4: Visual Export & Render Inspection
- Export the schematic to vector format (PDF / SVG):
  ```powershell
  kicad-cli sch export pdf "AIOT_BLACKBOX_PRESENTATION.kicad_sch"
  kicad-cli sch export svg "AIOT_BLACKBOX_PRESENTATION.kicad_sch"
  ```
- Inspect visual presentation:
  - No overlapping text strings or labels.
  - No wires passing through symbol text or pin numbers.
  - Title block text and sheet borders properly aligned within A4 format.

### Phase 5: Drawing Rules Compliance
- Cross-check against `D:\ĐỒ ÁN 2\SCHEMATIC_DRAWING_RULES.md`:
  - Power pins strictly follow the vertical order convention (`VBUS`, `VBAT`, `5V_SYS`, `3V3_SYS` top, `GND` bottom).
  - Functional blocks are logically grouped with clean spacing.
  - Net labels adhere to standard naming conventions.

### Phase 6: Diff Review & Regression Check
- Compare the modified schematic against the baseline:
  - Confirm ONLY the requested elements/nets changed.
  - Confirm protected areas have zero unintended differences:
    - **Primary Power**: `VBAT` (18650 battery) preserved as primary power source.
    - **External Input**: `VBUS` preserved as external USB-C input/charging.
    - **System Power Rails**: `5V_SYS` (regulated 5V rail; NOT renamed to `+5V`; NOT merged with `VBUS`), `3V3_SYS` (regulated 3.3V peripheral/logic rail; NOT powered from ESP32 DevKit onboard regulator), `GND`.
    - **Battery ADC**: `GPIO1 = ADC_VBAT_SENSE` (divider intact; no invented ADC channels).
    - **Digital Interfaces**: ESP32-S3 GPIO mapping, I2C, SPI, UART lines.
    - **UI**: Display, switches, LEDs, buzzer circuits.

---

## Mandatory Output: Verification Report

At the conclusion of the verification loop, emit a formal report in this exact format:

```text
============================================================
KICAD HARDWARE VERIFICATION REPORT
============================================================
Phase 1 - File Integrity & Locks:    [PASS / FAIL] (Backup created, no lock collision)
Phase 2 - Electrical Connectivity:   [PASS / FAIL] (Pins validated, no floating nets)
Phase 3 - KiCad ERC Check:           [PASS / FAIL] (0 errors, X warnings reviewed)
Phase 4 - Visual Export & Render:    [PASS / FAIL] (PDF/SVG exported and visually verified)
Phase 5 - Project Rules Compliance:  [PASS / FAIL] (Compliant with SCHEMATIC_DRAWING_RULES.md)
Phase 6 - Regression & Diff Review:  [PASS / FAIL] (Protected domains untouched)

OVERALL VERDICT: [PASS / FAIL]
============================================================
```

If any phase fails, the overall verdict is `FAIL` and the issue must be resolved using `orch-fix-defect` before claiming completion.
