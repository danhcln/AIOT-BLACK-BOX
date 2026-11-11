import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Danh\.gemini\antigravity-ide\brain\445775bc-37f2-4804-b5f5-a5cc29ef88c2\.system_generated\steps\1908\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find tables
tables = re.findall(r'<table[^>]*>([\s\S]+?)</table>', text)
print(f"Total tables: {len(tables)}")

for i, t in enumerate(tables):
    rows = re.findall(r'<tr[^>]*>([\s\S]+?)</tr>', t)
    print(f"\n=== Table {i} ({len(rows)} rows) ===")
    for r in rows[:25]:
        cols = re.findall(r'<t[hd][^>]*>([\s\S]+?)</t[hd]>', r)
        cols_clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cols]
        print("  | ".join(cols_clean))
