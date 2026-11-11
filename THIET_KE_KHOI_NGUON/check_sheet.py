import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('build_complete_power_project.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print("--- Lines 620-650 ---")
for i in range(620, min(650, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')

print("\n--- Last 30 lines ---")
for i in range(max(0, len(lines)-30), len(lines)):
    print(f"{i+1}: {lines[i]}", end='')
