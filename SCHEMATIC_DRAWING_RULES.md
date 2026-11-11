# AIOT BLACK BOX — SCHEMATIC DRAWING RULES

## 1. AUTHORITATIVE REFERENCES

The lecturer schematic located at:

`D:\ĐỒ ÁN 2\Mẫu của thầy\Project sample schematic.PDF`

is the PRIMARY VISUAL REFERENCE.

Use it to learn:
- schematic organization
- functional block arrangement
- symbol presentation
- wire routing style
- power/GND orientation
- spacing and alignment

DO NOT blindly copy its electrical circuit.

For electrical correctness, the authority order is:

1. Official manufacturer datasheet
2. Official hardware design/reference design
3. Official module documentation
4. Verified project design decisions

The lecturer sample controls VISUAL STYLE.
Official datasheets control ELECTRICAL CORRECTNESS.

---

## 2. MANDATORY POWER-PIN VERTICAL ORDER & ORIENTATION

All pins should normally exit HORIZONTALLY from the LEFT or RIGHT sides of a custom symbol.

However, power pins have a STRICT MANDATORY VERTICAL ORDER:

- **POSITIVE POWER PINS** such as `VCC`, `VIN`, `VBAT`, `+3V3`, `+5V`:
  Must be located near the **TOP** of the symbol's LEFT or RIGHT side.
- **GND PINS**:
  Must be located at the **VERY BOTTOM** of the symbol's LEFT or RIGHT side.

> [!IMPORTANT]
> **GND must NOT be placed directly underneath VCC near the top of the symbol.**
> GND should always be the LOWEST pin, or part of the lowest pin group, on the symbol.

### Preferred Default Convention

Unless specific interface routing dictates otherwise:
- **VCC / positive power**: upper LEFT
- **GND**: lower RIGHT

```text
+3V3 -------- VCC |---------------------------|
                  |                           |
SDA --------- SDA |                           | INT --------
SCL --------- SCL |          DEVICE           |
                  |                           |
                  |---------------------------| GND -------- GND
```

This convention is the PREFERRED style.

### GND Side Selection

GND should normally be placed on the RIGHT side at the BOTTOM of the symbol.

Preferred:

```text
                  |---------------------------|
                  |                           |
                  |          DEVICE           |
                  |                           |
                  |---------------------------| GND -------- GND
```

If routing or the surrounding circuit makes right-side GND clearly worse, GND may be placed on the LEFT side:

Alternative allowed:

```text
                  |---------------------------|
                  |                           |
                  |          DEVICE           |
                  |                           |
GND -------- GND  |---------------------------|
```

**Regardless of LEFT or RIGHT: GND MUST remain at the bottom-most graphical position.**

### Positive Power Side Selection

Positive power should normally be placed on the LEFT side near the TOP.

Preferred:

```text
+3V3 -------- VCC |---------------------------|
                  |                           |
                  |          DEVICE           |
```

The RIGHT side may be used when it produces substantially cleaner connectivity.

**Regardless of LEFT or RIGHT: POSITIVE POWER must remain in the upper region of the symbol.**

### Signal Pin Region

Normal signal/control/interface pins should occupy the middle region of the symbol.
Their LEFT/RIGHT side is selected according to connectivity.

Example:

```text
+3V3 -------- VCC |---------------------------|
                  |                           |
SDA --------- SDA |                           | INT --------
SCL --------- SCL |          DEVICE           | CS  --------
                  |                           |
                  |---------------------------| GND -------- GND
```

Therefore the mandatory vertical organization is:

```text
+---------------------------------------------+
| TOP REGION:                                 |
|   Positive power pins (VCC, 3V3, 5V, etc.)   |
+---------------------------------------------+
| MIDDLE REGION:                              |
|   Signal / interface / control pins         |
+---------------------------------------------+
| BOTTOM REGION:                              |
|   GND pins (lowest graphical position)      |
+---------------------------------------------+
```

### Important Distinction: Horizontal Pins Only

