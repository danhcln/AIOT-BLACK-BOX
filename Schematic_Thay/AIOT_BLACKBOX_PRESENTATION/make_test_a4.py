import os

content = """(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "11111111-2222-3333-4444-555555555555")
\t(paper "A4")
\t(title_block
\t\t(title "TEST TITLE")
\t\t(date "2026-09-22")
\t\t(rev "1.0")
\t\t(company "TEST COMPANY")
\t\t(comment 1 "GVHD: TEST")
\t\t(comment 2 "SVTH: TEST")
\t)
)
"""
with open("test_a4.kicad_sch", "w", encoding="utf-8") as f:
    f.write(content)
print("Written test_a4.kicad_sch")
