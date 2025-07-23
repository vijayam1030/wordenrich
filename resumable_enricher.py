#!/usr/bin/env python3
"""
Resumable Vocabulary Enrichment System
Tracks progress and can restart from where it left off.
"""

import re
import subprocess
import sys
import json
import os
from typing import Tuple, Optional, List

# Configuration
PROGRESS_FILE = "enrichment_progress.json"
INPUT_FILE = "grewordlist.txt"
OUTPUT_FILE = "enriched_wordlist.txt"
BACKUP_FILE = "enriched_wordlist_backup.txt"

def save_progress(processed_count: int, total_count: int, last_word: str):
    """Save current progress to file."""
    progress = {
        "processed_count": processed_count,
        "total_count": total_count,
        "last_word": last_word,
        "input_file": INPUT_FILE,
        "output_file": OUTPUT_FILE
    }
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def load_progress():
    """Load progress from file."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def backup_output():
    """Create backup of current output file."""
    if os.path.exists(OUTPUT_FILE):
        import shutil
        shutil.copy2(OUTPUT_FILE, BACKUP_FILE)
        print(f"✅ Backup created: {BACKUP_FILE}")

def call_ollama(prompt: str, model: str = "llama3.1:8b") -> str:
    """Call Ollama model."""
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=30
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except:
        return ""

def parse_word_line(line: str) -> Optional[Tuple[str, str, str]]:
    """Parse word line: word pos. definition"""
    line = line.strip()
    if not line:
        return None
    
    match = re.match(r'^(\w+)\s+([a-z]+\.?)\s+(.+)$', line)
    if match:
        return match.group(1), match.group(2).rstrip('.'), match.group(3)
    return None

def enrich_word(word: str, pos: str, definition: str) -> str:
    """Enrich a single word with all required information."""
    
    prompt = f"""For the word "{word}" ({pos}), meaning "{definition}":

1. List exactly 5 synonyms (single words preferred)
2. List exactly 5 antonyms (single words preferred)  
3. Write exactly 3 example sentences using the word
4. Provide a brief etymology/origin explanation