- "VCC at the top" does **NOT** mean a pin exits through the top edge.
- "GND at the bottom" does **NOT** mean a pin exits through the bottom edge.
- Pins still exit **HORIZONTALLY** through LEFT or RIGHT edges.
- The terms "TOP" and "BOTTOM" refer **ONLY** to their vertical elevation along the LEFT/RIGHT sides of the symbol.
- **DO NOT** create vertical VCC/GND pins entering through the top or bottom boundaries of the symbol box.

### Multiple Power / Ground Pins

- If a device contains multiple positive supply pins (e.g. VDD, VDDA, VDDIO): group them in the upper region when practical.
- If a device contains multiple GND pins (e.g. GND, AGND, PGND, EPAD): group them in the lowest region when practical.
- Never change their real pin numbers or electrical functions.

### Default Symbol Organization Template

Unless connectivity requires otherwise, use this default:

- **UPPER LEFT**: VCC / VIN / positive supply
- **MIDDLE LEFT**: input / interface signals coming from the left
- **MIDDLE RIGHT**: output / interface signals going to the right
- **LOWER RIGHT**: GND

Conceptually:

```text
+3V3 -------- VCC |---------------------------|
                  |                           |
INPUT 1 ----------|                           |---------- OUTPUT 1
INPUT 2 ----------|          DEVICE           |---------- OUTPUT 2
INPUT 3 ----------|                           |
                  |---------------------------| GND -------- GND
```

---

## 3. SYMBOL PIN REPOSITIONING

Graphical pin positions MAY be changed to improve readability.

Signal pins should face the components they connect to.

Examples:
- SDA/SCL face the I2C device.
- TX/RX face the UART device.
- SPI pins face the SPI peripheral.
- GPIO/control signals face their destination.

However:

NEVER change a real pin number for visual convenience.
NEVER change a real pin function.
NEVER change the electrical pin type incorrectly.

Allowed:
- graphical position
- graphical side (LEFT or RIGHT)
- graphical vertical ordering (within region constraints)

Not allowed:
- incorrect physical pin number
- invented pin mapping
- incorrect electrical function

Every production pin assignment must be verified against authoritative
documentation.

---

## 4. COMPONENT PLACEMENT BEFORE ROUTING

Do NOT place components randomly and then solve the layout using long wires.

Required workflow:

1. Determine connectivity.
2. Group components by function.
3. Place connected components near each other.
4. Orient related pins toward each other.
5. Reposition graphical pins when appropriate (adhering to Power Top / Signals Middle / GND Bottom).
6. Route wires only after placement is clean.

Placement should reduce wiring complexity BEFORE routing begins.

---

## 5. WIRE CROSSINGS

Avoid unnecessary wire crossings.

Target:
ZERO unnecessary crossings.

If wires cross excessively:

DO NOT accept the layout immediately.

First try:
- moving symbols
- rotating/reorienting symbols
- rearranging graphical pin positions (within region rules)
- changing block placement
- using appropriate net labels
- using a bus where appropriate

---

## 6. ORTHOGONAL WIRING

Use horizontal and vertical wire segments.

Use 90-degree turns.

Avoid:
- diagonal wires
- arbitrary-angle wires
- curved signal wires

The schematic must resemble a clean traditional engineering schematic.

---

## 7. JUNCTION DOTS

Do NOT use junction-dot networks as a shortcut for poor schematic
organization.

A junction dot is allowed ONLY when nets genuinely require an electrical
connection.

Avoid crowded structures containing many junction dots when cleaner
placement, net labels, power symbols or buses can express the circuit.

Never create a junction merely for visual convenience.

---

## 8. BUS RULE

When FOUR OR MORE related signals travel together, a bus SHOULD be
considered when it improves readability.

Examples:
- DATA[0..7]
- address groups
- related parallel GPIO groups

Use proper bus entries and identifiable individual nets.

Do NOT create a fake bus from unrelated signals simply because four or more
wires exist.

For 1–3 related signals, clean direct wiring is normally preferred.

Example:

```text
ESP32-S3                         IMU
SDA  -------------------------- SDA
SCL  -------------------------- SCL
```

---

