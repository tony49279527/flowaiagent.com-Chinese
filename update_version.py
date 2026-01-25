import os
files_updated = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                new_content = content.replace('v2.1', 'v2.2')
                if content != new_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    files_updated.append(path)
            except Exception as e:
                print(f"Error processing {path}: {e}")
print(f"Updated {len(files_updated)} files: {files_updated}")