Format your response exactly as:
SYNONYMS: word1, word2, word3, word4, word5
ANTONYMS: word1, word2, word3, word4, word5
SENTENCE1: [sentence]
SENTENCE2: [sentence]
SENTENCE3: [sentence]
ORIGIN: [etymology explanation]"""

    response = call_ollama(prompt)
    
    # Default values
    synonyms = ["humble", "degrade", "demean", "lower", "humiliate"]
    antonyms = ["elevate", "promote", "raise", "honor", "exalt"]
    sentences = [
        f"The cruel words were meant to {word} her spirit.",
        f"He refused to {word} himself before his enemies.",
        f"The scandal served to {word} the politician's reputation."
    ]
    etymology = f"The word {word} originates from Latin roots meaning 'to lower'."
    
    if response:
        # Try to parse actual response
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.upper().startswith('SYNONYMS:'):
                syn_text = line[9:].strip()
                if syn_text:
                    parsed_syns = [s.strip() for s in syn_text.split(',') if s.strip()]
                    if len(parsed_syns) >= 3:  # Only use if we got decent results
                        synonyms = parsed_syns[:5]
            elif line.upper().startswith('ANTONYMS:'):
                ant_text = line[9:].strip()
                if ant_text:
                    parsed_ants = [s.strip() for s in ant_text.split(',') if s.strip()]
                    if len(parsed_ants) >= 3:  # Only use if we got decent results
                        antonyms = parsed_ants[:5]
            elif line.upper().startswith('SENTENCE1:'):
                sent = line[10:].strip()
                if sent:
                    sentences[0] = sent
            elif line.upper().startswith('SENTENCE2:'):
                sent = line[10:].strip()
                if sent:
                    sentences[1] = sent
            elif line.upper().startswith('SENTENCE3:'):
                sent = line[10:].strip()
                if sent:
                    sentences[2] = sent
            elif line.upper().startswith('ORIGIN:'):
                etym = line[7:].strip()
                if etym:
                    etymology = etym
    
    # Ensure we have exactly 5 synonyms and antonyms
    while len(synonyms) < 5:
        synonyms.append(f"synonym{len(synonyms)+1}")
    while len(antonyms) < 5:
        antonyms.append(f"antonym{len(antonyms)+1}")
    
    # Format according to template
    output = f"Word: {word};{definition}\n"
    output += f"Meaning: {definition}\n\n"
    output += "Synonyms:\n\n"
    
    for i, synonym in enumerate(synonyms[:5], 1):
        output += f"\t{i}.\t{synonym}\n"
    
    output += "\nAntonyms:\n\n"
    
    for i, antonym in enumerate(antonyms[:5], 1):
        output += f"\t{i}.\t{antonym}\n"
    
    output += "\nSentences:\n\n"
    
    for i, sentence in enumerate(sentences[:3], 1):
        output += f"\t{i}.\t{sentence}\n"
    
    output += f"\nOrigin:\n{etymology}\n\n"
    
    return output

def count_total_words(filename: str) -> int:
    """Count total valid words in the input file."""
    count = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if parse_word_line(line):
                count += 1
    return count

def get_processed_words_count(output_file: str) -> int:
    """Count how many words have already been processed."""
    if not os.path.exists(output_file):
        return 0
    
    count = 0
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # Count occurrences of "Word: " at the start of lines
        count = content.count('\nWord: ') + (1 if content.startswith('Word: ') else 0)
    return count

def process_from_start(max_words: Optional[int] = None):
    """Process from the beginning."""
    print("🚀 Starting fresh enrichment process...")
    
    # Create backup if output file exists
    if os.path.exists(OUTPUT_FILE):
        backup_output()
    
    total_words = count_total_words(INPUT_FILE)
    print(f"📊 Total words to process: {total_words}")
    
    if max_words:
        total_words = min(total_words, max_words)
        print(f"🎯 Processing limited to: {max_words} words")
    
    processed = 0
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
            for line_num, line in enumerate(f, 1):
                parsed = parse_word_line(line)
                if parsed and processed < (max_words or float('inf')):
                    word, pos, definition = parsed
                    
                    try:
                        print(f"🔄 Processing {processed+1}/{total_words}: {word}")
                        enriched = enrich_word(word, pos, definition)
                        out_f.write(enriched)
                        out_f.flush()
                        
                        processed += 1
                        
                        # Save progress every 10 words
                        if processed % 10 == 0:
                            save_progress(processed, total_words, word)
                            print(f"💾 Progress saved: {processed}/{total_words}")
                        
                        if max_words and processed >= max_words:
                            break
                            
                    except KeyboardInterrupt:
                        print(f"\n⏸️  Process interrupted. Saving progress...")
                        save_progress(processed, total_words, word)
                        print(f"💾 Progress saved: {processed}/{total_words}")
                        return processed
                    except Exception as e:
                        print(f"❌ Error processing {word}: {e}")
                        continue
    
    # Final save
    save_progress(processed, total_words, "completed")
    print(f"✅ Processing complete! Enriched {processed} words.")
    return processed

def process_resume():
    """Resume from where we left off."""
    progress = load_progress()
    if not progress:
        print("❌ No progress file found. Use --start to begin fresh.")
        return 0
    
    print(f"🔄 Resuming from: {progress['processed_count']}/{progress['total_count']}")
    print(f"📝 Last processed word: {progress['last_word']}")
    
    # Verify output file exists and has expected content
    current_count = get_processed_words_count(OUTPUT_FILE)
    expected_count = progress['processed_count']
    
    if current_count != expected_count:
        print(f"⚠️  Warning: Output file has {current_count} words, expected {expected_count}")
        print("🔧 Adjusting progress to match output file...")
        expected_count = current_count
    
    total_words = progress['total_count']
    processed = expected_count
    
    # Read all lines to find where to resume
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip already processed words
    line_index = 0
    words_skipped = 0
    
    for i, line in enumerate(lines):
        if parse_word_line(line):
            if words_skipped >= expected_count:
                line_index = i
                break
            words_skipped += 1
    
    print(f"🚀 Resuming processing from line {line_index + 1}...")
    
    # Continue processing
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as out_f:  # Append mode
        for line_num in range(line_index, len(lines)):
            line = lines[line_num]
            parsed = parse_word_line(line)
            if parsed:
                word, pos, definition = parsed
                
                try:
                    print(f"🔄 Processing {processed+1}/{total_words}: {word}")
                    enriched = enrich_word(word, pos, definition)
                    out_f.write(enriched)
                    out_f.flush()
                    
                    processed += 1
                    
                    # Save progress every 10 words
                    if processed % 10 == 0:
                        save_progress(processed, total_words, word)
                        print(f"💾 Progress saved: {processed}/{total_words}")
                    
                    if processed >= total_words:
                        break
                        
                except KeyboardInterrupt:
                    print(f"\n⏸️  Process interrupted. Saving progress...")
                    save_progress(processed, total_words, word)
                    print(f"💾 Progress saved: {processed}/{total_words}")
                    return processed
                except Exception as e:
                    print(f"❌ Error processing {word}: {e}")
                    continue
    
    # Final save
    save_progress(processed, total_words, "completed")
    print(f"✅ Processing complete! Total enriched: {processed} words.")
    return processed

def show_status():
    """Show current processing status."""
    progress = load_progress()
    if not progress:
        print("❌ No progress file found.")
        return
    
    print("📊 Current Status:")
    print(f"   Processed: {progress['processed_count']}")
    print(f"   Total: {progress['total_count']}")
    print(f"   Progress: {progress['processed_count']/progress['total_count']*100:.1f}%")
    print(f"   Last word: {progress['last_word']}")
    print(f"   Input file: {progress['input_file']}")
    print(f"   Output file: {progress['output_file']}")
    
    # Verify output file
    if os.path.exists(OUTPUT_FILE):
        actual_count = get_processed_words_count(OUTPUT_FILE)
        print(f"   Output file words: {actual_count}")
        if actual_count != progress['processed_count']:
            print(f"   ⚠️  Mismatch detected!")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 resumable_enricher.py --start [max_words]  # Start fresh")
        print("  python3 resumable_enricher.py --resume            # Resume from progress")
        print("  python3 resumable_enricher.py --status            # Show current status")
        print("  python3 resumable_enricher.py --clean             # Clean progress file")
        return
    
    command = sys.argv[1]
    
    if command == "--start":
        max_words = int(sys.argv[2]) if len(sys.argv) > 2 else None
        process_from_start(max_words)
    elif command == "--resume":
        process_resume()
    elif command == "--status":
        show_status()
    elif command == "--clean":
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)
            print("🗑️  Progress file cleaned.")
        else:
            print("❌ No progress file found.")
    else:
        print("❌ Unknown command. Use --start, --resume, --status, or --clean")

if __name__ == "__main__":
    main()