import re, os, shutil, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

# Source schematic
SRC = 'AIOT_BLACKBOX_PRESENTATION.kicad_sch'
TEST_DIR = 'scratch_rev5'
os.makedirs(TEST_DIR, exist_ok=True)
TEST_SCH = os.path.join(TEST_DIR, 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
shutil.copy(SRC, TEST_SCH)

# Also copy .kicad_pro, .kicad_wks, and sym-lib-table if any
for ext in ['.kicad_pro', '.kicad_prl']:
    f = 'AIOT_BLACKBOX_PRESENTATION' + ext
    if os.path.exists(f):
        shutil.copy(f, os.path.join(TEST_DIR, f))
for other in ['border_only.kicad_wks', 'sym-lib-table']:
    if os.path.exists(other):
        shutil.copy(other, os.path.join(TEST_DIR, other))

print("Copied files to test directory:", TEST_DIR)