## 9. PARALLEL SIGNAL ROUTING

Signals belonging to the same interface should be routed cleanly and,
where practical, in parallel.

Examples:
- SDA / SCL
- TX / RX
- SPI signal group
- parallel data lines

Maintain consistent spacing.

Avoid unnecessary loops and unequal routing shapes.

---

## 10. MCU-CENTERED ORGANIZATION

ESP32-S3 is the primary logical controller.

The schematic should generally organize peripheral blocks around the MCU
according to connectivity.

Possible conceptual organization:

```text
                    4G / GNSS
                        |
                        |
MicroSD ----------- ESP32-S3 ----------- IMU
                        |
                 CANCEL / ALERT
                        |
                      POWER
```

This is a design principle, not an absolute coordinate requirement.

Choose positions that produce the cleanest schematic.

---

## 11. FUNCTIONAL BLOCKS

Clearly organize the schematic into functional blocks where applicable:

- KHỐI NGUỒN
- KHỐI XỬ LÝ TRUNG TÂM
- KHỐI CẢM BIẾN IMU
- KHỐI 4G / GNSS
- KHỐI LƯU TRỮ MICROSD
- KHỐI CẢNH BÁO
- KHỐI NÚT CANCEL
- KHỐI NGUỒN DỰ PHÒNG
- KHỐI LẬP TRÌNH / DEBUG

Use Vietnamese functional-block labels similar to the lecturer sample.

---

## 12. POWER NETS

Do not draw unnecessary long power wires across the schematic.

Use appropriate power symbols and named power nets such as:

+3V3
+5V
GND

and any project-specific supply rails.

Identically named power nets must represent the same electrical net.

---

## 13. DECOUPLING AND SUPPORT COMPONENTS

Decoupling capacitors and support components must remain visually associated
with the IC/module they support.

Do NOT move all capacitors into an unrelated corner merely to improve
appearance.

Electrical relationships must remain easy to understand.

---

## 14. TEXT AND WIRE OVERLAP

Never intentionally route wires through:

- symbol bodies
- component names
- references
- values
- pin numbers
- net labels
- block labels

All text must remain readable.

---

## 15. ALIGNMENT AND SPACING

Maintain consistent:

- component spacing
- wire spacing
- block spacing
- text sizing
- label placement
- power-symbol placement

Related components should align cleanly.

Avoid both excessive empty space and overcrowding.

---

## 16. CUSTOM SYMBOL POLICY

Do NOT blindly accept default KiCad symbol pin placement.

If a default symbol creates:

- messy wiring
- excessive crossings
- VCC/power pins in the lower region
- GND pins in the upper region or directly below VCC
- signals facing away from connected devices

create a PROJECT-LOCAL custom symbol.

Never modify global KiCad libraries for this purpose.

Custom symbols must preserve verified:

- pin numbers
- pin names/functions
- electrical pin types

---

## 17. ELECTRICAL CORRECTNESS OVERRIDES VISUAL STYLE

A beautiful schematic with incorrect electrical connections is INVALID.

Never:
- invent pins
- invent voltages
- invent component functions
- change real pin numbers for appearance
- copy electrical connections from the lecturer sample without verification

Official documentation overrides visual preferences whenever there is a
conflict.

---

## 18. KICAD FILE SAFETY

Before modifying a KiCad schematic:

1. Check for a .lck schematic lock file.
2. If the schematic is actively locked by KiCad, STOP.
3. Never delete an active lock file to force editing.
4. Create a backup before major modifications.
5. Do not modify the PCB unless the task explicitly requires PCB work.
6. Do not modify global KiCad libraries.

---

## 19. VALIDATION AFTER EVERY MAJOR SCHEMATIC CHANGE

Required workflow:

```text
Generate/edit .kicad_sch
        |
        v
Run KiCad ERC
        |
        v
Export PDF/SVG
        |
        v
Visually inspect
        |
        v
Fix layout/electrical issues
        |
        v
Validate again
```

Use the installed KiCad CLI:

`D:\Kicad\bin\kicad-cli.exe`

