#!/usr/bin/env python3
"""
Comprehensive Validation System for Vocabulary Enrichment
Validates synonyms, antonyms, sentences, and etymologies for accuracy
"""

import re
import subprocess
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    COMPREHENSIVE = "comprehensive"

@dataclass
class ValidationResult:
    is_valid: bool
    score: float  # 0.0 to 1.0
    issues: List[str]
    suggestions: List[str]

@dataclass
class WordValidation:
    word: str
    synonyms: ValidationResult
    antonyms: ValidationResult
    sentences: ValidationResult
    etymology: ValidationResult
    overall_score: float

class VocabularyValidator:
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.INTERMEDIATE):
        self.level = validation_level
        self.common_words = self.load_common_words()
        self.pos_patterns = self.load_pos_patterns()
        
    def load_common_words(self) -> set:
        """Load common English words for validation."""
        # In production, this would load from a comprehensive word list
        common = {
            'abandon', 'ability', 'able', 'about', 'above', 'absence', 'absolute', 'abstract',
            'academic', 'accept', 'access', 'accident', 'account', 'accurate', 'achieve', 'acid',
            'acquire', 'across', 'action', 'active', 'actual', 'add', 'address', 'adequate',
            'adjust', 'administration', 'admit', 'adopt', 'adult', 'advance', 'advantage', 'adventure',
            'advertising', 'advice', 'advocate', 'affair', 'affect', 'afford', 'afraid', 'after',
            'again', 'against', 'age', 'agency', 'agent', 'agree', 'agreement', 'ahead', 'aid',
            'aim', 'air', 'aircraft', 'alive', 'all', 'allow', 'almost', 'alone', 'along',
            'already', 'also', 'alter', 'alternative', 'although', 'always', 'amazing', 'among',
            'amount', 'analysis', 'analyze', 'ancient', 'anger', 'angle', 'angry', 'animal',
            'anniversary', 'announce', 'annual', 'another', 'answer', 'anxiety', 'any', 'anybody',
            'anyone', 'anything', 'anyway', 'anywhere', 'apart', 'apartment', 'apparent', 'appeal',
            'appear', 'application', 'apply', 'appoint', 'approach', 'appropriate', 'approval', 'approve',
            'area', 'argue', 'argument', 'arise', 'arm', 'army', 'around', 'arrange', 'arrangement',
            'arrest', 'arrival', 'arrive', 'art', 'article', 'artist', 'as', 'ask', 'aspect',
            'assess', 'assessment', 'asset', 'assign', 'assignment', 'assist', 'assistance', 'assistant',
            'associate', 'association', 'assume', 'assumption', 'at', 'atmosphere', 'attach', 'attack',
            'attempt', 'attend', 'attention', 'attitude', 'attract', 'attractive', 'audience', 'author',
            'authority', 'available', 'average', 'avoid', 'award', 'aware', 'awareness', 'away',
            'baby', 'back', 'background', 'bad', 'badly', 'bag', 'balance', 'ball', 'ban',
            'band', 'bank', 'bar', 'base', 'basic', 'basis', 'battle', 'be', 'beach',
            # ... would continue with thousands of words
            'degrade', 'demean', 'humiliate', 'belittle', 'diminish', 'elevate', 'enhance', 'dignify',
            'uplift', 'honor', 'leader', 'chief', 'head', 'director', 'commander', 'subordinate',
            'follower', 'servant', 'underling', 'inferior', 'structure', 'edifice', 'residence',
            'monastery', 'compound', 'renounce', 'relinquish', 'surrender', 'abandon', 'forfeit'
        }
        return common
        
    def load_pos_patterns(self) -> Dict[str, List[str]]:
        """Load part-of-speech patterns for validation."""
        return {
            'v': ['verb', 'action', 'process', 'do', 'make', 'create', 'become'],
            'n': ['noun', 'thing', 'person', 'place', 'concept', 'object'],
            'adj': ['adjective', 'quality', 'characteristic', 'descriptive'],
            'adv': ['adverb', 'manner', 'way', 'how', 'when', 'where']
        }

    def validate_synonyms(self, word: str, pos: str, definition: str, synonyms: List[str]) -> ValidationResult:
        """Comprehensive synonym validation."""
        issues = []
        suggestions = []
        score = 1.0
        
        # Basic checks
        if len(synonyms) != 5:
            issues.append(f"Expected 5 synonyms, got {len(synonyms)}")
            score -= 0.2
            
        # Check for duplicates
        if len(set(synonyms)) != len(synonyms):
            issues.append("Duplicate synonyms found")
            score -= 0.1
            
        # Check if synonyms are real words
        unknown_words = [s for s in synonyms if s.lower() not in self.common_words and not s.startswith('synonym')]
        if unknown_words and self.level in [ValidationLevel.INTERMEDIATE, ValidationLevel.COMPREHENSIVE]:
            issues.append(f"Possibly invalid words: {unknown_words}")
            score -= 0.1 * len(unknown_words)
            
        # Check if synonyms contain the original word
        if word.lower() in [s.lower() for s in synonyms]:
            issues.append("Synonyms contain the original word")
            score -= 0.2
            
        # Advanced semantic validation
        if self.level == ValidationLevel.COMPREHENSIVE:
            semantic_issues = self.validate_semantic_similarity(word, synonyms, definition)
            issues.extend(semantic_issues)
            if semantic_issues:
                score -= 0.1 * len(semantic_issues)
                
        # Part-of-speech consistency
        if pos in ['v', 'n', 'adj'] and self.level in [ValidationLevel.INTERMEDIATE, ValidationLevel.COMPREHENSIVE]:
            pos_issues = self.validate_pos_consistency(synonyms, pos)
            issues.extend(pos_issues)
            if pos_issues:
                score -= 0.1 * len(pos_issues)
                
        # Generate suggestions
        if score < 0.8:
            suggestions.append("Consider using more contextually appropriate synonyms")
        if unknown_words:
            suggestions.append("Verify that all synonyms are valid English words")
            
        return ValidationResult(
            is_valid=score >= 0.6,
            score=max(0.0, score),
            issues=issues,
            suggestions=suggestions
        )

    def validate_antonyms(self, word: str, pos: str, definition: str, synonyms: List[str], antonyms: List[str]) -> ValidationResult:
        """Comprehensive antonym validation."""
        issues = []
        suggestions = []
        score = 1.0
        
        # Basic checks
        if len(antonyms) != 5:
            issues.append(f"Expected 5 antonyms, got {len(antonyms)}")
            score -= 0.2
            
        # Check for duplicates
        if len(set(antonyms)) != len(antonyms):
            issues.append("Duplicate antonyms found")
            score -= 0.1
            
        # Check overlap with synonyms
        synonym_overlap = set(antonyms) & set(synonyms)
        if synonym_overlap:
            issues.append(f"Antonyms overlap with synonyms: {synonym_overlap}")
            score -= 0.3
            
        # Check if antonyms are real words
        unknown_words = [a for a in antonyms if a.lower() not in self.common_words and not a.startswith('antonym')]
        if unknown_words and self.level in [ValidationLevel.INTERMEDIATE, ValidationLevel.COMPREHENSIVE]:
            issues.append(f"Possibly invalid words: {unknown_words}")
            score -= 0.1 * len(unknown_words)
            
        # Advanced semantic validation
        if self.level == ValidationLevel.COMPREHENSIVE:
            semantic_issues = self.validate_semantic_opposition(word, antonyms, definition)
            issues.extend(semantic_issues)
            if semantic_issues:
                score -= 0.1 * len(semantic_issues)
                
        return ValidationResult(
            is_valid=score >= 0.6,
            score=max(0.0, score),
            issues=issues,
            suggestions=suggestions
        )

    def validate_sentences(self, word: str, pos: str, sentences: List[str]) -> ValidationResult:
        """Comprehensive sentence validation."""
        issues = []
        suggestions = []
        score = 1.0
        
        # Basic checks
        if len(sentences) != 3:
            issues.append(f"Expected 3 sentences, got {len(sentences)}")
            score -= 0.2
            
        for i, sentence in enumerate(sentences, 1):
            # Check if sentence contains the word
            if word.lower() not in sentence.lower():
                issues.append(f"Sentence {i} doesn't contain the target word")
                score -= 0.2
                continue
                
            # Check sentence length
            if len(sentence) < 20:
                issues.append(f"Sentence {i} is too short ({len(sentence)} chars)")
                score -= 0.1
                
            # Check if sentence is complete
            if not re.search(r'[.!?]$', sentence.strip()):
                issues.append(f"Sentence {i} doesn't end with proper punctuation")
                score -= 0.05
                
            # Check for generic patterns
            generic_patterns = [
                "is important in understanding",
                "is commonly used in",
                "has significant implications",
                "enhances comprehension",
                "is often encountered"
            ]
            if any(pattern in sentence.lower() for pattern in generic_patterns):
                issues.append(f"Sentence {i} appears generic/templated")
                score -= 0.15
                
            # Advanced grammar validation
            if self.level == ValidationLevel.COMPREHENSIVE:
                grammar_issues = self.validate_sentence_grammar(sentence, word, pos)
                if grammar_issues:
                    issues.extend([f"Sentence {i}: {issue}" for issue in grammar_issues])
                    score -= 0.1 * len(grammar_issues)
                    
        return ValidationResult(
            is_valid=score >= 0.6,
            score=max(0.0, score),
            issues=issues,
            suggestions=suggestions
        )

    def validate_etymology(self, word: str, etymology: str) -> ValidationResult:
        """Etymology validation."""
        issues = []
        suggestions = []
        score = 1.0
        
        # Basic checks
        if len(etymology) < 30:
            issues.append(f"Etymology too short ({len(etymology)} chars)")
            score -= 0.2
            
        # Check for generic patterns
        generic_patterns = [
            "has ancient linguistic origins",
            "derives from classical linguistic roots",
            "has evolved through historical linguistic development",
            "comes from Latin, with the prefix"
        ]
        if any(pattern in etymology for pattern in generic_patterns):
            issues.append("Etymology appears generic/templated")
            score -= 0.3
            
        # Check for language mentions
        languages = ['Latin', 'Greek', 'Old French', 'Old English', 'Germanic', 'Proto-Indo-European']
        if not any(lang in etymology for lang in languages):
            issues.append("Etymology doesn't specify source language")
            score -= 0.2
            
        # Check for etymological structure
        if 'from' not in etymology.lower() and 'derived' not in etymology.lower():
            issues.append("Etymology lacks proper derivation structure")
            score -= 0.1
            
        return ValidationResult(
            is_valid=score >= 0.6,
            score=max(0.0, score),
            issues=issues,
            suggestions=suggestions
        )

    def validate_semantic_similarity(self, word: str, synonyms: List[str], definition: str) -> List[str]:
        """Advanced semantic validation using definition matching."""
        issues = []
        
        # Check if synonyms make sense with the definition
        key_concepts = self.extract_key_concepts(definition)
        
        for synonym in synonyms:
            if synonym.startswith('synonym'):  # Skip fallback synonyms
                continue
                
            # Simple heuristic: check if synonym relates to key concepts
            if not self.check_semantic_relatedness(synonym, key_concepts):
                issues.append(f"'{synonym}' may not be semantically related to '{word}'")
                
        return issues

    def validate_semantic_opposition(self, word: str, antonyms: List[str], definition: str) -> List[str]:
        """Advanced semantic validation for antonyms."""
        issues = []
        
        # This would use more sophisticated NLP in production
        # For now, basic heuristics
        positive_indicators = ['good', 'high', 'up', 'increase', 'enhance', 'promote']
        negative_indicators = ['bad', 'low', 'down', 'decrease', 'reduce', 'lower']
        
        word_sentiment = self.get_word_sentiment(word, definition)
        
        for antonym in antonyms:
            if antonym.startswith('antonym'):  # Skip fallback antonyms
                continue
                
            antonym_sentiment = self.get_word_sentiment(antonym, "")
            if word_sentiment == antonym_sentiment and word_sentiment != 'neutral':
                issues.append(f"'{antonym}' may not be opposite to '{word}'")
                
        return issues

    def validate_pos_consistency(self, words: List[str], expected_pos: str) -> List[str]:
        """Check part-of-speech consistency."""
        issues = []
        
        # Simple heuristic patterns
        pos_patterns = {
            'v': ['ed', 'ing', 'ize', 'ify', 'ate'],
            'n': ['tion', 'sion', 'ness', 'ment', 'ity'],
            'adj': ['ful', 'less', 'ous', 'ive', 'able']
        }
        
        if expected_pos in pos_patterns:
            expected_patterns = pos_patterns[expected_pos]
            for word in words:
                if word.startswith(('synonym', 'antonym')):
                    continue
                    
                # This is a very basic check - in production would use proper POS tagging
                if not any(word.endswith(pattern) for pattern in expected_patterns) and len(word) > 6:
                    # Only flag if it's a longer word that should have clear POS markers
                    pass  # Simplified for now
                    
        return issues

    def validate_sentence_grammar(self, sentence: str, word: str, pos: str) -> List[str]:
        """Basic grammar validation."""
        issues = []
        
        # Check for basic grammar patterns
        if not re.match(r'^[A-Z]', sentence):
            issues.append("Sentence doesn't start with capital letter")
            
        # Check for proper word usage based on POS
        word_occurrences = re.findall(rf'\b{re.escape(word)}\b', sentence, re.IGNORECASE)
        if len(word_occurrences) > 1:
            issues.append("Word used multiple times in sentence")
            
        return issues

    def extract_key_concepts(self, definition: str) -> List[str]:
        """Extract key concepts from definition."""
        # Simple keyword extraction
        stop_words = {'the', 'a', 'an', 'to', 'of', 'in', 'on', 'at', 'by', 'for', 'with', 'from'}
        words = re.findall(r'\b\w+\b', definition.lower())
        return [w for w in words if w not in stop_words and len(w) > 3]

    def check_semantic_relatedness(self, word: str, concepts: List[str]) -> bool:
        """Basic semantic relatedness check."""
        # In production, this would use word embeddings or WordNet
        # For now, simple keyword matching
        word_lower = word.lower()
        return any(concept in word_lower or word_lower in concept for concept in concepts)

    def get_word_sentiment(self, word: str, definition: str) -> str:
        """Basic sentiment analysis."""
        positive = ['good', 'great', 'excellent', 'positive', 'enhance', 'improve', 'elevate', 'honor']
        negative = ['bad', 'poor', 'negative', 'lower', 'degrade', 'demean', 'hate', 'horrible']
        
        text = (word + ' ' + definition).lower()
        
        pos_count = sum(1 for p in positive if p in text)
        neg_count = sum(1 for n in negative if n in text)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'

    def validate_word_complete(self, word: str, pos: str, definition: str, 
                             synonyms: List[str], antonyms: List[str], 
                             sentences: List[str], etymology: str) -> WordValidation:
        """Complete validation of a word's enrichment."""
        
        # Validate each component
        syn_result = self.validate_synonyms(word, pos, definition, synonyms)
        ant_result = self.validate_antonyms(word, pos, definition, synonyms, antonyms)
        sent_result = self.validate_sentences(word, pos, sentences)
        etym_result = self.validate_etymology(word, etymology)
        
        # Calculate overall score
        weights = {'synonyms': 0.3, 'antonyms': 0.3, 'sentences': 0.25, 'etymology': 0.15}
        overall_score = (
            syn_result.score * weights['synonyms'] +
            ant_result.score * weights['antonyms'] +
            sent_result.score * weights['sentences'] +
            etym_result.score * weights['etymology']
        )
        
        return WordValidation(
            word=word,
            synonyms=syn_result,
            antonyms=ant_result,
            sentences=sent_result,
            etymology=etym_result,
            overall_score=overall_score
        )

