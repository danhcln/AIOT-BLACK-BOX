import json

with open(r'C:\Users\Danh\.gemini\antigravity\brain\129ea0c8-203e-468b-ad30-d772b9c45265\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if '"step_index": 548' in line or '"step_index":548' in line:
            obj = json.loads(line)
            for tc in obj.get('tool_calls', []):
                args = tc.get('arguments', {})
                for k in ['Content', 'CommandLine', 'Replacement']:
                    if k in args and len(args[k]) > 100:
                        with open(r'D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\render_base.py', 'w', encoding='utf-8') as out:
                            out.write(args[k])
                        print(f'Wrote {k} of length {len(args[k])} to render_base.py')

