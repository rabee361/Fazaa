#!/usr/bin/env python
"""
Minify CSS, JavaScript, or HTML files and save to the root directory.
Usage: python minify.py path/to/file.css
"""

import os
import sys
import re
import argparse
from pathlib import Path
from csscompressor import compress as compress_css
from jsmin import jsmin
from htmlmin import minify as minify_html

def minify_file(file_path):
    """Minify a file based on its extension and save to root directory."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist.")
        return False
    
    # Get file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine file type and minify accordingly
    ext = file_path.suffix.lower()
    if ext == '.css':
        minified = compress_css(content)
    elif ext == '.js':
        minified = jsmin(content)
    elif ext == '.html':
        minified = minify_html(content, remove_comments=True, remove_empty_space=True)
    else:
        print(f"Error: Unsupported file type {ext}. Supported types: .css, .js, .html")
        return False
    
    # Create output filename (original_name.min.ext)
    output_name = f"{file_path.stem}.min{ext}"
    output_path = Path(os.getcwd()) / output_name
    
    # Save minified content
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(minified)
    
    print(f"Minified {file_path} -> {output_path}")
    print(f"Original size: {len(content):,} bytes")
    print(f"Minified size: {len(minified):,} bytes")
    print(f"Reduction: {(1 - len(minified)/len(content))*100:.2f}%")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Minify CSS, JS, or HTML files')
    parser.add_argument('file_path', help='Path to the file to minify')
    args = parser.parse_args()
    
    minify_file(args.file_path)

if __name__ == '__main__':
    main()