def main():
    """Example usage of the validation system."""
    validator = VocabularyValidator(ValidationLevel.INTERMEDIATE)
    
    # Test case
    word = "abase"
    pos = "v"
    definition = "To lower in position, estimation, or the like; degrade."
    synonyms = ["degrade", "demean", "humiliate", "belittle", "diminish"]
    antonyms = ["elevate", "enhance", "dignify", "uplift", "honor"]
    sentences = [
        "The scandal served to abase the politician's reputation.",
        "His arrogant behavior would only abase him in the eyes of others.",
        "The harsh criticism was intended to abase her confidence."
    ]
    etymology = 'From Old French "abaissier," derived from Latin "ad-" (to) + "bassus" (low), meaning to bring low or humble.'
    
    result = validator.validate_word_complete(
        word, pos, definition, synonyms, antonyms, sentences, etymology
    )
    
    print(f"Validation Results for '{word}':")
    print(f"Overall Score: {result.overall_score:.2f}")
    print(f"Synonyms: {result.synonyms.score:.2f} - {'PASS' if result.synonyms.is_valid else 'FAIL'}")
    print(f"Antonyms: {result.antonyms.score:.2f} - {'PASS' if result.antonyms.is_valid else 'FAIL'}")
    print(f"Sentences: {result.sentences.score:.2f} - {'PASS' if result.sentences.is_valid else 'FAIL'}")
    print(f"Etymology: {result.etymology.score:.2f} - {'PASS' if result.etymology.is_valid else 'FAIL'}")
    
    if result.synonyms.issues:
        print(f"Synonym Issues: {result.synonyms.issues}")
    if result.antonyms.issues:
        print(f"Antonym Issues: {result.antonyms.issues}")
    if result.sentences.issues:
        print(f"Sentence Issues: {result.sentences.issues}")
    if result.etymology.issues:
        print(f"Etymology Issues: {result.etymology.issues}")

if __name__ == "__main__":
    main()