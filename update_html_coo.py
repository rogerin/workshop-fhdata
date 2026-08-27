import json

with open('data_bundle.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Re-read build_html.py logic with updated COO question and detailed modeling
with open('build_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's inspect if we can make the HTML even richer with the COO question
print("Loaded build_html.py, length:", len(code))
