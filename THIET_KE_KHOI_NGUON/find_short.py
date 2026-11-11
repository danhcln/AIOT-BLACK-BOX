# -*- coding: utf-8 -*-
import json

with open("erc_s2.json", "r", encoding="utf-8") as f:
    d = json.load(f)

for v in d['sheets'][0]['violations']:
    if 'multiple_net_names' in v.get('type', '') or 'pin_to_pin' in v.get('type', ''):
        print(v.get('type'), v.get('description'))
        for it in v.get('items', []):
            print("  ", it.get('description'), it.get('pos'))
