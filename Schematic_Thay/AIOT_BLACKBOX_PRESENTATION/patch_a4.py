import subprocess
import re

# Update generate_a4_sch.py with the exact pin positions and run ERC
with open('generate_a4_sch.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's inspect custom_gnss_sym in generate_a4_sch.py
print("Checking custom_gnss_sym pin offsets...")
