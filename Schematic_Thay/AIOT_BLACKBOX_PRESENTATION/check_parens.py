with open(r'scratch_rev6\AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

open_parens = text.count('(')
close_parens = text.count(')')
print(f"Open parens: {open_parens}, Close parens: {close_parens}")

# Find mismatched line
depth = 0
for line_no, line in enumerate(text.splitlines(), 1):
    depth += line.count('(') - line.count(')')
    if depth < 0:
        print(f"Negative depth at line {line_no}: {line}")
        break
print("Final depth:", depth)
