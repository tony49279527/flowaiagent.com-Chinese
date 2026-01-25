import os
import re

BASE_DIR = r'c:\Users\sales-Tony\.gemini\antigravity\playground\vector-apogee'

def fix_files():
    print("Scanning for corrupted tags...")
    fixed_count = 0
    
    for filename in os.listdir(BASE_DIR):
        if filename.endswith('.html'):
            file_path = os.path.join(BASE_DIR, filename)
            try:
                # Read as UTF-8. If it fails, try to read as binary and fix bytes?
                # The file is likely valid UTF-8, just containing '?' characters.
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                
                # Fix 1: Meta tags ending with ?> instead of ">
                # Regex: <meta [^>]+content="[^"]+\?>
                # Simpler: just replace '?>' with '">' if it looks like a meta tag end?
                # Or just replace '?>' with '">__QUOTE__' then handle?
                # Let's match the specific corruption pattern seen: content="...?>
                
                def fix_meta(match):
                    return match.group(0).replace('?>', '">')
                
                # Matches: content="...?> 
                # Be careful not to match valid '?>' (PHP?), but this is HTML.
                new_content = re.sub(r'content="[^"]+\?>', fix_meta, new_content)
                
                # Fix 2: Title tags ending with ?/title>
                new_content = new_content.replace('?/title>', '</title>')
                
                if content != new_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed {filename}")
                    fixed_count += 1
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"Fix complete. {fixed_count} files repaired.")

if __name__ == "__main__":
    fix_files()
