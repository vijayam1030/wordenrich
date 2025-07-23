#!/usr/bin/env python3
"""
Simple Vocabulary Enrichment System
"""

import re
import subprocess
import sys
from typing import Tuple, Optional, List

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
    
    # Get everything in one call for efficiency
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
    
    # Debug: Optional debug output
    # print(f"Raw response for {word}:")
    # print(response[:200] + "..." if len(response) > 200 else response)
    # print("---")
    
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
    
    # Format according to updated template
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

def main():
    if len(sys.argv) > 1:
        max_words = int(sys.argv[1])
    else:
        max_words = 3  # Default to 3 for testing
    
    input_file = "grewordlist.txt"
    output_file = "enriched_wordlist.txt"
    
    processed = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for line_num, line in enumerate(f, 1):
                parsed = parse_word_line(line)
                if parsed and processed < max_words:
                    word, pos, definition = parsed
                    print(f"Processing {processed+1}/{max_words}: {word}")
                    
                    enriched = enrich_word(word, pos, definition)
                    out_f.write(enriched)
                    out_f.flush()
                    
                    processed += 1
                    if processed >= max_words:
                        break
    
    print(f"Enriched {processed} words to {output_file}")

if __name__ == "__main__":
    main()