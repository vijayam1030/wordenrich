#!/usr/bin/env python3
"""
Multi-LLM Cross-Validation System
Uses multiple language models to validate and improve vocabulary enrichment quality
"""

import subprocess
import json
import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import statistics

class ValidationStrategy(Enum):
    CONSENSUS = "consensus"           # Majority agreement
    EXPERT_PANEL = "expert_panel"    # Different models for different tasks
    CROSS_CHECK = "cross_check"      # Each model validates others' outputs

@dataclass
class ModelResponse:
    model_name: str
    synonyms: List[str]
    antonyms: List[str]
    sentences: List[str] 
    etymology: str
    confidence: float
    response_time: float

@dataclass
class ConsensusResult:
    final_synonyms: List[str]
    final_antonyms: List[str]
    final_sentences: List[str]
    final_etymology: str
    confidence_score: float
    agreement_level: float
    model_votes: Dict[str, float]

class MultiLLMValidator:
    def __init__(self, strategy: ValidationStrategy = ValidationStrategy.CONSENSUS):
        self.strategy = strategy
        self.available_models = self.detect_available_models()
        self.model_specializations = self.define_model_roles()
        print(f"🤖 Available models: {list(self.available_models.keys())}")
        print(f"🔄 Validation strategy: {strategy.value}")

    def detect_available_models(self) -> Dict[str, dict]:
        """Detect available Ollama models and their characteristics."""
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
            if result.returncode != 0:
                print("⚠️  Ollama not available, falling back to single model")
                return {"llama3.1:8b": {"size": "8B", "speed": "medium", "quality": "high"}}
            
            models = {}
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        name = parts[0]
                        size = parts[2]
                        
                        # Categorize models by their characteristics
                        if "tinyllama" in name.lower() or "smollm" in name.lower():
                            models[name] = {"size": "1-2B", "speed": "fast", "quality": "basic"}
                        elif "gemma:2b" in name.lower() or "codegemma:2b" in name.lower():
                            models[name] = {"size": "2B", "speed": "fast", "quality": "good"}
                        elif "phi3" in name.lower() or "qwen2.5:14b" in name.lower():
                            models[name] = {"size": "3-14B", "speed": "medium", "quality": "high"}
                        elif "llama3.1:8b" in name.lower() or "mistral:7b" in name.lower():
                            models[name] = {"size": "7-8B", "speed": "medium", "quality": "high"}
                        elif "codellama" in name.lower():
                            models[name] = {"size": "7-13B", "speed": "slow", "quality": "specialized"}
                        else:
                            models[name] = {"size": "unknown", "speed": "medium", "quality": "medium"}
            
            return models
            
        except Exception as e:
            print(f"⚠️  Error detecting models: {e}")
            return {"llama3.1:8b": {"size": "8B", "speed": "medium", "quality": "high"}}

    def define_model_roles(self) -> Dict[str, List[str]]:
        """Define specialized roles for different models."""
        roles = {
            "synonym_expert": [],      # Best for finding synonyms
            "grammar_expert": [],      # Best for sentence validation  
            "etymology_expert": [],    # Best for word origins
            "general_validator": []    # Good all-around validators
        }
        
        # Assign models to roles based on their characteristics
        for model_name, props in self.available_models.items():
            if "llama" in model_name.lower() or "mistral" in model_name.lower():
                roles["general_validator"].append(model_name)
                roles["synonym_expert"].append(model_name)
            elif "phi3" in model_name.lower():
                roles["grammar_expert"].append(model_name)
                roles["general_validator"].append(model_name)
            elif "qwen" in model_name.lower():
                roles["etymology_expert"].append(model_name)
                roles["general_validator"].append(model_name)
            elif "codellama" in model_name.lower():
                roles["grammar_expert"].append(model_name)
            else:
                roles["general_validator"].append(model_name)
        
        # Ensure we have at least one model per role
        all_models = list(self.available_models.keys())
        for role in roles:
            if not roles[role] and all_models:
                roles[role] = [all_models[0]]  # Fallback to first available model
                
        return roles

    def call_model_with_timeout(self, model: str, prompt: str, timeout: int = 30) -> Optional[str]:
        """Call a specific model with timeout."""
        try:
            start_time = time.time()
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt,
                text=True,
                capture_output=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            response_time = time.time() - start_time
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            else:
                print(f"❌ {model} failed to respond")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {model} timed out")
            return None
        except Exception as e:
            print(f"❌ {model} error: {e}")
            return None

    def get_model_enrichment(self, model: str, word: str, pos: str, definition: str) -> Optional[ModelResponse]:
        """Get enrichment from a specific model."""
        prompt = f"""For the word "{word}" ({pos}), meaning "{definition}":

Provide exactly 5 synonyms, 5 antonyms, 3 example sentences, and etymology.

Format response as:
SYNONYMS: word1, word2, word3, word4, word5
ANTONYMS: word1, word2, word3, word4, word5
SENTENCE1: [sentence using {word}]
SENTENCE2: [sentence using {word}]
SENTENCE3: [sentence using {word}]
ORIGIN: [etymology]
CONFIDENCE: [0.0-1.0 confidence in this response]

Be precise and specific."""

        start_time = time.time()
        response = self.call_model_with_timeout(model, prompt)
        response_time = time.time() - start_time
        
        if not response:
            return None
            
        # Parse response
        lines = response.split('\n')
        synonyms = []
        antonyms = []
        sentences = ["", "", ""]
        etymology = ""
        confidence = 0.8  # Default confidence
        
        for line in lines:
            line = line.strip()
            if line.upper().startswith('SYNONYMS:'):
                syn_text = line[9:].strip()
                if syn_text and ',' in syn_text:
                    synonyms = [s.strip() for s in syn_text.split(',') if s.strip()][:5]
            elif line.upper().startswith('ANTONYMS:'):
                ant_text = line[9:].strip()
                if ant_text and ',' in ant_text:
                    antonyms = [s.strip() for s in ant_text.split(',') if s.strip()][:5]
            elif line.upper().startswith('SENTENCE1:'):
                sentences[0] = line[10:].strip()
            elif line.upper().startswith('SENTENCE2:'):
                sentences[1] = line[10:].strip()
            elif line.upper().startswith('SENTENCE3:'):
                sentences[2] = line[10:].strip()
            elif line.upper().startswith('ORIGIN:'):
                etymology = line[7:].strip()
            elif line.upper().startswith('CONFIDENCE:'):
                try:
                    confidence = float(line[11:].strip())
                except:
                    confidence = 0.8

        # Validate we got reasonable content
        if len(synonyms) >= 3 and len(antonyms) >= 3 and any(sentences) and etymology:
            return ModelResponse(
                model_name=model,
                synonyms=synonyms,
                antonyms=antonyms,
                sentences=sentences,
                etymology=etymology,
                confidence=confidence,
                response_time=response_time
            )
        else:
            print(f"⚠️  {model} provided incomplete response")
            return None

    def validate_with_cross_check(self, target_model: str, word: str, pos: str, definition: str,
                                 synonyms: List[str], antonyms: List[str]) -> Dict[str, float]:
        """Use other models to validate one model's synonyms/antonyms."""
        validator_models = [m for m in self.model_specializations["general_validator"] 
                          if m != target_model][:2]  # Use up to 2 other models
        
        validation_scores = {}
        
        for validator in validator_models:
            prompt = f"""Evaluate these synonyms and antonyms for "{word}" ({pos}): {definition}

SYNONYMS TO EVALUATE: {', '.join(synonyms)}
ANTONYMS TO EVALUATE: {', '.join(antonyms)}

Rate each list from 0.0 to 1.0:
SYNONYM_SCORE: [0.0-1.0]
ANTONYM_SCORE: [0.0-1.0]
ISSUES: [list any problems found]"""

            response = self.call_model_with_timeout(validator, prompt, 15)
            if response:
                scores = self.parse_validation_scores(response)
                validation_scores[validator] = scores
                
        return validation_scores

    def parse_validation_scores(self, response: str) -> Dict[str, float]:
        """Parse validation scores from model response."""
        scores = {"synonym_score": 0.7, "antonym_score": 0.7}  # Defaults
        
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.upper().startswith('SYNONYM_SCORE:'):
                try:
                    scores["synonym_score"] = float(line[14:].strip())
                except:
                    pass
            elif line.upper().startswith('ANTONYM_SCORE:'):
                try:
                    scores["antonym_score"] = float(line[14:].strip())
                except:
                    pass
                    
        return scores

    def build_consensus(self, responses: List[ModelResponse], word: str) -> ConsensusResult:
        """Build consensus from multiple model responses."""
        if not responses:
            return None
            
        # Collect all synonyms/antonyms with vote counts
        synonym_votes = {}
        antonym_votes = {}
        sentence_candidates = []
        etymology_candidates = []
        
        total_confidence = 0
        model_votes = {}
        
        for response in responses:
            weight = response.confidence
            model_votes[response.model_name] = weight
            total_confidence += weight
            
            # Weight votes by model confidence
            for syn in response.synonyms:
                if syn:
                    synonym_votes[syn] = synonym_votes.get(syn, 0) + weight
                    
            for ant in response.antonyms:
                if ant:
                    antonym_votes[ant] = antonym_votes.get(ant, 0) + weight
                    
            # Collect sentence and etymology candidates
            for sent in response.sentences:
                if sent and word.lower() in sent.lower():
                    sentence_candidates.append((sent, weight))
                    
            if response.etymology:
                etymology_candidates.append((response.etymology, weight))
        
        # Select top synonyms and antonyms by vote weight
        final_synonyms = sorted(synonym_votes.items(), key=lambda x: x[1], reverse=True)[:5]
        final_synonyms = [syn for syn, _ in final_synonyms]
        
        final_antonyms = sorted(antonym_votes.items(), key=lambda x: x[1], reverse=True)[:5]
        final_antonyms = [ant for ant, _ in final_antonyms]
        
        # Select best sentences by weight
        sentence_candidates.sort(key=lambda x: x[1], reverse=True)
        final_sentences = [sent for sent, _ in sentence_candidates[:3]]
        
        # Select etymology with highest weight
        if etymology_candidates:
            etymology_candidates.sort(key=lambda x: x[1], reverse=True)
            final_etymology = etymology_candidates[0][0]
        else:
            final_etymology = f"Etymology for {word} from multiple sources."
        
        # Calculate agreement level
        num_models = len(responses)
        max_possible_agreement = num_models * max(r.confidence for r in responses)
        actual_agreement = total_confidence / max_possible_agreement if max_possible_agreement > 0 else 0
        
        confidence_score = total_confidence / num_models if num_models > 0 else 0
        
        return ConsensusResult(
            final_synonyms=final_synonyms,
            final_antonyms=final_antonyms,
            final_sentences=final_sentences,
            final_etymology=final_etymology,
            confidence_score=confidence_score,
            agreement_level=actual_agreement,
            model_votes=model_votes
        )

    def multi_model_validation(self, word: str, pos: str, definition: str) -> Optional[ConsensusResult]:
        """Perform multi-model validation using the selected strategy."""
        
        if self.strategy == ValidationStrategy.CONSENSUS:
            return self.consensus_validation(word, pos, definition)
        elif self.strategy == ValidationStrategy.EXPERT_PANEL:
            return self.expert_panel_validation(word, pos, definition)
        elif self.strategy == ValidationStrategy.CROSS_CHECK:
            return self.cross_check_validation(word, pos, definition)
        else:
            return None

    def consensus_validation(self, word: str, pos: str, definition: str) -> Optional[ConsensusResult]:
        """Get consensus from multiple models."""
        # Select fastest and most reliable models first
        model_priorities = []
        for model, props in self.available_models.items():
            if props["speed"] == "fast":
                model_priorities.append((model, 3))  # High priority for fast models
            elif props["speed"] == "medium" and props["quality"] == "high":
                model_priorities.append((model, 2))  # Medium priority for quality models
            else:
                model_priorities.append((model, 1))  # Low priority for others
        
        # Sort by priority and select top 2 models for better response rates
        model_priorities.sort(key=lambda x: x[1], reverse=True)
        selected_models = [model for model, _ in model_priorities[:2]]
        print(f"🤖 Consensus validation with: {selected_models}")
        
        responses = []
        for model in selected_models:
            print(f"   📡 Querying {model}...")
            response = self.get_model_enrichment(model, word, pos, definition)
            if response:
                responses.append(response)
                
        if len(responses) >= 1:  # Accept single model if at least one responds
            return self.build_consensus(responses, word)
        else:
            print(f"⚠️  No model responses for consensus")
            return None

    def expert_panel_validation(self, word: str, pos: str, definition: str) -> Optional[ConsensusResult]:
        """Use specialized models for different tasks."""
        print(f"🧑‍🔬 Expert panel validation...")
        
        # Get synonyms from synonym expert
        synonym_expert = self.model_specializations["synonym_expert"][0] if self.model_specializations["synonym_expert"] else None
        grammar_expert = self.model_specializations["grammar_expert"][0] if self.model_specializations["grammar_expert"] else None
        etymology_expert = self.model_specializations["etymology_expert"][0] if self.model_specializations["etymology_expert"] else None
        
        responses = []
        
        # Collect responses from available experts
        experts = [synonym_expert, grammar_expert, etymology_expert]
        for expert in experts:
            if expert:
                print(f"   🎓 Expert {expert}...")
                response = self.get_model_enrichment(expert, word, pos, definition)
                if response:
                    responses.append(response)
                    
        if responses:
            return self.build_consensus(responses, word)
        else:
            return None

    def cross_check_validation(self, word: str, pos: str, definition: str) -> Optional[ConsensusResult]:
        """Use models to validate each other's outputs."""
        print(f"🔄 Cross-check validation...")
        
        # Get initial response from primary model
        primary_model = list(self.available_models.keys())[0]
        primary_response = self.get_model_enrichment(primary_model, word, pos, definition)
        
        if not primary_response:
            return None
            
        # Validate with other models
        validation_scores = self.validate_with_cross_check(
            primary_model, word, pos, definition,
            primary_response.synonyms, primary_response.antonyms
        )
        
        # Adjust confidence based on validation
        if validation_scores:
            avg_syn_score = statistics.mean([scores["synonym_score"] for scores in validation_scores.values()])
            avg_ant_score = statistics.mean([scores["antonym_score"] for scores in validation_scores.values()])
            
            # Update confidence based on cross-validation
            validated_confidence = (avg_syn_score + avg_ant_score) / 2
            primary_response.confidence = min(primary_response.confidence, validated_confidence)
            
        return ConsensusResult(
            final_synonyms=primary_response.synonyms,
            final_antonyms=primary_response.antonyms, 
            final_sentences=primary_response.sentences,
            final_etymology=primary_response.etymology,
            confidence_score=primary_response.confidence,
            agreement_level=primary_response.confidence,
            model_votes={primary_model: primary_response.confidence}
        )

def main():
    """Test the multi-LLM validation system."""
    validator = MultiLLMValidator(ValidationStrategy.CONSENSUS)
    
    # Test case
    word = "abase"
    pos = "v" 
    definition = "To lower in position, estimation, or the like; degrade."
    
    print(f"\n🧪 Testing multi-LLM validation for '{word}'")
    result = validator.multi_model_validation(word, pos, definition)
    
    if result:
        print(f"\n📊 Multi-LLM Results:")
        print(f"Confidence Score: {result.confidence_score:.2f}")
        print(f"Agreement Level: {result.agreement_level:.2f}")
        print(f"Model Votes: {result.model_votes}")
        print(f"Final Synonyms: {result.final_synonyms}")
        print(f"Final Antonyms: {result.final_antonyms}")
        print(f"Final Etymology: {result.final_etymology[:100]}...")
    else:
        print("❌ Multi-LLM validation failed")

if __name__ == "__main__":
    main()