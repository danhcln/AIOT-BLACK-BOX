---
name: orch-fix-defect
description: Systematic hardware and schematic defect debugging workflow. Use when ERC fails, nets are disconnected or misnamed, pins mismatch datasheets, power rails cross, exports fail, or unexpected regressions occur. Enforces root-cause isolation before applying minimal targeted fixes.
metadata:
  origin: ECC
---

# orch-fix-defect — Systematic Hardware Defect Resolution

Systematic debugging workflow adapted from ECC `skills/orch-fix-defect/SKILL.md`, `commands/orch-fix-defect.md`, and `agents/build-error-resolver.md` for KiCad schematic defects.

## Core Principle
**Determine root cause before applying a fix.**  
Never apply speculative edits, random wire moves, or blind refactoring. Identify the exact mechanism causing the defect, isolate the minimal fix, and verify it back to green.

## Invocation Policy
For schematic problems, ERC failures, or incorrect nets:
```text
orch-fix-defect
  → verification-loop
```

## Defect Trigger Categories
Activate this workflow whenever:
1. **ERC Violations**: Pin connected to other pin with incompatible electrical type, power pin not driven, conflicting net labels.
2. **Disconnected Pins / Nets**: Missing wire segments, misaligned pin coordinates, typo in global or hierarchical labels.
3. **Duplicate Connections / Shorts**: Two different power rails or signal nets accidentally shorted or sharing a label.
4. **Power Rail Inconsistencies**: Accidental connection or confusion among protected power domains:
   - `VBAT`: 18650 Li-ion battery rail (PRIMARY POWER SOURCE)
   - `VBUS`: External USB-C charging/input source (NOT primary operating power)
   - `5V_SYS`: Regulated 5V system rail (must NOT be renamed to `+5V`; must NOT be merged with `VBUS`)
   - `3V3_SYS`: Regulated 3.3V peripheral/logic rail (must NOT be fed from ESP32 DevKit onboard regulator)
   - `GND`: Common ground
5. **Battery ADC Sense Defects**: Issues touching `GPIO1 = ADC_VBAT_SENSE` or voltage divider.
6. **ESP32 Power Misconceptions**: Schematic erroneously drawing peripheral power from ESP32 GPIOs or DevKit pins instead of system power rails.
7. **Pinout / Symbol Mismatches**: Custom symbol pin order or numbering disagrees with manufacturer datasheet.
8. **Missing No-Connect Flags**: Real exposed module pins left floating without a KiCad `no_connect` marker.
9. **Export / CLI Failures**: `kicad-cli` fails to generate SVG/PDF due to syntax errors or corrupt S-expressions.
10. **Visual Overlaps**: Text, pin labels, or wire lines crossing symbol outlines or colliding with other elements.
11. **Unexpected Regressions**: Circuitry that was previously correct suddenly shows errors or missing connections.

## Systematic Debugging Protocol

### Phase 1: Defect Intake & Reproduction
- Extract the exact error message or visual anomaly.
- If ERC failed, parse the report: identify pin numbers, component reference designators, and coordinate locations:
  ```powershell
  kicad-cli sch erc --output report.rpt "AIOT_BLACKBOX_PRESENTATION.kicad_sch"
  ```
- Do not attempt fixes before understanding the exact reported issue.

### Phase 2: Root Cause Investigation
- Trace the issue directly to the underlying element:
  - Check S-expression syntax and coordinates.
  - Verify pin electrical types (`input`, `output`, `power_in`, `passive`, `no_connect`).
  - Cross-check against the authoritative component datasheet.
  - Compare with the known good baseline or backup.
- Distinguish between a cosmetic warning and a true electrical fault.

### Phase 3: Minimal Targeted Fix
- Apply the fix strictly to the isolated component, pin, or net.
- Do not rewrite surrounding blocks or change global styles.
- Preserve all existing symbol IDs, references, and non-defective wiring.

### Phase 4: Verification to Green
- Re-run the diagnostic check:
  - Re-run KiCad CLI ERC to verify zero remaining errors.
  - Re-export the schematic to PDF/SVG and visually inspect the repaired zone.
- Confirm the fix resolved the error completely.

### Phase 5: Transition to Verification Loop
- Hand off to `verification-loop` to execute the full 6-phase verification and emit the formal report.
