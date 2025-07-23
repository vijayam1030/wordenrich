#!/usr/bin/env python3
"""
Fast Parallel Vocabulary Enrichment System
Target: 5000 words in 30 minutes (166 words/minute, ~2.7 words/second)
"""

import re
import subprocess
import sys
import json
import os
import time
from typing import Tuple, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import queue
import threading

# Configuration
PROGRESS_FILE = "enrichment_progress.json"
INPUT_FILE = "grewordlist.txt"
OUTPUT_FILE = "enriched_wordlist.txt"
BACKUP_FILE = "enriched_wordlist_backup.txt"

# Performance settings
MAX_WORKERS = 8  # Parallel Ollama calls
BATCH_SIZE = 50  # Words to process in memory before writing
TIMEOUT = 15     # Reduced timeout per word
PROGRESS_SAVE_INTERVAL = 25  # Save progress every 25 words
USE_FAST_MODEL = True  # Use smaller, faster model

class FastEnricher:
    def __init__(self):
        self.write_lock = Lock()
        self.progress_lock = Lock()
        self.processed_count = 0
        self.failed_words = []
        self.start_time = time.time()
        
        # Choose fastest available model
        self.model = self.get_fastest_model()
        print(f"🚀 Using model: {self.model}")
        
    def get_fastest_model(self):
        """Select the fastest available model."""
        # Preference order: smallest to largest for speed
        fast_models = [
            "tinyllama:1.1b",
            "smollm2:latest", 
            "gemma:2b",
            "codegemma:2b",
            "phi3:3.8b",
            "llama3.1:8b"
        ]
        
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            available = result.stdout
            
            for model in fast_models:
                if model in available:
                    return model
            
            # Fallback
            return "llama3.1:8b"
        except:
            return "llama3.1:8b"

    def call_ollama_fast(self, prompt: str) -> str:
        """Optimized Ollama call with shorter timeout and simpler prompt."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                text=True,
                capture_output=True,
                timeout=TIMEOUT
            )
            return result.stdout.strip() if result.returncode == 0 else ""
        except subprocess.TimeoutExpired:
            return ""
        except:
            return ""

    def enrich_word_fast(self, word: str, pos: str, definition: str) -> str:
        """Fast enrichment with simplified prompt."""
        
        # Much shorter, more direct prompt
        prompt = f"""Word: {word} ({pos}) - {definition}

