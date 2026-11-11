import re, sys, subprocess

# Let's test KiCad ERC on a test schematic with various pin number styles
# Let's see how kicad-cli runs ERC on test schematic
test_cmd = [
    r'D:\KiCad\bin\kicad-cli.exe',
    'sch',
    'erc',
    '--severity-all',
    '--format', 'json',
    r'AIOT_BLACKBOX_PRESENTATION.kicad_sch'
]
res = subprocess.run(test_cmd, capture_output=True, text=True)
print("Current REV5 ERC exit code:", res.returncode)
print("Current REV5 ERC output:\n", res.stdout[:500])
