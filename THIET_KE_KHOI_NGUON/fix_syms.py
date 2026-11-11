import re

with open('custom_symbols_def.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix DW01A Pin 5 and Pin 6 to passive
text = re.sub(r'\(pin power_in line \(at -12\.7 7\.62 0\) \(length 2\.54\) \(name "VCC"',
              '(pin passive line (at -12.7 7.62 0) (length 2.54) (name "VCC"', text)
text = re.sub(r'\(pin power_in line \(at -12\.7 -7\.62 0\) \(length 2\.54\) \(name "GND"',
              '(pin passive line (at -12.7 -7.62 0) (length 2.54) (name "GND"', text)

# Fix BQ25895 BTST Pin 21 to passive
text = re.sub(r'\(pin power_in line \(at 17\.78 0\.0 180\) \(length 2\.54\) \(name "BTST"',
              '(pin passive line (at 17.78 0.0 180) (length 2.54) (name "BTST"', text)

with open('custom_symbols_def.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated custom_symbols_def.py successfully.")