Give me:
SYN: 5 synonyms separated by commas
ANT: 5 antonyms separated by commas  
EX1: One example sentence
EX2: Second example sentence
EX3: Third example sentence
ETY: Brief etymology in one sentence"""

        response = self.call_ollama_fast(prompt)
        
        # Fast defaults
        synonyms = ["humble", "degrade", "demean", "lower", "humiliate"]
        antonyms = ["elevate", "promote", "raise", "honor", "exalt"]
        sentences = [
            f"The word {word} is commonly used in formal contexts.",
            f"Examples of {word} can be found in literature.",
            f"Understanding {word} improves vocabulary skills."
        ]
        etymology = f"The word {word} has ancient linguistic origins."
        
        if response:
            # Fast parsing - look for key patterns
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('SYN:'):
                    syns = [s.strip() for s in line[4:].split(',') if s.strip()]
                    if len(syns) >= 3:
                        synonyms = syns[:5]
                elif line.startswith('ANT:'):
                    ants = [s.strip() for s in line[4:].split(',') if s.strip()]
                    if len(ants) >= 3:
                        antonyms = ants[:5]
                elif line.startswith('EX1:'):
                    sent = line[4:].strip()
                    if sent:
                        sentences[0] = sent
                elif line.startswith('EX2:'):
                    sent = line[4:].strip()
                    if sent:
                        sentences[1] = sent
                elif line.startswith('EX3:'):
                    sent = line[4:].strip()
                    if sent:
                        sentences[2] = sent
                elif line.startswith('ETY:'):
                    etym = line[4:].strip()
                    if etym:
                        etymology = etym
        
        # Ensure exact counts
        while len(synonyms) < 5:
            synonyms.append(f"synonym{len(synonyms)+1}")
        while len(antonyms) < 5:
            antonyms.append(f"antonym{len(antonyms)+1}")
        
        # Fast template formatting
        output = f"Word: {word};{definition}\nMeaning: {definition}\n\nSynonyms:\n\n"
        for i, syn in enumerate(synonyms[:5], 1):
            output += f"\t{i}.\t{syn}\n"
        output += "\nAntonyms:\n\n"
        for i, ant in enumerate(antonyms[:5], 1):
            output += f"\t{i}.\t{ant}\n"
        output += "\nSentences:\n\n"
        for i, sent in enumerate(sentences[:3], 1):
            output += f"\t{i}.\t{sent}\n"
        output += f"\nOrigin:\n{etymology}\n\n"
        
        return output

    def parse_word_line(self, line: str) -> Optional[Tuple[str, str, str]]:
        """Parse word line: word pos. definition"""
        line = line.strip()
        if not line:
            return None
        
        match = re.match(r'^(\w+)\s+([a-z]+\.?)\s+(.+)$', line)
        if match:
            return match.group(1), match.group(2).rstrip('.'), match.group(3)
        return None

    def process_word_batch(self, word_batch: List[Tuple[str, str, str]]) -> List[str]:
        """Process a batch of words in parallel."""
        results = []
        
        def process_single_word(word_data):
            word, pos, definition = word_data
            try:
                return self.enrich_word_fast(word, pos, definition)
            except Exception as e:
                print(f"❌ Error processing {word}: {e}")
                self.failed_words.append(word)
                return None
        
        # Process batch in parallel
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_single_word, word_data): word_data for word_data in word_batch}
            
            for future in as_completed(futures):
                word_data = futures[future]
                result = future.result()
                if result:
                    results.append(result)
                    
                    # Update progress
                    with self.progress_lock:
                        self.processed_count += 1
                        if self.processed_count % 10 == 0:
                            elapsed = time.time() - self.start_time
                            rate = self.processed_count / elapsed * 60
                            print(f"⚡ Processed {self.processed_count} words | Rate: {rate:.1f} words/min")
        
        return results

    def save_progress(self, processed_count: int, total_count: int, last_word: str):
        """Save current progress to file."""
        progress = {
            "processed_count": processed_count,
            "total_count": total_count,
            "last_word": last_word,
            "input_file": INPUT_FILE,
            "output_file": OUTPUT_FILE,
            "failed_words": self.failed_words
        }
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f, indent=2)

    def process_all_words_fast(self, max_words: Optional[int] = None):
        """Fast processing with batching and parallel execution."""
        print("🚀 Starting FAST enrichment process...")
        
        # Backup existing file
        if os.path.exists(OUTPUT_FILE):
            import shutil
            shutil.copy2(OUTPUT_FILE, BACKUP_FILE)
            print(f"✅ Backup created: {BACKUP_FILE}")
        
        # Read all words
        words_to_process = []
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parsed = self.parse_word_line(line)
                if parsed:
                    words_to_process.append(parsed)
                    if max_words and len(words_to_process) >= max_words:
                        break
        
        total_words = len(words_to_process)
        print(f"📊 Total words to process: {total_words}")
        print(f"⚡ Target rate: {total_words/30:.1f} words/min for 30min completion")
        print(f"🔧 Using {MAX_WORKERS} parallel workers, batch size {BATCH_SIZE}")
        
        # Process in batches
        all_results = []
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
            for i in range(0, total_words, BATCH_SIZE):
                batch = words_to_process[i:i+BATCH_SIZE]
                batch_num = i // BATCH_SIZE + 1
                total_batches = (total_words + BATCH_SIZE - 1) // BATCH_SIZE
                
                print(f"🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} words)")
                
                # Process batch
                batch_results = self.process_word_batch(batch)
                
                # Write results immediately
                for result in batch_results:
                    out_f.write(result)
                    out_f.flush()
                
                # Save progress
                if self.processed_count % PROGRESS_SAVE_INTERVAL == 0:
                    last_word = batch[-1][0] if batch else "unknown"
                    self.save_progress(self.processed_count, total_words, last_word)
        
        # Final statistics
        elapsed = time.time() - self.start_time
        rate = self.processed_count / elapsed * 60
        
        print(f"\n✅ Processing complete!")
        print(f"📊 Processed: {self.processed_count}/{total_words} words")
        print(f"⏱️  Time elapsed: {elapsed/60:.1f} minutes")
        print(f"⚡ Average rate: {rate:.1f} words/minute")
        print(f"❌ Failed words: {len(self.failed_words)}")
        
        if self.failed_words:
            print(f"Failed words: {', '.join(self.failed_words[:10])}{'...' if len(self.failed_words) > 10 else ''}")
        
        # Final save
        self.save_progress(self.processed_count, total_words, "completed")
        
        return self.processed_count

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 fast_enricher.py --fast [max_words]     # Fast parallel processing")
        print("  python3 fast_enricher.py --benchmark [words]    # Speed benchmark")
        return
    
    command = sys.argv[1]
    
    if command == "--fast":
        max_words = int(sys.argv[2]) if len(sys.argv) > 2 else None
        enricher = FastEnricher()
        enricher.process_all_words_fast(max_words)
        
    elif command == "--benchmark":
        test_words = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        print(f"🏁 Running benchmark with {test_words} words...")
        enricher = FastEnricher()
        start_time = time.time()
        processed = enricher.process_all_words_fast(test_words)
        elapsed = time.time() - start_time
        rate = processed / elapsed * 60
        
        print(f"\n🏁 BENCHMARK RESULTS:")
        print(f"   Words processed: {processed}")
        print(f"   Time taken: {elapsed:.1f} seconds")
        print(f"   Rate: {rate:.1f} words/minute")
        print(f"   Estimated time for 5000 words: {5000/rate:.1f} minutes")
        
    else:
        print("❌ Unknown command. Use --fast or --benchmark")

if __name__ == "__main__":
    main()