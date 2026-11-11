import sys
sys.stdout.reconfigure(encoding='utf-8')
import build_complete_power_project as bp

print("Calling build_sheet2...")
bp.build_sheet2("02_CHARGER_BATTERY.kicad_sch")
print("Done.")
