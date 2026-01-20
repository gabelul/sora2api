#!/usr/bin/env python3
"""
Chinese String Extractor for i18n Translation
Scans HTML files for Chinese text that needs translation
"""
import re
import os
from pathlib import Path
from html.parser import HTMLParser

class ChineseTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chinese_texts = []
        self.current_path = []
        self.skip_tags = {'script', 'style', 'code', 'pre'}
        self.in_skip_tag = 0
        
    def handle_starttag(self, tag, attrs):
        self.current_path.append(tag)
        if tag in self.skip_tags:
            self.in_skip_tag += 1
            
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.in_skip_tag -= 1
        if self.current_path and self.current_path[-1] == tag:
            self.current_path.pop()
            
    def handle_data(self, data):
        if self.in_skip_tag > 0:
            return
        text = data.strip()
        if text and re.search(r'[\u4e00-\u9fff]', text):
            path = '/'.join(self.current_path[-3:]) if len(self.current_path) >= 3 else '/'.join(self.current_path)
            self.chinese_texts.append({
                'text': text,
                'path': path
            })

def extract_chinese_from_html(html_content):
    """Extract Chinese text from HTML content"""
    parser = ChineseTextExtractor()
    try:
        parser.feed(html_content)
    except:
        pass
    
    # Also check for Chinese in attributes (placeholder, title, etc)
    attr_pattern = r'(?:placeholder|title|aria-label|alt)=["\']([^"\']*[\u4e00-\u9fff][^"\']*)["\']'
    for match in re.finditer(attr_pattern, html_content):
        parser.chinese_texts.append({
            'text': match.group(1),
            'path': 'attribute'
        })
    
    return parser.chinese_texts

def main():
    static_dir = Path(__file__).parent.parent / 'static'
    html_files = ['login.html', 'manage.html', 'generate.html']
    
    print("=" * 60)
    print("Chinese String Extractor for i18n Translation")
    print("=" * 60)
    print()
    
    all_strings = {}
    total_count = 0
    
    for filename in html_files:
        filepath = static_dir / filename
        if not filepath.exists():
            print(f"⚠️  {filename} not found")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chinese_texts = extract_chinese_from_html(content)
        print(f"📄 Scanning {filename}...")
        print(f"   Found {len(chinese_texts)} Chinese text fragments")
        
        for item in chinese_texts:
            text = item['text']
            if text not in all_strings:
                all_strings[text] = []
            all_strings[text].append({
                'file': filename,
                'path': item['path']
            })
        total_count += len(chinese_texts)
    
    print()
    if not all_strings:
        print("✅ No untranslated Chinese strings found!")
        return
        
    print(f"📝 Found {len(all_strings)} unique Chinese strings:")
    print("-" * 60)
    
    for i, (text, locations) in enumerate(list(all_strings.items())[:50], 1):
        display_text = text[:60] + "..." if len(text) > 60 else text
        loc = locations[0]
        print(f'{i:4}. "{display_text}"')
        print(f"      File: {loc['file']} | Path: {loc['path']}")
        print()
    
    if len(all_strings) > 50:
        print(f"... and {len(all_strings) - 50} more strings")
    
    print()
    print("-" * 60)
    print("To translate these strings:")
    print("  1. Add appropriate keys to static/locales/en.json")
    print("  2. Add data-i18n=\"key\" attributes to HTML elements")
    print("  3. The i18n.js loader will auto-translate on page load")
    print()

if __name__ == '__main__':
    main()
