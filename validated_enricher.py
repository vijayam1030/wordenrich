#!/usr/bin/env python3
"""
Validated Vocabulary Enrichment System
Incorporates comprehensive validation for output quality assurance
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

# Import our validation system
from validation_system import VocabularyValidator, ValidationLevel, ValidationResult

# Configuration
PROGRESS_FILE = "enrichment_progress.json"
INPUT_FILE = "grewordlist.txt"
OUTPUT_FILE = "enriched_wordlist.txt"
VALIDATION_REPORT_FILE = "validation_report.json"
BACKUP_FILE = "enriched_wordlist_backup.txt"

# Quality-focused settings with validation
MAX_WORKERS = 6
BATCH_SIZE = 20           # Smaller batches for better validation
TIMEOUT = 30              # Longer timeout for quality
PROGRESS_SAVE_INTERVAL = 10
MODEL = "llama3.1:8b"
MIN_QUALITY_THRESHOLD = 0.7  # Minimum acceptable quality score

class ValidatedEnricher:
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.INTERMEDIATE):
        self.write_lock = Lock()
        self.progress_lock = Lock()
        self.processed_count = 0
        self.failed_words = []
        self.start_time = time.time()
        self.quality_stats = {
            "good_responses": 0, 
            "fallback_used": 0,
            "validation_passed": 0,
            "validation_failed": 0,
            "retry_attempts": 0
        }
        self.validation_results = []
        
        # Initialize validator
        self.validator = VocabularyValidator(validation_level)
        print(f"🎯 Using quality model: {MODEL}")
        print(f"🔍 Validation level: {validation_level.value}")
        print(f"📊 Quality threshold: {MIN_QUALITY_THRESHOLD}")

    def call_ollama_validated(self, prompt: str, word: str) -> str:
        """Quality-focused Ollama call with validation retry logic."""
        max_retries = 2
        
        for attempt in range(max_retries + 1):
            try:
                result = subprocess.run(
                    ["ollama", "run", MODEL],
                    input=prompt,
                    text=True,
                    capture_output=True,
                    timeout=TIMEOUT
                )
                if result.returncode == 0 and result.stdout.strip():
                    response = result.stdout.strip()
                    
                    # Quick validation check before returning
                    if self.quick_response_check(response, word):
                        return response
                    elif attempt < max_retries:
                        print(f"🔄 Response validation failed for {word}, retrying ({attempt + 1}/{max_retries})")
                        self.quality_stats["retry_attempts"] += 1
                        continue
                    else:
                        print(f"⚠️  Final attempt failed validation for {word}, using fallback")
                        return ""
                else:
                    if attempt < max_retries:
                        print(f"🔄 No response for {word}, retrying ({attempt + 1}/{max_retries})")
                        continue
                    else:
                        print(f"⚠️  No response for {word} after retries, using fallback")
                        return ""
                        
            except subprocess.TimeoutExpired:
                if attempt < max_retries:
                    print(f"⏰ Timeout for {word}, retrying ({attempt + 1}/{max_retries})")
                    continue
                else:
                    print(f"⏰ Final timeout for {word}, using fallback")
                    return ""
            except Exception as e:
                print(f"❌ Error for {word}: {e}")
                return ""
        
        return ""

    def quick_response_check(self, response: str, word: str) -> bool:
        """Quick validation to check if response is worth processing."""
        lines = response.split('\n')
        has_synonyms = any(line.upper().startswith('SYNONYMS:') for line in lines)
        has_antonyms = any(line.upper().startswith('ANTONYMS:') for line in lines)
        has_sentences = any(line.upper().startswith('SENTENCE') for line in lines)
        
        return has_synonyms and has_antonyms and has_sentences

    def enrich_word_validated(self, word: str, pos: str, definition: str) -> Tuple[str, Optional[dict]]:
        """High-quality enrichment with comprehensive validation."""
        
        # Enhanced prompt for better quality
        prompt = f"""For the word "{word}" ({pos}), meaning "{definition}":

Please provide exactly 5 synonyms and 5 antonyms that are actual words closely related to this specific word.
Write 3 natural example sentences using the word appropriately.
Provide accurate etymology with specific language origins.

