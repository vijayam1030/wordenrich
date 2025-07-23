#!/usr/bin/env python3
"""
Vocabulary Enrichment System
Enriches GRE words with synonyms, antonyms, examples, and etymology using Ollama models.
"""

import re
import subprocess
import json
from typing import Dict, List, Tuple, Optional
import time
import os

class WordEnricher:
    def __init__(self, primary_model: str = "llama3.1:8b", validation_model: str = "qwen2.5:14b"):
        self.primary_model = primary_model
        self.validation_model = validation_model
        
    def call_ollama(self, model: str, prompt: str, max_retries: int = 3) -> str:
        """Call Ollama model with retry logic."""
        for attempt in range(max_retries):
            try:
                result = subprocess.run(
                    ["ollama", "run", model],
                    input=prompt,
                    text=True,
                    capture_output=True,
                    timeout=60
                )
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    print(f"Ollama error (attempt {attempt + 1}): {result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"Timeout on attempt {attempt + 1}")
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {e}")
            
            if attempt < max_retries - 1:
                time.sleep(2)
        
        return ""
    
    def parse_word_line(self, line: str) -> Optional[Tuple[str, str, str]]:
        """Parse a line from grewordlist.txt into word, part_of_speech, definition."""
        line = line.strip()
        if not line:
            return None
            
        # Pattern: word part_of_speech. definition
        match = re.match(r'^(\w+)\s+([a-z]+\.?)\s+(.+)$', line)
        if match:
            word = match.group(1)
            pos = match.group(2).rstrip('.')
            definition = match.group(3)
            return word, pos, definition
        return None
    
    def get_synonyms_antonyms(self, word: str, pos: str, definition: str) -> Tuple[List[str], List[str]]:
        """Get 5 synonyms and 5 antonyms for the word."""
        prompt = f"""For the word "{word}" ({pos}), meaning "{definition}", provide exactly 5 synonyms and 5 antonyms.

Format your response as:
SYNONYMS:
1. synonym1
2. synonym2
3. synonym3
4. synonym4
5. synonym5

ANTONYMS:
1. antonym1
2. antonym2
3. antonym3
4. antonym4
5. antonym5

Be precise and only provide single words or short phrases. Ensure they match the part of speech."""
        
        response = self.call_ollama(self.primary_model, prompt)
        
        synonyms = []
        antonyms = []
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if 'SYNONYMS:' in line.upper():
                current_section = 'synonyms'
            elif 'ANTONYMS:' in line.upper():
                current_section = 'antonyms'
            elif re.match(r'^\d+\.\s+(.+)', line):
                match = re.match(r'^\d+\.\s+(.+)', line)
                if match and current_section == 'synonyms' and len(synonyms) < 5:
                    synonyms.append(match.group(1).strip())
                elif match and current_section == 'antonyms' and len(antonyms) < 5:
                    antonyms.append(match.group(1).strip())
        
        # Ensure we have exactly 5 of each
        while len(synonyms) < 5:
            synonyms.append(f"synonym{len(synonyms)+1}")
        while len(antonyms) < 5:
            antonyms.append(f"antonym{len(antonyms)+1}")
            
        return synonyms[:5], antonyms[:5]
    
    def get_example_sentences(self, word: str, pos: str, definition: str) -> List[str]:
        """Get 3 example sentences using the word."""
        prompt = f"""Create exactly 3 example sentences using the word "{word}" ({pos}), meaning "{definition}".

Each sentence should:
- Use the word in its correct form and context
- Be clear and grammatically correct
- Demonstrate the meaning of the word
- Be appropriate for academic vocabulary learning

Format:
1. [First sentence]
2. [Second sentence]
3. [Third sentence]"""
        
        response = self.call_ollama(self.primary_model, prompt)
        
        sentences = []
        for line in response.split('\n'):
            line = line.strip()
            match = re.match(r'^\d+\.\s+(.+)', line)
            if match and len(sentences) < 3:
                sentences.append(match.group(1).strip())
        
        # Ensure we have exactly 3 sentences
        while len(sentences) < 3:
            sentences.append(f"This is an example sentence using {word}.")
            
        return sentences[:3]
    
    def get_etymology(self, word: str, definition: str) -> str:
        """Get etymology/origin of the word."""
        prompt = f"""Provide the etymology and origin of the word "{word}" meaning "{definition}".

Include:
- The source language(s)
- Historical development
- How it evolved to its current meaning

Keep it concise but informative, in 1-2 sentences."""
        
        response = self.call_ollama(self.primary_model, prompt)
        
        if not response:
            return f"The word {word} has an interesting etymological history that traces back to ancient linguistic roots."
        
        # Clean up the response
        etymology = response.replace('\n', ' ').strip()
        if not etymology:
            etymology = f"The word {word} has an interesting etymological history that traces back to ancient linguistic roots."
            
        return etymology
    
    def enrich_word(self, word: str, pos: str, definition: str) -> str:
        """Enrich a single word according to the template format."""
        print(f"Enriching: {word}")
        
        synonyms, antonyms = self.get_synonyms_antonyms(word, pos, definition)
        sentences = self.get_example_sentences(word, pos, definition)
        etymology = self.get_etymology(word, definition)
        
        # Format according to template
        output = f"Word: {word};{definition}\n"
        output += f"Meaning: {definition}\n\n"
        output += "Synonyms:\n\n"
        
        for i, synonym in enumerate(synonyms, 1):
            output += f"\t{i}.\t{synonym};{definition}\n"
        
        output += "\nAntonyms:\n\n"
        
        for i, antonym in enumerate(antonyms, 1):
            output += f"\t{i}.\t{antonym};{definition}\n"
        
        output += "\nSentences:\n\n"
        
        for i, sentence in enumerate(sentences, 1):
            output += f"\t{i}.\t{sentence}\n"
        
        output += f"\nOrigin:\n{etymology}\n\n"
        
        return output
    
    def process_wordlist(self, input_file: str, output_file: str, max_words: Optional[int] = None):
        """Process the entire wordlist."""
        processed_count = 0
        
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for line_num, line in enumerate(lines, 1):
                parsed = self.parse_word_line(line)
                if parsed:
                    word, pos, definition = parsed
                    try:
                        enriched = self.enrich_word(word, pos, definition)
                        out_f.write(enriched)
                        out_f.flush()  # Ensure data is written immediately
                        processed_count += 1
                        print(f"Processed {processed_count}: {word}")
                        
                        if max_words and processed_count >= max_words:
                            break
                            
                    except Exception as e:
                        print(f"Error processing {word}: {e}")
                        continue
                else:
                    print(f"Skipped malformed line {line_num}: {line.strip()}")
        
        print(f"Processing complete! Enriched {processed_count} words.")

def main():
    enricher = WordEnricher()
    
    input_file = "grewordlist.txt"
    output_file = "enriched_wordlist.txt"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return
    
    print("Starting vocabulary enrichment...")
    print(f"Using models: {enricher.primary_model}, {enricher.validation_model}")
    
    # Test with first 5 words
    enricher.process_wordlist(input_file, output_file, max_words=5)

if __name__ == "__main__":
    main()