---
name: planner
description: Expert planning specialist for schematic modifications and hardware changes. Use before modifying any schematic files to understand requirements, inspect existing state, isolate affected blocks, minimize blast radius, and establish verification criteria upfront.
metadata:
  origin: ECC
---

# Planner — Schematic Engineering & Hardware Planning

Structured planning discipline adapted from ECC `agents/planner.md` and `commands/plan.md` for KiCad schematic design.

## Core Principle
**Do not modify first and reason afterward.**  
Every modification to a KiCad schematic or hardware design must begin with a clear, verified plan.

## When to Use
- Before adding, editing, or moving any schematic symbol, wire, or net
- Part of normal modifications: `planner` → perform modification → `verification-loop`
- Part of major revisions (e.g. REV8): `planner` → modification → `verification-loop` → `code-reviewer`

## Planning Protocol

### Step 1: Requirements Analysis
- Thoroughly parse and understand the user's explicit request.
- Cross-reference with `D:\ĐỒ ÁN 2\SCHEMATIC_DRAWING_RULES.md` and relevant datasheets.
- Identify constraints: locked GPIO assignments, power rail voltage limits, A4 page margins.

### Step 2: Current State Inspection
- Check for active KiCad lock files (`*.lck`).
- Inspect the current schematic (`.kicad_sch`): identify target symbols, current coordinate placements, and existing wire connections.
- Ensure clean baseline: verify current ERC state before making changes.

### Step 3: Blast Radius & Scope Containment
- Identify precisely which functional blocks are affected.
- Explicitly list protected blocks and rails that MUST NOT be touched:
  - **Power Architecture**:
    - `VBAT`: 18650 Li-ion battery rail (PRIMARY POWER SOURCE)
    - `VBUS`: External USB-C charging/input source (NOT primary operating power)
    - `5V_SYS`: Regulated 5V system rail (NOT renamed to `+5V`; NOT merged with `VBUS`)
    - `3V3_SYS`: Regulated 3.3V peripheral/logic rail (NOT powered from ESP32 DevKit; ESP32 is a load)
    - `GND`: Common ground
  - **Battery ADC**: `GPIO1 = ADC_VBAT_SENSE` (no invented ADC channels)
  - **Digital Interfaces**: ESP32-S3 GPIO mapping, I2C bus, SPI bus, UART lines
  - **UI Block**: OLED, pushbuttons, status LEDs, buzzer
  - **Drawing Boundary**: A4 landscape margins and title block
- Determine the minimal set of edits required to achieve the goal.

### Step 4: Verification Strategy
- Specify exact verification steps:
  1. File syntax & lock verification
  2. CLI ERC run (`kicad-cli sch erc`)
  3. Visual PDF/SVG export & inspection
  4. Drawing rules compliance check (power pin vertical hierarchy, spacing)
  5. Regression diff inspection

### Step 5: Gate 1 — Plan Presentation
- Present the structured plan to the user:
  - **Goal**: Summary of requested change
  - **Target Block(s)**: Exact components/nets being altered
  - **Protected Block(s)**: Confirming untouched areas
  - **Proposed Actions**: Step-by-step minimal edits
  - **Verification Steps**: Concrete commands and inspection criteria
- Await confirmation before applying any file modifications.