Do not declare success solely because the schematic file opens.

---

## 20. VISUAL QUALITY CHECKLIST

Before accepting a schematic, verify:

- [ ] Pins exit horizontally from LEFT or RIGHT only
- [ ] Positive power (VCC/VIN/3V3/5V) is located in the UPPER region of the symbol
- [ ] GND is located at the VERY BOTTOM of the symbol
- [ ] GND is NOT placed directly underneath VCC near the top
- [ ] GND defaults to lower RIGHT unless routing dictates otherwise
- [ ] Signal pins occupy the MIDDLE region of the symbol
- [ ] Related signal pins face each other
- [ ] No unnecessary diagonal wires
- [ ] No unnecessary wire crossings
- [ ] No wires through text or symbols
- [ ] No confusing junction-dot networks
- [ ] 4+ related signals use a bus when beneficial
- [ ] 1–3 signals use clean direct wiring when appropriate
- [ ] Related signal wires are parallel where practical
- [ ] Functional blocks are clearly identifiable
- [ ] MCU/peripheral placement is logical
- [ ] Power symbols/net labels are used cleanly
- [ ] Decoupling/support components remain associated with their devices
- [ ] Text is readable
- [ ] Spacing and alignment are consistent
- [ ] Overall visual style follows the lecturer sample

---

## 21. ELECTRICAL QUALITY CHECKLIST

Before accepting a production schematic, verify:

- [ ] Real part number is known
- [ ] Pin numbers verified from authoritative documentation
- [ ] Pin functions verified
- [ ] Supply voltage verified
- [ ] Logic voltage compatibility verified
- [ ] Required pull-ups/pull-downs verified
- [ ] Required decoupling verified
- [ ] Required protection circuitry verified
- [ ] Interface connections verified
- [ ] Required unused-pin handling verified
- [ ] ERC executed
- [ ] No unexplained critical ERC errors
- [ ] No invented electrical assumptions

---

## 22. DEFINITION OF PASS

A schematic passes ONLY when BOTH conditions are satisfied:

A. ELECTRICAL CORRECTNESS

AND

B. VISUAL / DRAWING QUALITY

ERC = 0 errors alone does NOT automatically mean PASS.

A visually clean schematic with incorrect pin mapping does NOT mean PASS.

The exported PDF/SVG must also be visually inspected before acceptance.

---

## 24. A4 PRESENTATION SCHEMATIC RULES

This section governs all PRESENTATION schematics intended for lecturer review, thesis defense, and presentation slides. It codifies the compact, bold, highly legible style derived from the lecturer's sample schematic.

### RULE A — PAGE SIZE
Presentation schematic MUST fit on exactly **ONE A4 Landscape page (297 mm x 210 mm)**. Do NOT use A3 or multiple sheets for presentation schematics. Everything must fit comfortably within the printable drawing frame.

### RULE B — COMPACT PRESENTATION
Eliminate all report-style explanatory paragraphs, long sentences, and redundant operational notes from the schematic canvas (e.g. descriptions of 15s countdowns, sensor ranges, or driver design rationale). Explanations belong in the project report. The schematic must communicate visually through clear symbols, short block titles, and direct wiring.

### RULE C — PIN NAMING
Use short, conventional, functional pin names on peripheral symbols:
- `SDA`, `SCL`, `INT`, `AD0`
- `CS`, `MOSI`, `MISO`, `SCK`
- `TX`, `RX`, `PPS`
- `PWRKEY`, `STATUS`
- `CANCEL`, `LED`, `BUZZER`
- `5V`, `3V3`, `VBAT`, `GND`

Avoid long, redundant names such as `I2C0_SDA`, `SPI_MOSI`, `MODEM_RXD`, or `BUZZER_CTRL` on peripheral symbols.

