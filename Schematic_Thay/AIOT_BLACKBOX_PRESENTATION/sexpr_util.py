import re

def extract_sexprs(content, tag):
    idx = 0
    results = []
    pattern = tag
    while True:
        pos = content.find(pattern, idx)
        if pos == -1:
            break
        count = 0
        end = -1
        for i in range(pos, len(content)):
            if content[i] == '(':
                count += 1
            elif content[i] == ')':
                count -= 1
                if count == 0:
                    end = i + 1
                    break
        if end != -1:
            results.append((pos, end, content[pos:end]))
            idx = end
        else:
            idx = pos + 1
    return results
