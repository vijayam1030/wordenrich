#!/usr/bin/env python3
"""
Extract all words from enrichedpdfplan.txt and generate JavaScript data for games
"""

import re
import json
from pathlib import Path

def parse_word_entry(entry_text):
    """Parse a single word entry from the text."""
    lines = entry_text.strip().split('\n')
    
    word_data = {
        'word': '',
        'meaning': '',
        'synonyms': [],
        'antonyms': []
    }
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        if not line or re.match(r'^-{10,}$', line):
            continue
            
        if line.startswith('Word: '):
            word_line = line[6:]
            if ';' in word_line:
                word_data['word'], word_data['meaning'] = word_line.split(';', 1)
                word_data['word'] = word_data['word'].strip()
                word_data['meaning'] = word_data['meaning'].strip()
            else:
                word_data['word'] = word_line.strip()
        elif line.startswith('Meaning: '):
            word_data['meaning'] = line[9:].strip()
        elif line == 'Synonyms:':
            current_section = 'synonyms'
        elif line == 'Antonyms:':
            current_section = 'antonyms'
        elif line.startswith('Sentences:'):
            current_section = None  # Skip sentences for games
        elif line.startswith('Origin:'):
            current_section = None  # Skip origin for games
        elif line and current_section:
            clean_line = re.sub(r'^\d+\.\s*', '', line).strip()
            if clean_line and current_section in ['synonyms', 'antonyms']:
                word_data[current_section].append(clean_line)
    
    return word_data

def main():
    """Extract all words and create JavaScript data."""
    input_file = "enrichedpdfplan.txt"
    
    if not Path(input_file).exists():
        print(f"❌ Error: Input file '{input_file}' not found!")
        return
    
    print("🔍 Reading enriched word data...")
    
    # Read and parse the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split entries using flexible dash pattern
    entries = re.split(r'\n-{25,}\n', content)
    
    words_data = []
    print(f"📝 Processing {len(entries)} entries...")
    
    for i, entry in enumerate(entries):
        if entry.strip():
            try:
                word_data = parse_word_entry(entry)
                if word_data['word'] and word_data['meaning']:
                    # Clean up the data
                    word_data['word'] = word_data['word'].strip()
                    word_data['meaning'] = word_data['meaning'].strip()
                    word_data['synonyms'] = word_data['synonyms'][:5]  # Limit to 5
                    word_data['antonyms'] = word_data['antonyms'][:5]   # Limit to 5
                    words_data.append(word_data)
                    
                    if len(words_data) % 500 == 0:
                        print(f"✅ Processed {len(words_data)} words...")
                        
            except Exception as e:
                print(f"⚠️  Error processing entry {i}: {e}")
                continue
    
    print(f"🎯 Successfully extracted {len(words_data)} words!")
    
    # Generate JavaScript array
    js_data = json.dumps(words_data, indent=4)
    
    # Write to JavaScript file
    with open('game_words_data.js', 'w', encoding='utf-8') as f:
        f.write(f"// Generated word data from enrichedpdfplan.txt\n")
        f.write(f"// Total words: {len(words_data)}\n")
        f.write(f"const gameData = {js_data};\n")
        f.write(f"\n// Export for Node.js if needed\n")
        f.write(f"if (typeof module !== 'undefined' && module.exports) {{\n")
        f.write(f"    module.exports = gameData;\n")
        f.write(f"}}\n")
    
    print(f"📁 JavaScript data written to: game_words_data.js")
    print(f"🎮 Ready to use in your word games!")
    
    # Also create a sample for verification
    sample_words = words_data[:10]
    print(f"\n📋 Sample words:")
    for word in sample_words:
        print(f"  • {word['word']}: {word['meaning'][:50]}...")

if __name__ == "__main__":
    main()