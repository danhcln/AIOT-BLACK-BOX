with open('custom_symbols_def.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '(pin power_in line (at 15.24 -2.54 180) (length 2.54) (name "BOOT"'
replacement = '(pin passive line (at 15.24 -2.54 180) (length 2.54) (name "BOOT"'

if target in text:
    text = text.replace(target, replacement)
    with open('custom_symbols_def.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully replaced BOOT pin with passive line.")
else:
    print("Target string not found!")