### RULE D — MCU GPIO DISPLAY
On the central MCU (ESP32-S3), display the concise hardware GPIO designator (e.g. `GPIO8`, `GPIO9`, `GPIO10`, `GPIO11`, `GPIO12`, `GPIO13`, `GPIO14`, `GPIO17`, `GPIO18`, `GPIO21`, `GPIO43`, `GPIO44`, `GPIO4`, `GPIO5`, `GPIO6`, `GPIO7`, `GPIO15`, `GPIO1`).
Peripheral pins display functional names (`SDA`, `TX`, `CS`). Direct wires connecting them require NO redundant duplicate labels.

### RULE E — DEVICE PIN ORIENTATION
All custom-symbol device pins MUST exit **HORIZONTALLY** from the LEFT or RIGHT sides. Never create pins exiting vertically through the top or bottom edges of IC/module boxes.

### RULE F — DEVICE POWER-PIN POSITION
On rectangular device/module symbols:
- Positive supply pins (`VCC`, `3V3`, `5V`, `VBAT`) must be located in the **upper region** of the Left or Right side.
- Ground pins (`GND`) must be located at the **very bottom** (lowest graphical position) of the Left or Right side.

### RULE G — POWER SYMBOL ORIENTATION
KiCad global/local power symbols connected to wires MUST follow a strict vertical orientation:
- **Positive power symbols** (`+3V3`, `5V_SYS`, `5V_USB`, `VBAT`) MUST point vertically **UP** (arrow/bar pointing upwards).
- **Ground symbols** (`GND`) MUST point vertically **DOWN** (bars pointing downwards).
- Never randomly rotate power symbols horizontally.
*(Critical distinction: Device pins exit horizontally; Power symbols point vertically).*

### RULE H — SIGNAL ROUTING
Prefer direct, straight **horizontal signal wires** between peripheral blocks and the central MCU. Connected pins should directly face each other whenever practical.

### RULE I — BENDS
Minimize wire bends:
- **0 bends** (straight horizontal line) is ideal.
- **1 or 2 orthogonal bends** (90-degree turns) are allowed when routing around blocks.
- **NEVER** use diagonal wires or non-orthogonal lines.

### RULE J — JUNCTIONS
Use junction dots **ONLY** where genuine electrical branching occurs (e.g. shared I2C bus taps, voltage dividers, power rail feeds). Never use junction dots for decoration or across crossing wires.

### RULE K — BUS
Use buses only when they materially improve readability (e.g., wide parallel buses). For standard 2-wire (I2C, UART) and 4-wire (SPI) interfaces, clean direct parallel orthogonal wiring is preferred.

### RULE L — PRINTABILITY
The presentation schematic MUST remain crisp, bold, and fully legible when printed on standard A4 paper in **black-and-white** on standard office printers. Text weights, line widths, and visual spacing must ensure effortless readability without relying on color differentiation.

### RULE M — VISUAL HIERARCHY
Establish clear visual precedence:
1. **PAGE / PROJECT TITLE**: Most prominent.
2. **FUNCTIONAL BLOCK TITLE**: Bold, distinct headers.
3. **COMPONENT NAME**: Clear, identifiable module labels.
4. **PIN NAME**: Concise, crisp functional labels.
5. **REFERENCE DESIGNATOR & VALUE**: Compact, legible labels.

### RULE N — LECTURER STYLE
For PRESENTATION schematics, the visual style of `D:\ĐỒ ÁN 2\Mẫu của thầy\Project sample schematic.PDF` is the controlling aesthetic reference (clean layout, bold block headers, compact academic title block, vertical power rails, high symbol density), while official datasheets and verified engineering decisions control electrical correctness.

### RULE O — CUSTOM SYMBOL PIN-TEXT CONTAINMENT
For every rectangular custom symbol:
- Pin names must be completely inside the symbol body.
- Pin names must never cross or touch the symbol border.
- Pin numbers must remain clearly separated from pin names.
- Power pin names such as VCC, 3V3, 5V and GND must follow the same containment rule.
- Device pins still exit horizontally LEFT/RIGHT.
- Positive power SYMBOLS point vertically UP.
- GND SYMBOLS point vertically DOWN.
- Electrical pin numbers/types/connectivity must never be changed merely to improve appearance.

