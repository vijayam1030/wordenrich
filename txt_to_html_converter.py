#!/usr/bin/env python3
"""
Convert enrichedpdfplan.txt to HTML format for PDF generation.
"""

import re
import html
from pathlib import Path

def parse_word_entry(entry_text):
    """Parse a single word entry from the text."""
    lines = entry_text.strip().split('\n')
    
    word_data = {
        'word': '',
        'meaning': '',
        'synonyms': [],
        'antonyms': [],
        'sentences': [],
        'origin': ''
    }
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and separator lines
        if not line or re.match(r'^-{10,}$', line):
            continue
            
        if line.startswith('Word: '):
            # Reset data for new word (in case of parsing errors)
            word_data = {
                'word': '',
                'meaning': '',
                'synonyms': [],
                'antonyms': [],
                'sentences': [],
                'origin': ''
            }
            current_section = None
            
            # Extract word and meaning from the first line
            word_line = line[6:]  # Remove "Word: "
            if ';' in word_line:
                word_data['word'], word_data['meaning'] = word_line.split(';', 1)
            else:
                word_data['word'] = word_line
        elif line.startswith('Meaning: '):
            word_data['meaning'] = line[9:]
        elif line == 'Synonyms:':
            current_section = 'synonyms'
        elif line == 'Antonyms:':
            current_section = 'antonyms'
        elif line == 'Sentences:':
            current_section = 'sentences'
        elif line.startswith('Origin:'):
            current_section = 'origin'
            if len(line) > 7:  # If there's content after "Origin:"
                word_data['origin'] = line[7:].strip()
        elif line and current_section:
            # Remove numbering and clean up the line
            clean_line = re.sub(r'^\d+\.\s*', '', line)
            clean_line = clean_line.strip()
            
            if current_section == 'origin':
                if word_data['origin']:
                    word_data['origin'] += ' ' + clean_line
                else:
                    word_data['origin'] = clean_line
            elif clean_line:
                word_data[current_section].append(clean_line)
    
    return word_data

def convert_to_html(input_file, output_file):
    """Convert the enriched word list to HTML format."""
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split entries by any line with 25+ consecutive dashes
    entries = re.split(r'\n-{25,}\n', content)
    
    # HTML template
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enriched Word Dictionary</title>
    <style>
        body {
            font-family: 'Georgia', serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }
        
        .word-entry {
            background: white;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            page-break-inside: avoid;
        }
        
        .word-title {
            font-size: 2.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        
        .meaning {
            font-size: 1.1em;
            color: #555;
            margin-bottom: 20px;
            font-style: italic;
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        
        .section-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-top: 25px;
            margin-bottom: 10px;
            border-bottom: 2px solid #bdc3c7;
            padding-bottom: 5px;
        }
        
        .synonyms, .antonyms {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }
        
        .synonym, .antonym {
            background-color: #e8f5e8;
            color: #27ae60;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            border: 1px solid #27ae60;
        }
        
        .antonym {
            background-color: #fdf2f2;
            color: #e74c3c;
            border: 1px solid #e74c3c;
        }
        
        .sentences {
            margin-bottom: 15px;
        }
        
        .sentence {
            background-color: #f8f9fa;
            padding: 12px;
            margin: 8px 0;
            border-radius: 5px;
            border-left: 3px solid #17a2b8;
            font-style: italic;
        }
        
        .origin {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
            font-size: 0.95em;
            color: #856404;
        }
        
        .toc {
            background: white;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .toc h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        
        .toc-list {
            columns: 3;
            column-gap: 20px;
            list-style: none;
            padding-left: 0;
        }
        
        .toc-item {
            break-inside: avoid;
            margin-bottom: 5px;
        }
        
        .toc-link {
            color: #3498db;
            text-decoration: none;
            font-size: 0.9em;
        }
        
        .toc-link:hover {
            text-decoration: underline;
        }
        
        @media print {
            body {
                background-color: white;
                font-size: 12pt;
            }
            
            .word-entry {
                box-shadow: none;
                border: 1px solid #ddd;
            }
        }
    </style>
</head>
<body>
    <h1 style="text-align: center; color: #2c3e50; font-size: 2.5em; margin-bottom: 30px;">📚 Enriched Word Dictionary</h1>
    
    <div class="toc">
        <h2>📋 Table of Contents</h2>
        <ul class="toc-list">
"""
    
    word_entries = []
    toc_items = []
    
    print(f"Processing {len(entries)} entries...")
    
    for i, entry in enumerate(entries):
        if entry.strip():
            try:
                word_data = parse_word_entry(entry)
                if word_data['word']:
                    word_entries.append(word_data)
                    # Create anchor-safe word ID
                    word_id = re.sub(r'[^a-zA-Z0-9]', '_', word_data['word'].lower())
                    toc_items.append(f'<li class="toc-item"><a href="#{word_id}" class="toc-link">{html.escape(word_data["word"])}</a></li>')
            except Exception as e:
                print(f"Error processing entry {i}: {e}")
                continue
    
    # Add TOC items
    html_content += '\n'.join(toc_items)
    html_content += """
        </ul>
    </div>
"""
    
    # Add word entries
    for word_data in word_entries:
        word_id = re.sub(r'[^a-zA-Z0-9]', '_', word_data['word'].lower())
        
        html_content += f"""
    <div class="word-entry" id="{word_id}">
        <div class="word-title">{html.escape(word_data['word'])}</div>
        
        <div class="meaning">{html.escape(word_data['meaning'])}</div>
"""
        
        if word_data['synonyms']:
            html_content += """
        <div class="section-title">🟢 Synonyms</div>
        <div class="synonyms">
"""
            for synonym in word_data['synonyms']:
                html_content += f'            <span class="synonym">{html.escape(synonym)}</span>\n'
            html_content += """        </div>
"""
        
        if word_data['antonyms']:
            html_content += """
        <div class="section-title">🔴 Antonyms</div>
        <div class="antonyms">
"""
            for antonym in word_data['antonyms']:
                html_content += f'            <span class="antonym">{html.escape(antonym)}</span>\n'
            html_content += """        </div>
"""
        
        if word_data['sentences']:
            html_content += """
        <div class="section-title">💬 Example Sentences</div>
        <div class="sentences">
"""
            for sentence in word_data['sentences']:
                html_content += f'            <div class="sentence">{html.escape(sentence)}</div>\n'
            html_content += """        </div>
"""
        
        if word_data['origin']:
            html_content += f"""
        <div class="section-title">📜 Origin</div>
        <div class="origin">{html.escape(word_data['origin'])}</div>
"""
        
        html_content += """    </div>
"""
    
    html_content += """
</body>
</html>"""
    
    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Conversion complete!")
    print(f"📁 Input file: {input_file}")
    print(f"📄 Output file: {output_file}")
    print(f"📊 Processed {len(word_entries)} word entries")

def main():
    """Main function to run the converter."""
    input_file = "enrichedpdfplan.txt"
    output_file = "enriched_words_dictionary.html"
    
    if not Path(input_file).exists():
        print(f"❌ Error: Input file '{input_file}' not found!")
        return
    
    print("🔄 Converting text file to HTML...")
    convert_to_html(input_file, output_file)
    
    print(f"\n📖 To convert to PDF, you can:")
    print(f"1. Open '{output_file}' in your browser and print to PDF")
    print(f"2. Use wkhtmltopdf: wkhtmltopdf {output_file} dictionary.pdf")
    print(f"3. Use Chrome headless: chrome --headless --print-to-pdf={output_file.replace('.html', '.pdf')} {output_file}")

if __name__ == "__main__":
    main()