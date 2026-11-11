import subprocess

# We can test loading by calling kicad-cli sch export svg
with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Let's inspect what's in the file
for i, line in enumerate(lines[:30]):
    print(f"{i+1}: {line.rstrip()}")

# Let's check the bottom lines
print("--- BOTTOM LINES ---")
for i, line in enumerate(lines[-30:]):
    print(f"{len(lines)-30+i+1}: {line.rstrip()}")