### RULE P — PRESENTATION TITLE BLOCK
For lecturer-presentation schematics:
- Use the lecturer reference as the visual template for the title block.
- PROJECT is centered and visually dominant.
- ĐỀ TÀI, SVTH and GVHD are clearly separated.
- Student names and student IDs are column-aligned.
- Long project titles may use multiple lines.
- All text must remain inside the title-block cells with adequate padding.
- Title-block text must remain readable in A4 monochrome printing.
- Never invent student, supervisor, university or project metadata.
- Use only project information explicitly supplied by the user.

### RULE Q — WIRE VISIBILITY
Every electrical connection must be visually traceable.
Wires must not be hidden by:
- reference text
- value text
- component names
- block labels
Component text must be repositioned instead of allowing wire/text overlap.

### RULE R — DISCRETE COMPONENT TEXT CLEARANCE
Reference designators and values for R/C/D/Q/SW components must not overlap the graphical body of the component.
Maintain visible clearance between:
- symbol body
- reference
- value
- wire
- junction dot

### RULE S — LED POLARITY CHECK
For every LED:
Electrical polarity must be verified from actual KiCad pin numbers, not only from graphical appearance.
For an active-HIGH indicator connected to GPIO:
GPIO -> current-limiting resistor -> LED anode -> LED cathode -> GND
unless the documented circuit intentionally uses another topology.

### RULE T — PRESENTATION TITLE BLOCK COLOR
For this lecturer-presentation project:
The custom PROJECT title block uses a consistent dark-blue style matching the lecturer reference.
Border, dividers and title-block text use the same dark-blue visual family.
The rest of the schematic is NOT recolored merely to match the title block.

### RULE U — TITLE BLOCK TEXT CLEARANCE
No title-block text may touch:
- outer border
- divider line
- neighboring text
PROJECT must be centered vertically and horizontally in its row.
Long project titles should use the available cell area efficiently while retaining safe padding.
Student names must be bold and visually comparable in weight to the supervisor name.

### RULE V — DEDICATED SIGNAL LANES
For presentation schematics:
- Closely related GPIO circuits should use separate visual routing lanes whenever space permits.
- Avoid long signal wires crossing through unrelated functional circuits.
- Prefer moving local passive components slightly rather than routing a signal around multiple unrelated components.
- For parallel GPIO functions, prefer vertically stacked independent rows.
- Target zero signal-wire crossings inside each functional block.
- Electrical connectivity always has priority over appearance.

### RULE W — COMPLETE DEVICE / MODULE PIN REPRESENTATION
1. For lecturer-presentation schematics, every IC, development board, or module must display all VERIFIED physical/exposed pins whenever the exact hardware variant is known.
2. Used pins and unused pins must both remain visible.
3. Existing approved connections must remain unchanged when symbols are expanded.
4. Unused pins must remain electrically unconnected unless the hardware documentation explicitly requires otherwise.
5. Never add fake wires to unused pins.
6. Proper KiCad No Connect markers may be used when required for ERC.
7. Never invent pin names, numbers, electrical types, or connector positions.
8. Manufacturer/board documentation controls pinout correctness.
9. Lecturer reference controls visual style only.
10. For development boards, show all pins physically exposed on the board headers, not inaccessible internal IC package pads.
11. If the exact breakout/module revision cannot be identified, flag the module for hardware identification instead of fabricating a complete pinout.
12. Complete symbols must remain readable on A4.
13. Device pins normally exit horizontally LEFT/RIGHT.
14. Existing used-pin GPIO/net mapping is considered FROZEN unless the user explicitly requests an electrical redesign.

---

## 25. MANDATORY AI BEHAVIOR

Before EVERY future task that creates, edits, rearranges, reviews or expands
a schematic in this project:

1. Read this entire file first.
2. Read the lecturer sample when visual comparison is relevant.
3. Treat these rules as mandatory project requirements.
4. Do not silently ignore a rule.
5. If a rule conflicts with electrical correctness, electrical correctness
   wins and the conflict must be reported.
6. After work, explicitly report whether the schematic complies with this
   rule file.

END OF MANDATORY SCHEMATIC DRAWING RULES.
