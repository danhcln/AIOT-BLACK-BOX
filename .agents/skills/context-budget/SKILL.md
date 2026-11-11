---
name: context-budget
description: Audits context window consumption across active skills, rules, and customizations. Invoked ONLY for explicit audits of context overhead; normal KiCad tasks must NOT automatically invoke this skill.
metadata:
  origin: ECC
---

# context-budget — Customization Context Audit

Context optimization skill adapted from ECC `skills/context-budget/SKILL.md` to ensure minimal token consumption.

## Invocation Policy
> [!IMPORTANT]
> **NORMAL AUTO-INVOCATION IS DISABLED.**
> - Do NOT invoke this skill during normal KiCad schematic engineering tasks.
> - Use ONLY when the user or agent explicitly requests an audit of agent customizations or context overhead.

## Core Principle
**Keep context small and relevant.**  
Do not load every tool or rule into every prompt. Skills should be loaded on-demand only when their specialized capability is required.

## Standard Invocation Guidelines per Task Type

1. **Normal schematic modifications**:
   `planner` → perform requested modification → `verification-loop`

2. **Schematic problems / ERC failures / incorrect nets**:
   `orch-fix-defect` → `verification-loop`

3. **Major revisions (e.g. REV8)**:
   `planner` → modification → `verification-loop` → `code-reviewer`

4. **Context / customization auditing only**:
   `context-budget` *(Explicit audit requests only)*

## How to Audit Context Overhead

### 1. Skill Inventory Check
- Verify that only the minimal, relevant subset of skills is installed in `.agents/skills/`.
- Verify each `SKILL.md` has concise frontmatter (`description` < 40 words) and stays under 250 lines.

### 2. Rule Files Check
- Check that rules in `.agents/rules/` are concise, high-signal, and contain no redundant prose.
- Ensure project rules (`SCHEMATIC_DRAWING_RULES.md`) remain authoritative.
