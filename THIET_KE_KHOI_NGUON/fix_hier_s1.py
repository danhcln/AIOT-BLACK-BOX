import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    orig_len = len(text)
    
    # In Sheet 1
    if "01_INPUT_SELECTION" in filepath:
        # Move hierarchical label at 248.92 83.82 to 248.92 78.74
        text = text.replace('(at 248.92 83.82 0)', '(at 248.92 78.74 0)')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Fixed {filepath}")

fix_file("01_INPUT_SELECTION.kicad_sch")
