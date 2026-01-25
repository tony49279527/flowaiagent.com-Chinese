import os
import re
from PIL import Image

BASE_DIR = r'c:\Users\sales-Tony\.gemini\antigravity\playground\vector-apogee'
IMAGES_DIR = os.path.join(BASE_DIR, 'images')

def convert_images():
    print("Converting images to WebP...")
    converted_count = 0
    
    if not os.path.exists(IMAGES_DIR):
        print(f"Images directory not found: {IMAGES_DIR}")
        return

    for filename in os.listdir(IMAGES_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(IMAGES_DIR, filename)
            webp_path = os.path.splitext(file_path)[0] + '.webp'
            
            # Skip if WebP already exists and is newer
            if os.path.exists(webp_path) and os.path.getmtime(webp_path) > os.path.getmtime(file_path):
                continue
                
            try:
                with Image.open(file_path) as img:
                    img.save(webp_path, 'WEBP', quality=80)
                    
                orig_size = os.path.getsize(file_path)
                webp_size = os.path.getsize(webp_path)
                reduction = (orig_size - webp_size) / orig_size * 100
                print(f"Converted {filename}: {orig_size/1024:.1f}KB -> {webp_size/1024:.1f}KB (-{reduction:.1f}%)")
                converted_count += 1
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")
                
    print(f"Image conversion complete. {converted_count} images processed.")

def update_html_references():
    print("Updating HTML references...")
    updated_files = 0
    
    for filename in os.listdir(BASE_DIR):
        if filename.endswith('.html'):
            file_path = os.path.join(BASE_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace .png/.jpg/.jpeg with .webp in src attributes
            # Pattern: src="images/name.png" -> src="images/name.webp"
            # We match strict path inside src to avoid false positives
            
            def replace_callback(match):
                full_match = match.group(0) # e.g. src="images/foo.png"
                ext = match.group(2) # .png
                
                # Check if the WebP file actually exists before replacing
                # Extract image filename from match
                # match.group(1) is the prefix path (images/) + name
                relative_path = match.group(1)
                image_filename = relative_path.split('/')[-1] # foo.png
                basename = os.path.splitext(image_filename)[0]
                webp_filename = basename + '.webp'
                
                # We assume images are in 'images' folder as per structure
                # But relative path might be complex. 
                # Let's just trust that we converted everything in images/ dir.
                # If the src points to "images/...", we replace extension.
                
                return full_match.replace(ext, '.webp')

            # Match .png or .jpg or .jpeg
            # We want to replace the extension with .webp
            # Group 1: Full relative path (images/foo.png)
            # Group 2: Extension WITHOUT dot (png)
            
            def replace_callback(match):
                full_match = match.group(0) # src="images/foo.png"
                ext_without_dot = match.group(2) # png
                
                # Verify we are replacing the extension at the end
                # replace matches all occurrences, so be careful.
                # simpler: Just use string slicing or re.sub inside
                
                return full_match.replace('.' + ext_without_dot, '.webp')

            # Regex: matches dot then extension. 
            new_content = re.sub(r'src=["\'](images/[^"\']+\.(png|jpg|jpeg))["\']', replace_callback, content, flags=re.IGNORECASE)
            
            # REPAIR STEP: Fix ..webp if any created by previous run
            new_content = new_content.replace('..webp', '.webp')

            # Add loading="lazy" logic (unchanged)... 
            def lazy_callback(match):
                img_tag = match.group(0)
                if 'loading=' in img_tag:
                    return img_tag
                if 'hero' in img_tag or 'logo' in img_tag: 
                    return img_tag
                return img_tag[:-1] + ' loading="lazy">'

            new_content = re.sub(r'<img[^>]+>', lazy_callback, new_content)

            if content != new_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_files += 1
                print(f"Updated {filename}")

    print(f"HTML update complete. {updated_files} files updated.")

if __name__ == "__main__":
    convert_images()
    update_html_references()
