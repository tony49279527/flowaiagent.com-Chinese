import re

# Read the styles.css file
with open('styles.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Read the modal styles to insert
with open('MODAL_STYLES_TO_INSERT.css', 'r', encoding='utf-8') as f:
    modal_styles = f.read()

# Find .user-name selector and insert after it
pattern = r'(\.user-name\s*\{[^}]*\})'
match = re.search(pattern, content)

if match:
    insert_position = match.end()
    
    # Insert modal styles after .user-name
    new_content = content[:insert_position] + '\n\n' + modal_styles + '\n' + content[insert_position:]
    
    # Write back to file
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print('✓ Success! Modal styles inserted after .user-name')
    print(f'✓ Inserted {len(modal_styles)} characters of Modal CSS')
else:
    print('✗ Error: Could not find .user-name selector')