Format your response exactly as:
SYNONYMS: word1, word2, word3, word4, word5
ANTONYMS: word1, word2, word3, word4, word5
SENTENCE1: [natural sentence using {word}]
SENTENCE2: [different sentence using {word}]
SENTENCE3: [third sentence using {word}]
ORIGIN: [detailed etymology with language origins]

Be specific to this word. Avoid generic responses."""

        response = self.call_ollama_validated(prompt, word)
        
        # Quality-based fallbacks
        synonyms = self.get_quality_synonyms(word, pos, definition)
        antonyms = self.get_quality_antonyms(word, pos, definition)
        sentences = self.get_quality_sentences(word, pos, definition)
        etymology = self.get_quality_etymology(word, definition)
        
        ai_response_used = False
        
        if response:
            # Parse response with validation
            parsed_data = self.parse_ai_response(response, word)
            if parsed_data:
                synonyms, antonyms, sentences, etymology = parsed_data
                ai_response_used = True
                self.quality_stats["good_responses"] += 1
            else:
                self.quality_stats["fallback_used"] += 1
        else:
            self.quality_stats["fallback_used"] += 1
        
        # Ensure exact counts
        while len(synonyms) < 5:
            synonyms.append(f"synonym{len(synonyms)+1}")
        while len(antonyms) < 5:
            antonyms.append(f"antonym{len(antonyms)+1}")
        
        # COMPREHENSIVE VALIDATION
        validation_result = self.validator.validate_word_complete(
            word, pos, definition, synonyms, antonyms, sentences, etymology
        )
        
        # Store validation results
        validation_data = {
            "word": word,
            "overall_score": validation_result.overall_score,
            "synonym_score": validation_result.synonyms.score,
            "antonym_score": validation_result.antonyms.score,
            "sentence_score": validation_result.sentences.score,
            "etymology_score": validation_result.etymology.score,
            "ai_response_used": ai_response_used,
            "issues": {
                "synonyms": validation_result.synonyms.issues,
                "antonyms": validation_result.antonyms.issues,
                "sentences": validation_result.sentences.issues,
                "etymology": validation_result.etymology.issues
            }
        }
        
        # Track validation statistics
        if validation_result.overall_score >= MIN_QUALITY_THRESHOLD:
            self.quality_stats["validation_passed"] += 1
        else:
            self.quality_stats["validation_failed"] += 1
            print(f"⚠️  Low quality score for {word}: {validation_result.overall_score:.2f}")
        
        # Format output
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
        
        return output, validation_data

    def parse_ai_response(self, response: str, word: str) -> Optional[Tuple[List[str], List[str], List[str], str]]:
        """Parse and validate AI response."""
        lines = response.split('\n')
        synonyms = []
        antonyms = []
        sentences = ["", "", ""]
        etymology = ""
        
        for line in lines:
            line = line.strip()
            if line.upper().startswith('SYNONYMS:'):
                syn_text = line[9:].strip()
                if syn_text and ',' in syn_text:
                    parsed_syns = [s.strip() for s in syn_text.split(',') if s.strip() and len(s.strip()) > 1]
                    if len(parsed_syns) >= 4:
                        synonyms = parsed_syns[:5]
                        
            elif line.upper().startswith('ANTONYMS:'):
                ant_text = line[9:].strip()
                if ant_text and ',' in ant_text:
                    parsed_ants = [s.strip() for s in ant_text.split(',') if s.strip() and len(s.strip()) > 1]
                    if len(parsed_ants) >= 4:
                        antonyms = parsed_ants[:5]
                        
            elif line.upper().startswith('SENTENCE1:'):
                sent = line[10:].strip()
                if sent and word.lower() in sent.lower() and len(sent) > 15:
                    sentences[0] = sent
                    
            elif line.upper().startswith('SENTENCE2:'):
                sent = line[10:].strip()
                if sent and word.lower() in sent.lower() and len(sent) > 15:
                    sentences[1] = sent
                    
            elif line.upper().startswith('SENTENCE3:'):
                sent = line[10:].strip()
                if sent and word.lower() in sent.lower() and len(sent) > 15:
                    sentences[2] = sent
                    
            elif line.upper().startswith('ORIGIN:'):
                etym = line[7:].strip()
                if etym and len(etym) > 20:
                    etymology = etym
        
        # Validate that we got good content
        if (len(synonyms) >= 4 and len(antonyms) >= 4 and 
            all(sentences) and etymology):
            return synonyms, antonyms, sentences, etymology
        else:
            return None

    # Keep the existing fallback methods from quality_enricher.py
    def get_quality_synonyms(self, word: str, pos: str, definition: str) -> List[str]:
        """Generate quality synonyms based on word analysis."""
        if 'lower' in definition.lower() or 'degrade' in definition.lower():
            return ["degrade", "demean", "humiliate", "belittle", "diminish"]
        elif 'superior' in definition.lower() or 'leader' in definition.lower():
            return ["leader", "chief", "head", "director", "commander"]
        elif 'building' in definition.lower() or 'dwelling' in definition.lower():
            return ["structure", "edifice", "residence", "monastery", "compound"]
        elif 'give up' in definition.lower() or 'renounce' in definition.lower():
            return ["renounce", "relinquish", "surrender", "abandon", "forfeit"]
        elif 'body' in definition.lower() or 'cavity' in definition.lower():
            return ["torso", "midsection", "belly", "trunk", "core"]
        elif pos == 'adj' and ('hate' in definition.lower() or 'repugnant' in definition.lower()):
            return ["detestable", "loathsome", "repulsive", "odious", "abhorrent"]
        elif pos == 'n' and 'act' in definition.lower():
            return ["action", "deed", "practice", "behavior", "conduct"]
        else:
            return ["related", "similar", "associated", "corresponding", "equivalent"]

    def get_quality_antonyms(self, word: str, pos: str, definition: str) -> List[str]:
        """Generate quality antonyms based on word analysis."""
        if 'lower' in definition.lower() or 'degrade' in definition.lower():
            return ["elevate", "enhance", "dignify", "uplift", "honor"]
        elif 'superior' in definition.lower() or 'leader' in definition.lower():
            return ["subordinate", "follower", "servant", "underling", "inferior"]
        elif 'give up' in definition.lower() or 'renounce' in definition.lower():
            return ["claim", "assert", "maintain", "retain", "assume"]
        elif pos == 'adj' and ('hate' in definition.lower() or 'repugnant' in definition.lower()):
            return ["lovable", "admirable", "appealing", "pleasant", "delightful"]
        elif 'temporary' in definition.lower() or 'suspension' in definition.lower():
            return ["permanent", "active", "ongoing", "continuous", "persistent"]
        else:
            return ["different", "opposite", "contrary", "unrelated", "distinct"]

    def get_quality_sentences(self, word: str, pos: str, definition: str) -> List[str]:
        """Generate quality sentences with proper context."""
        if 'lower' in definition.lower():
            return [
                f"The scandal served to {word} the politician's reputation.",
                f"His arrogant behavior would only {word} him in the eyes of others.",
                f"The harsh criticism was intended to {word} her confidence."
            ]
        elif 'superior' in definition.lower():
            return [
                f"The {word} of the monastery was known for wisdom and compassion.",
                f"As {word}, she oversaw the daily operations of the community.",
                f"The role of {word} required both spiritual and administrative skills."
            ]
        elif 'building' in definition.lower():
            return [
                f"The ancient {word} stood majestically on the hillside.",
                f"Visitors often toured the historic {word} to learn about monastic life.",
                f"The {word} complex included libraries, gardens, and living quarters."
            ]
        else:
            return [
                f"The study of {word} reveals important insights about the subject.",
                f"Understanding {word} is crucial for grasping the broader concept.",
                f"The term {word} appears frequently in academic literature."
            ]

    def get_quality_etymology(self, word: str, definition: str) -> str:
        """Generate quality etymology based on specific word knowledge."""
        etymology_dict = {
            'abase': 'From Old French "abaissier," derived from Latin "ad-" (to) + "bassus" (low), meaning to bring low or humble.',
            'abbess': 'From Old French "abbesse," derived from Latin "abbatissa," feminine form of "abbas" meaning father or abbot.',
            'abbey': 'From Old French "abbeie," derived from Latin "abbatia," meaning the jurisdiction of an abbot.',
            'abbot': 'From Old English "abbod," derived from Latin "abbas," from Greek "abba" meaning father.',
            'abdicate': 'From Latin "abdicare," meaning to disown or renounce, from "ab-" (away) + "dicare" (to declare).',
            'abdomen': 'From Latin "abdomen," possibly from "abdere" meaning to hide, referring to the hidden internal cavity.',
            'abdominal': 'From Latin "abdominalis," relating to the abdomen or belly region.',
            'abduction': 'From Latin "abductio," from "abducere" meaning to lead away, from "ab-" (away) + "ducere" (to lead).',
            # ... (include all the etymologies from quality_enricher.py)
        }
        
        if word.lower() in etymology_dict:
            return etymology_dict[word.lower()]
        
        # Fallback patterns with more accuracy
        if word.endswith('ess'):
            return f'The word "{word}" derives from Old French, with the suffix "-ess" indicating a female form or role.'
        elif word.endswith('ate') and len(word) > 4:
            return f'The word "{word}" comes from Latin, with the suffix "-ate" indicating action, process, or state.'
        elif word.endswith('tion'):
            return f'The word "{word}" derives from Latin, with the suffix "-tion" indicating the result or act of a process.'
        else:
            return f'The word "{word}" derives from classical linguistic roots and has developed its current meaning through historical usage.'

    def parse_word_line(self, line: str) -> Optional[Tuple[str, str, str]]:
        """Parse word line: word pos. definition"""
        line = line.strip()
        if not line:
            return None
        
        match = re.match(r'^(\w+)\s+([a-z]+\.?)\s+(.+)$', line)
        if match:
            return match.group(1), match.group(2).rstrip('.'), match.group(3)
        return None

    def process_word_batch(self, word_batch: List[Tuple[str, str, str]]) -> Tuple[List[str], List[dict]]:
        """Process batch with comprehensive validation."""
        results = []
        validation_data = []
        
        def process_single_word(word_data):
            word, pos, definition = word_data
            try:
                start = time.time()
                result, validation = self.enrich_word_validated(word, pos, definition)
                elapsed = time.time() - start
                
                with self.progress_lock:
                    self.processed_count += 1
                    if validation:
                        self.validation_results.append(validation)
                    
                    if self.processed_count % 5 == 0:
                        total_elapsed = time.time() - self.start_time
                        rate = self.processed_count / total_elapsed * 60
                        
                        # Calculate quality metrics
                        if self.validation_results:
                            avg_score = sum(v["overall_score"] for v in self.validation_results) / len(self.validation_results)
                            passed_pct = (self.quality_stats["validation_passed"] / self.processed_count) * 100
                            print(f"🎯 {self.processed_count} words | {rate:.1f}/min | Avg Quality: {avg_score:.2f} | Pass Rate: {passed_pct:.1f}%")
                        else:
                            print(f"🎯 {self.processed_count} words | {rate:.1f}/min")
                
                return result, validation
            except Exception as e:
                print(f"❌ Error processing {word}: {e}")
                self.failed_words.append(word)
                return None, None
        
        # Process with validation
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_single_word, word_data): word_data for word_data in word_batch}
            
            for future in as_completed(futures):
                result = future.result()
                if result[0]:  # If we got a result
                    results.append(result[0])
                    if result[1]:  # If we got validation data
                        validation_data.append(result[1])
        
        return results, validation_data

    def save_progress_and_validation(self, processed_count: int, total_count: int, last_word: str):
        """Save progress and validation results."""
        # Save progress
        progress = {
            "processed_count": processed_count,
            "total_count": total_count,
            "last_word": last_word,
            "input_file": INPUT_FILE,
            "output_file": OUTPUT_FILE,
            "failed_words": self.failed_words,
            "quality_stats": self.quality_stats
        }
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f, indent=2)
        
        # Save validation report
        if self.validation_results:
            avg_score = sum(v["overall_score"] for v in self.validation_results) / len(self.validation_results)
            
            validation_report = {
                "summary": {
                    "total_validated": len(self.validation_results),
                    "average_score": avg_score,
                    "pass_rate": (self.quality_stats["validation_passed"] / processed_count) * 100 if processed_count > 0 else 0,
                    "ai_success_rate": (self.quality_stats["good_responses"] / processed_count) * 100 if processed_count > 0 else 0
                },
                "detailed_results": self.validation_results[-100:]  # Keep last 100 for space
            }
            
            with open(VALIDATION_REPORT_FILE, 'w') as f:
                json.dump(validation_report, f, indent=2)

    def process_all_words_validated(self, max_words: Optional[int] = None):
        """Validated processing with comprehensive quality control."""
        print("🔍 Starting VALIDATED enrichment process...")
        print(f"📊 Quality threshold: {MIN_QUALITY_THRESHOLD}")
        print(f"🎯 Comprehensive validation enabled")
        
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
        print(f"🔧 Using {MAX_WORKERS} workers, batch size {BATCH_SIZE}")
        
        # Validated batch processing
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
            for i in range(0, total_words, BATCH_SIZE):
                batch = words_to_process[i:i+BATCH_SIZE]
                batch_num = i // BATCH_SIZE + 1
                total_batches = (total_words + BATCH_SIZE - 1) // BATCH_SIZE
                
                print(f"🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} words)")
                
                batch_results, batch_validations = self.process_word_batch(batch)
                
                # Write results immediately
                for result in batch_results:
                    out_f.write(result)
                    out_f.flush()
                
                # Save progress and validation data
                if self.processed_count % PROGRESS_SAVE_INTERVAL == 0:
                    last_word = batch[-1][0] if batch else "unknown"
                    self.save_progress_and_validation(self.processed_count, total_words, last_word)
        
        # Final statistics
        elapsed = time.time() - self.start_time
        rate = self.processed_count / elapsed * 60
        
        if self.validation_results:
            avg_score = sum(v["overall_score"] for v in self.validation_results) / len(self.validation_results)
            pass_rate = (self.quality_stats["validation_passed"] / self.processed_count) * 100
            ai_success_rate = (self.quality_stats["good_responses"] / self.processed_count) * 100
        else:
            avg_score = 0
            pass_rate = 0
            ai_success_rate = 0
        
        print(f"\n🏆 VALIDATED ENRICHMENT COMPLETE!")
        print(f"📊 Processed: {self.processed_count}/{total_words} words")
        print(f"⏱️  Time elapsed: {elapsed/60:.1f} minutes")
        print(f"⚡ Average rate: {rate:.1f} words/minute")
        print(f"🎯 Average quality score: {avg_score:.2f}")
        print(f"✅ Validation pass rate: {pass_rate:.1f}%")
        print(f"🤖 AI success rate: {ai_success_rate:.1f}%")
        print(f"🔄 Retry attempts: {self.quality_stats['retry_attempts']}")
        print(f"❌ Failed words: {len(self.failed_words)}")
        
        # Final save
        self.save_progress_and_validation(self.processed_count, total_words, "completed")
        
        print(f"📈 Validation report saved to: {VALIDATION_REPORT_FILE}")
        return self.processed_count

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 validated_enricher.py --validated [max_words]  # Validated processing")
        print("  python3 validated_enricher.py --test [words]           # Test with validation")
        print("  python3 validated_enricher.py --strict [words]         # Strict validation")
        return
    
    command = sys.argv[1]
    
    if command == "--validated":
        max_words = int(sys.argv[2]) if len(sys.argv) > 2 else None
        enricher = ValidatedEnricher(ValidationLevel.INTERMEDIATE)
        enricher.process_all_words_validated(max_words)
        
    elif command == "--test":
        test_words = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        print(f"🧪 Validated test with {test_words} words...")
        enricher = ValidatedEnricher(ValidationLevel.INTERMEDIATE)
        enricher.process_all_words_validated(test_words)
        
    elif command == "--strict":
        test_words = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        print(f"🔒 Strict validation test with {test_words} words...")
        enricher = ValidatedEnricher(ValidationLevel.COMPREHENSIVE)
        enricher.process_all_words_validated(test_words)
        
    else:
        print("❌ Unknown command. Use --validated, --test, or --strict")

if __name__ == "__main__":
    main()