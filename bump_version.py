import os
import re

files_to_update = [
    'index.html', 'index_en.html',
    'create-analysis.html', 'create_en.html',
    'cases.html', 'cases_en.html',
    'blog.html', 'blog_en.html',
    'report.html', 'report_en.html',
    'payment.html', 'payment_en.html'
]

cwd = os.getcwd()

for filename in files_to_update:
    path = os.path.join(cwd, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace v2.6 with v2.7
        new_content = content.replace('v2.6', 'v2.7')
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename} to v2.7")
        else:
            print(f"No changes needed for {filename}")
    else:
        print(f"File not found: {filename}")
