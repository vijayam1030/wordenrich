#!/usr/bin/env python3
"""
Generate a multi-tab word game interface with different game variations
"""

import re
import html
import json
import random
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
        
        if not line or re.match(r'^-{10,}$', line):
            continue
            
        if line.startswith('Word: '):
            word_data = {
                'word': '',
                'meaning': '',
                'synonyms': [],
                'antonyms': [],
                'sentences': [],
                'origin': ''
            }
            current_section = None
            
            word_line = line[6:]
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
            if len(line) > 7:
                word_data['origin'] = line[7:].strip()
        elif line and current_section:
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

def generate_funny_clues(word_data):
    """Generate funny and creative clues for the word."""
    word = word_data['word'].lower()
    meaning = word_data['meaning']
    synonyms = word_data['synonyms']
    antonyms = word_data['antonyms']
    origin = word_data['origin']
    
    clues = []
    
    # Rhyme clue
    if word.endswith('ate'):
        clues.append(f"🎵 This word rhymes with 'fate' and means to {meaning.lower()}")
    elif word.endswith('ous'):
        clues.append(f"🎵 This '-ous' word describes something {meaning.lower()}")
    elif word.endswith('ent'):
        clues.append(f"🎵 This '-ent' word is about {meaning.lower()}")
    
    # Synonym riddle
    if synonyms:
        clue_synonyms = synonyms[:3]
        clues.append(f"🔍 I'm buddies with {', '.join(clue_synonyms)}. What am I?")
    
    # Antonym riddle
    if antonyms:
        clue_antonyms = antonyms[:2]
        clues.append(f"⚡ I'm the opposite of {' and '.join(clue_antonyms)}!")
    
    # Letter clue
    clues.append(f"📝 I start with '{word[0].upper()}' and have {len(word)} letters")
    
    # Origin clue
    if origin and 'Latin' in origin:
        clues.append(f"🏛️ My ancestors spoke Latin, and I mean {meaning.lower()}")
    
    # Silly definition
    silly_meanings = [
        f"🤪 I'm what happens when {meaning.lower()} gets fancy",
        f"😄 Imagine {meaning.lower()} wearing a tuxedo - that's me!",
        f"🎭 I'm the drama queen version of {meaning.lower()}"
    ]
    clues.append(random.choice(silly_meanings))
    
    return clues

def create_multi_game_html(words_data):
    """Create the multi-tab game HTML."""
    
    # Convert words data to JSON for JavaScript
    game_data = []
    for word_data in words_data:
        if word_data['word'] and word_data['meaning']:
            clues = generate_funny_clues(word_data)
            game_data.append({
                'word': word_data['word'],
                'meaning': word_data['meaning'],
                'synonyms': word_data['synonyms'][:5],
                'antonyms': word_data['antonyms'][:5],
                'sentences': word_data['sentences'][:3],
                'origin': word_data['origin'],
                'clues': clues,
                'difficulty': len(word_data['word']) + len(word_data['synonyms']) # Simple difficulty metric
            })
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Word Games Collection</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Comic Sans MS', cursive, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .game-container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .game-header {{
            text-align: center;
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .game-title {{
            font-size: 3em;
            color: #667eea;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        
        .game-subtitle {{
            font-size: 1.2em;
            color: #666;
        }}
        
        /* Tab Styles */
        .tab-container {{
            background: white;
            border-radius: 20px 20px 0 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .tab-nav {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 3px solid #e9ecef;
        }}
        
        .tab-btn {{
            flex: 1;
            padding: 20px;
            background: none;
            border: none;
            font-size: 1.1em;
            font-weight: bold;
            color: #666;
            cursor: pointer;
            transition: all 0.3s ease;
            border-bottom: 4px solid transparent;
            font-family: inherit;
        }}
        
        .tab-btn:hover {{
            background: #e9ecef;
            color: #333;
        }}
        
        .tab-btn.active {{
            color: #667eea;
            background: white;
            border-bottom-color: #667eea;
        }}
        
        .tab-icon {{
            font-size: 1.3em;
            margin-bottom: 5px;
            display: block;
        }}
        
        .tab-label {{
            font-size: 0.9em;
            display: block;
        }}
        
        /* Game Content */
        .tab-content {{
            display: none;
            padding: 40px;
            background: white;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .game-description {{
            background: linear-gradient(135deg, #e8f5e8 0%, #c6f6d5 100%);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            border-left: 5px solid #38a169;
        }}
        
        .question-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            font-size: 1.3em;
            line-height: 1.6;
            text-align: center;
        }}
        
        .clue {{
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border: 2px dashed #ffeaa7;
            font-size: 1.1em;
        }}
        
        .multiple-choice-clue {{
            background: linear-gradient(135deg, #e8f5e8 0%, #c6f6d5 100%);
            color: #22543d;
            border: 2px solid #38a169;
            padding: 20px;
            border-radius: 15px;
            font-weight: bold;
        }}
        
        .choice-options {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 15px;
        }}
        
        .choice-option {{
            background: #38a169;
            color: white;
            padding: 12px 20px;
            border-radius: 15px;
            font-size: 0.95em;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: left;
            border: 2px solid transparent;
        }}
        
        .choice-option:hover {{
            background: #2f855a;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(56, 161, 105, 0.3);
        }}
        
        .choice-option.selected {{
            background: #2f855a;
            border-color: #22543d;
            box-shadow: 0 4px 12px rgba(56, 161, 105, 0.4);
        }}
        
        .input-area {{
            margin: 30px 0;
            text-align: center;
        }}
        
        .game-input {{
            padding: 15px;
            font-size: 1.2em;
            border: 3px solid #667eea;
            border-radius: 25px;
            width: 100%;
            max-width: 400px;
            text-align: center;
            font-family: inherit;
        }}
        
        .game-input:focus {{
            outline: none;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        }}
        
        .btn-group {{
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        
        .game-btn {{
            padding: 12px 25px;
            font-size: 1.1em;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-family: inherit;
            transition: all 0.3s ease;
        }}
        
        .submit-btn {{
            background: #48bb78;
            color: white;
        }}
        
        .submit-btn:hover {{
            background: #38a169;
            transform: translateY(-2px);
        }}
        
        .hint-btn {{
            background: #ed8936;
            color: white;
        }}
        
        .hint-btn:hover {{
            background: #dd6b20;
            transform: translateY(-2px);
        }}
        
        .skip-btn {{
            background: #e53e3e;
            color: white;
        }}
        
        .skip-btn:hover {{
            background: #c53030;
            transform: translateY(-2px);
        }}
        
        .primary-btn {{
            background: #667eea;
            color: white;
        }}
        
        .primary-btn:hover {{
            background: #5a67d8;
            transform: translateY(-2px);
        }}
        
        .score-board {{
            display: flex;
            justify-content: space-around;
            background: #f7fafc;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
        }}
        
        .score-item {{
            text-align: center;
        }}
        
        .score-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .score-label {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .feedback {{
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            font-size: 1.2em;
            font-weight: bold;
            text-align: center;
        }}
        
        .correct {{
            background: #c6f6d5;
            color: #22543d;
            border: 2px solid #38a169;
        }}
        
        .incorrect {{
            background: #fed7d7;
            color: #742a2a;
            border: 2px solid #e53e3e;
        }}
        
        .answer-reveal {{
            background: #bee3f8;
            color: #2a4365;
            border: 2px solid #3182ce;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        
        .word-details {{
            text-align: left;
            margin-top: 15px;
        }}
        
        .detail-section {{
            margin: 10px 0;
        }}
        
        .detail-title {{
            font-weight: bold;
            color: #667eea;
        }}
        
        .synonym-tag, .antonym-tag {{
            display: inline-block;
            padding: 5px 10px;
            margin: 3px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        
        .synonym-tag {{
            background: #c6f6d5;
            color: #22543d;
        }}
        
        .antonym-tag {{
            background: #fed7d7;
            color: #742a2a;
        }}
        
        .example-sentence {{
            background: #f7fafc;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            border-left: 4px solid #667eea;
            font-style: italic;
        }}
        
        /* Speed Mode Specific */
        .timer-display {{
            font-size: 2em;
            font-weight: bold;
            color: #e53e3e;
            text-align: center;
            margin: 20px 0;
        }}
        
        .progress-bar {{
            background: #e2e8f0;
            border-radius: 25px;
            overflow: hidden;
            height: 10px;
            margin: 20px 0;
        }}
        
        .progress-fill {{
            background: linear-gradient(90deg, #48bb78, #38a169);
            height: 100%;
            transition: width 0.3s ease;
        }}
        
        /* Difficulty Settings */
        .difficulty-selector {{
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
        }}
        
        .difficulty-btn {{
            padding: 10px 20px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 20px;
            cursor: pointer;
            font-family: inherit;
            transition: all 0.3s ease;
        }}
        
        .difficulty-btn.active {{
            background: #667eea;
            color: white;
        }}
        
        /* Memory Game Cards */
        .memory-card {{
            transition: all 0.3s ease;
            user-select: none;
            font-weight: bold;
        }}
        
        .memory-card:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        
        @keyframes bounce {{
            0%, 20%, 60%, 100% {{
                transform: translateY(0);
            }}
            40% {{
                transform: translateY(-10px);
            }}
            80% {{
                transform: translateY(-5px);
            }}
        }}
        
        .bounce {{
            animation: bounce 1s;
        }}
        
        .hidden {{
            display: none;
        }}
        
        @media (max-width: 768px) {{
            .game-container {{
                padding: 10px;
            }}
            
            .game-header, .tab-content {{
                padding: 20px;
            }}
            
            .game-title {{
                font-size: 2em;
            }}
            
            .tab-nav {{
                flex-direction: column;
            }}
            
            .btn-group {{
                flex-direction: column;
                align-items: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-header">
            <h1 class="game-title">🎮 Word Games Collection</h1>
            <p class="game-subtitle">Choose your challenge and master the vocabulary!</p>
        </div>
        
        <div class="tab-container">
            <div class="tab-nav">
                <button class="tab-btn active" data-tab="classic">
                    <span class="tab-icon">📚</span>
                    <span class="tab-label">Classic Mode</span>
                </button>
                <button class="tab-btn" data-tab="speed">
                    <span class="tab-icon">⚡</span>
                    <span class="tab-label">Speed Challenge</span>
                </button>
                <button class="tab-btn" data-tab="quiz">
                    <span class="tab-icon">🧠</span>
                    <span class="tab-label">Quiz Master</span>
                </button>
                <button class="tab-btn" data-tab="memory">
                    <span class="tab-icon">🧩</span>
                    <span class="tab-label">Memory Game</span>
                </button>
                <button class="tab-btn" data-tab="battle">
                    <span class="tab-icon">⚔️</span>
                    <span class="tab-label">Word Battle</span>
                </button>
            </div>
            
            <!-- Classic Mode Tab -->
            <div class="tab-content active" id="classic-tab">
                <div class="game-description">
                    <h3>📚 Classic Word Master</h3>
                    <p>The original word guessing game with hints and multiple choice support. Perfect for learning and understanding vocabulary in depth.</p>
                </div>
                
                <div class="score-board">
                    <div class="score-item">
                        <div class="score-number" id="classic-correct">0</div>
                        <div class="score-label">Correct</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="classic-total">0</div>
                        <div class="score-label">Total</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="classic-streak">0</div>
                        <div class="score-label">Streak</div>
                    </div>
                </div>
                
                <div class="difficulty-selector">
                    <button class="difficulty-btn active" data-difficulty="easy">🟢 Easy</button>
                    <button class="difficulty-btn" data-difficulty="medium">🟡 Medium</button>
                    <button class="difficulty-btn" data-difficulty="hard">🔴 Hard</button>
                </div>
                
                <div class="question-card" id="classic-question">
                    Click "New Question" to start playing!
                </div>
                
                <div class="btn-group">
                    <button class="game-btn submit-btn" id="classic-word-meaning">📖 Word → Meaning</button>
                    <button class="game-btn submit-btn" id="classic-meaning-word">🔍 Meaning → Word</button>
                    <button class="game-btn submit-btn" id="classic-sentence-clue">💬 Sentence Clues</button>
                    <button class="game-btn submit-btn" id="classic-fun-clues">🎭 Fun Clues</button>
                </div>
                
                <div id="classic-clues-area"></div>
                
                <div class="input-area">
                    <input type="text" class="game-input" id="classic-answer-input" placeholder="Type your answer here..." disabled>
                </div>
                
                <div class="btn-group">
                    <button class="game-btn submit-btn" id="classic-submit-btn" disabled>Submit Answer</button>
                    <button class="game-btn hint-btn" id="classic-hint-btn" disabled>Get Hint 💡</button>
                    <button class="game-btn skip-btn" id="classic-skip-btn" disabled>Skip Question</button>
                </div>
                
                <div class="btn-group">
                    <button class="game-btn primary-btn" id="classic-new-question">New Question 🎲</button>
                </div>
                
                <div id="classic-feedback-area"></div>
            </div>
            
            <!-- Speed Challenge Tab -->
            <div class="tab-content" id="speed-tab">
                <div class="game-description">
                    <h3>⚡ Speed Challenge</h3>
                    <p>Answer as many questions as possible in 60 seconds! Quick thinking and fast typing required.</p>
                </div>
                
                <div class="timer-display" id="speed-timer">60</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="speed-progress" style="width: 100%"></div>
                </div>
                
                <div class="score-board">
                    <div class="score-item">
                        <div class="score-number" id="speed-correct">0</div>
                        <div class="score-label">Correct</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="speed-total">0</div>
                        <div class="score-label">Attempted</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="speed-wpm">0</div>
                        <div class="score-label">WPM</div>
                    </div>
                </div>
                
                <div class="question-card" id="speed-question">
                    Click "Start Speed Challenge" to begin!
                </div>
                
                <div class="input-area">
                    <input type="text" class="game-input" id="speed-answer-input" placeholder="Type answer and press Enter..." disabled>
                </div>
                
                <div class="btn-group">
                    <button class="game-btn primary-btn" id="speed-start-btn">Start Speed Challenge ⚡</button>
                    <button class="game-btn skip-btn" id="speed-skip-btn" disabled>Skip (Space)</button>
                </div>
                
                <div id="speed-feedback-area"></div>
            </div>
            
            <!-- Quiz Master Tab -->
            <div class="tab-content" id="quiz-tab">
                <div class="game-description">
                    <h3>🧠 Quiz Master</h3>
                    <p>Take comprehensive vocabulary quizzes with detailed scoring and progress tracking.</p>
                </div>
                
                <div class="score-board">
                    <div class="score-item">
                        <div class="score-number" id="quiz-progress">0/10</div>
                        <div class="score-label">Progress</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="quiz-score">0%</div>
                        <div class="score-label">Score</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="quiz-grade">-</div>
                        <div class="score-label">Grade</div>
                    </div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" id="quiz-progress-bar" style="width: 0%"></div>
                </div>
                
                <div class="question-card" id="quiz-question">
                    Click "Start Quiz" to begin a 10-question vocabulary test!
                </div>
                
                <div id="quiz-options-area"></div>
                
                <div class="btn-group">
                    <button class="game-btn primary-btn" id="quiz-start-btn">Start Quiz 🧠</button>
                    <button class="game-btn submit-btn" id="quiz-next-btn" disabled>Next Question →</button>
                </div>
                
                <div id="quiz-feedback-area"></div>
            </div>
            
            <!-- Memory Game Tab -->
            <div class="tab-content" id="memory-tab">
                <div class="game-description">
                    <h3>🧩 Memory Game</h3>
                    <p>Match words with their meanings in this memory-challenging card game.</p>
                </div>
                
                <div class="score-board">
                    <div class="score-item">
                        <div class="score-number" id="memory-matches">0</div>
                        <div class="score-label">Matches</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="memory-attempts">0</div>
                        <div class="score-label">Attempts</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="memory-time">0s</div>
                        <div class="score-label">Time</div>
                    </div>
                </div>
                
                <div id="memory-grid" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0;">
                    <!-- Memory cards will be generated here -->
                </div>
                
                <div class="btn-group">
                    <button class="game-btn primary-btn" id="memory-start-btn">Start Memory Game 🧩</button>
                    <button class="game-btn hint-btn" id="memory-shuffle-btn" disabled>Shuffle Cards 🔄</button>
                </div>
                
                <div id="memory-feedback-area"></div>
            </div>
            
            <!-- Word Battle Tab -->
            <div class="tab-content" id="battle-tab">
                <div class="game-description">
                    <h3>⚔️ Word Battle</h3>
                    <p>Battle against the clock in different challenge modes. Survive as long as you can!</p>
                </div>
                
                <div class="score-board">
                    <div class="score-item">
                        <div class="score-number" id="battle-level">1</div>
                        <div class="score-label">Level</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="battle-lives">❤️❤️❤️</div>
                        <div class="score-label">Lives</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="battle-score">0</div>
                        <div class="score-label">Score</div>
                    </div>
                </div>
                
                <div class="timer-display" id="battle-timer">10</div>
                
                <div class="question-card" id="battle-question">
                    Click "Start Battle" to begin the ultimate vocabulary challenge!
                </div>
                
                <div class="input-area">
                    <input type="text" class="game-input" id="battle-answer-input" placeholder="Quick! Type your answer..." disabled>
                </div>
                
                <div class="btn-group">
                    <button class="game-btn primary-btn" id="battle-start-btn">Start Battle ⚔️</button>
                    <button class="game-btn skip-btn" id="battle-surrender-btn" disabled>Surrender 🏳️</button>
                </div>
                
                <div id="battle-feedback-area"></div>
            </div>
        </div>
    </div>

    <script>
        const gameData = {json.dumps(game_data)};
        
        // Global game state
        let activeTab = 'classic';
        let gameStates = {{
            classic: {{
                currentWord: null,
                gameMode: 'word-to-meaning',
                hintsUsed: 0,
                correctAnswers: 0,
                totalQuestions: 0,
                currentStreak: 0,
                difficulty: 'easy'
            }},
            speed: {{
                timeLeft: 60,
                totalTime: 60,
                correctAnswers: 0,
                totalQuestions: 0,
                isActive: false,
                startTime: 0,
                timer: null
            }},
            quiz: {{
                currentQuestion: 0,
                totalQuestions: 10,
                correctAnswers: 0,
                questions: [],
                isActive: false
            }},
            memory: {{
                cards: [],
                flippedCards: [],
                matchedPairs: 0,
                attempts: 0,
                startTime: 0,
                isActive: false
            }},
            battle: {{
                level: 1,
                lives: 3,
                score: 0,
                timeLeft: 10,
                isActive: false,
                currentWord: null,
                timer: null
            }}
        }};
        
        // Initialize the game
        document.addEventListener('DOMContentLoaded', function() {{
            initializeTabs();
            initializeClassicMode();
            initializeSpeedMode();
            initializeQuizMode();
            initializeMemoryMode();
            initializeBattleMode();
        }});
        
        function initializeTabs() {{
            const tabButtons = document.querySelectorAll('.tab-btn');
            const tabContents = document.querySelectorAll('.tab-content');
            
            tabButtons.forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const targetTab = btn.dataset.tab;
                    
                    // Update active tab
                    tabButtons.forEach(b => b.classList.remove('active'));
                    tabContents.forEach(content => content.classList.remove('active'));
                    
                    btn.classList.add('active');
                    document.getElementById(targetTab + '-tab').classList.add('active');
                    
                    activeTab = targetTab;
                }});
            }});
        }}
        
        // Classic Mode Functions
        function initializeClassicMode() {{
            const state = gameStates.classic;
            
            // Mode buttons
            document.getElementById('classic-word-meaning').addEventListener('click', () => {{
                state.gameMode = 'word-to-meaning';
                highlightActiveMode('classic', 'word-to-meaning');
                generateClassicQuestion();
            }});
            
            document.getElementById('classic-meaning-word').addEventListener('click', () => {{
                state.gameMode = 'meaning-to-word';
                highlightActiveMode('classic', 'meaning-to-word');
                generateClassicQuestion();
            }});
            
            document.getElementById('classic-sentence-clue').addEventListener('click', () => {{
                state.gameMode = 'sentence-clue';
                highlightActiveMode('classic', 'sentence-clue');
                generateClassicQuestion();
            }});
            
            document.getElementById('classic-fun-clues').addEventListener('click', () => {{
                state.gameMode = 'fun-clues';
                highlightActiveMode('classic', 'fun-clues');
                generateClassicQuestion();
            }});
            
            // Difficulty buttons
            document.querySelectorAll('#classic-tab .difficulty-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    document.querySelectorAll('#classic-tab .difficulty-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    state.difficulty = btn.dataset.difficulty;
                    generateClassicQuestion();
                }});
            }});
            
            // Game controls
            document.getElementById('classic-new-question').addEventListener('click', generateClassicQuestion);
            document.getElementById('classic-submit-btn').addEventListener('click', checkClassicAnswer);
            document.getElementById('classic-hint-btn').addEventListener('click', showClassicHint);
            document.getElementById('classic-skip-btn').addEventListener('click', skipClassicQuestion);
            
            // Input handling
            const answerInput = document.getElementById('classic-answer-input');
            answerInput.addEventListener('keypress', (e) => {{
                if (e.key === 'Enter') {{
                    checkClassicAnswer();
                }}
            }});
            
            answerInput.addEventListener('input', () => {{
                document.getElementById('classic-submit-btn').disabled = answerInput.value.trim() === '';
            }});
            
            // Highlight first mode as active
            highlightActiveMode('classic', 'word-to-meaning');
        }}
        
        function highlightActiveMode(tab, mode) {{
            const buttons = {{
                'word-to-meaning': document.getElementById(tab + '-word-meaning'),
                'meaning-to-word': document.getElementById(tab + '-meaning-word'),
                'sentence-clue': document.getElementById(tab + '-sentence-clue'),
                'fun-clues': document.getElementById(tab + '-fun-clues')
            }};
            
            Object.values(buttons).forEach(btn => {{
                if (btn) btn.style.background = '#48bb78';
            }});
            
            if (buttons[mode]) {{
                buttons[mode].style.background = '#38a169';
            }}
        }}
        
        function generateClassicQuestion() {{
            const state = gameStates.classic;
            
            // Filter words by difficulty
            let filteredWords = gameData;
            if (state.difficulty === 'easy') {{
                filteredWords = gameData.filter(w => w.word.length <= 6 && w.synonyms.length >= 2);
            }} else if (state.difficulty === 'medium') {{
                filteredWords = gameData.filter(w => w.word.length > 6 && w.word.length <= 10);
            }} else {{
                filteredWords = gameData.filter(w => w.word.length > 10 || w.synonyms.length < 2);
            }}
            
            state.currentWord = filteredWords[Math.floor(Math.random() * filteredWords.length)];
            state.hintsUsed = 0;
            state.selectedAnswer = null;
            
            // Reset UI
            document.getElementById('classic-clues-area').innerHTML = '';
            document.getElementById('classic-feedback-area').innerHTML = '';
            const answerInput = document.getElementById('classic-answer-input');
            answerInput.value = '';
            answerInput.style.display = 'none'; // Hide text input
            document.getElementById('classic-submit-btn').disabled = true;
            document.getElementById('classic-hint-btn').style.display = 'none'; // Hide hints - we show MC immediately
            document.getElementById('classic-skip-btn').disabled = false;
            
            // Generate and show multiple choice options
            generateClassicOptions();
        }}
        
        function generateClassicOptions() {{
            const state = gameStates.classic;
            let options = [];
            let correctAnswer = '';
            
            // Generate options based on game mode
            switch(state.gameMode) {{
                case 'word-to-meaning':
                    // Show 4 meanings, one is correct
                    const wrongMeanings = gameData
                        .filter(w => w.word !== state.currentWord.word && w.meaning.length > 10)
                        .sort(() => Math.random() - 0.5)
                        .slice(0, 3)
                        .map(w => w.meaning);
                    options = [...wrongMeanings, state.currentWord.meaning].sort(() => Math.random() - 0.5);
                    correctAnswer = state.currentWord.meaning;
                    document.getElementById('classic-question').innerHTML = '<strong>What does "' + state.currentWord.word + '" mean?</strong>';
                    break;
                    
                case 'meaning-to-word':
                    // Show 4 words, one is correct
                    const wrongWords = gameData
                        .filter(w => w.word !== state.currentWord.word)
                        .sort(() => Math.random() - 0.5)
                        .slice(0, 3)
                        .map(w => w.word);
                    options = [...wrongWords, state.currentWord.word].sort(() => Math.random() - 0.5);
                    correctAnswer = state.currentWord.word;
                    document.getElementById('classic-question').innerHTML = '<strong>Which word means:</strong><br>"' + state.currentWord.meaning + '"';
                    break;
                    
                case 'sentence-clue':
                    // Show 4 words, one fits the sentence
                    const wrongSentenceWords = gameData
                        .filter(w => w.word !== state.currentWord.word)
                        .sort(() => Math.random() - 0.5)
                        .slice(0, 3)
                        .map(w => w.word);
                    options = [...wrongSentenceWords, state.currentWord.word].sort(() => Math.random() - 0.5);
                    correctAnswer = state.currentWord.word;
                    
                    if (state.currentWord.sentences.length > 0) {{
                        const sentence = state.currentWord.sentences[Math.floor(Math.random() * state.currentWord.sentences.length)];
                        const hiddenSentence = sentence.replace(new RegExp(state.currentWord.word, 'gi'), '____');
                        document.getElementById('classic-question').innerHTML = '<strong>Fill in the blank:</strong><br>"' + hiddenSentence + '"';
                    }} else {{
                        // Fallback to word-to-meaning
                        state.gameMode = 'word-to-meaning';
                        generateClassicOptions();
                        return;
                    }}
                    break;
                    
                case 'fun-clues':
                    // Show 4 words, one matches the clue
                    const wrongClueWords = gameData
                        .filter(w => w.word !== state.currentWord.word)
                        .sort(() => Math.random() - 0.5)
                        .slice(0, 3)
                        .map(w => w.word);
                    options = [...wrongClueWords, state.currentWord.word].sort(() => Math.random() - 0.5);
                    correctAnswer = state.currentWord.word;
                    
                    const randomClue = state.currentWord.clues[Math.floor(Math.random() * state.currentWord.clues.length)];
                    document.getElementById('classic-question').innerHTML = '<strong>Guess the word:</strong><br>' + randomClue;
                    break;
            }}
            
            state.correctAnswer = correctAnswer;
            state.options = options;
            
            // Display options
            displayClassicOptions(options);
        }}
        
        function displayClassicOptions(options) {{
            const optionsArea = document.getElementById('classic-clues-area');
            optionsArea.innerHTML = '<div style="margin: 20px 0; font-weight: bold; color: #667eea;">Choose the correct answer:</div>';
            
            options.forEach((option, index) => {{
                const optionDiv = document.createElement('div');
                optionDiv.className = 'choice-option';
                optionDiv.style.margin = '10px 0';
                optionDiv.style.cursor = 'pointer';
                optionDiv.textContent = (index + 1) + '. ' + option;
                
                optionDiv.onclick = function() {{
                    // Clear previous selections
                    document.querySelectorAll('#classic-clues-area .choice-option').forEach(opt => {{
                        opt.classList.remove('selected');
                        opt.style.background = '#38a169';
                    }});
                    
                    // Mark this as selected
                    optionDiv.classList.add('selected');
                    optionDiv.style.background = '#2f855a';
                    
                    gameStates.classic.selectedAnswer = option;
                    document.getElementById('classic-submit-btn').disabled = false;
                }};
                
                optionsArea.appendChild(optionDiv);
            }});
        }}
        
        // Helper function to extract context from sentences
        function getContextClue(word) {{
            if (!word.sentences || word.sentences.length === 0) {{
                // Fallback context based on synonyms/antonyms
                if (word.synonyms.length > 0) {{
                    return 'situations involving ' + word.synonyms.slice(0, 2).join(' or ');
                }}
                return 'formal or literary contexts';
            }}
            
            const sentence = word.sentences[0];
            // Try to extract meaningful context
            if (sentence.includes('person') || sentence.includes('people')) {{
                return 'describing people or personalities';
            }} else if (sentence.includes('feeling') || sentence.includes('emotion')) {{
                return 'emotions and feelings';
            }} else if (sentence.includes('action') || sentence.includes('do')) {{
                return 'actions and behaviors';
            }} else if (sentence.includes('place') || sentence.includes('location')) {{
                return 'places and locations';
            }} else {{
                return 'everyday situations';
            }}
        }}
        
        function showClassicHint() {{
            const state = gameStates.classic;
            state.hintsUsed++;
            
            const clue = document.createElement('div');
            clue.className = 'clue';
            
            // Generate multiple choice options 
            let multipleChoiceOptions = [];
            if ((state.gameMode === 'word-to-meaning' && state.hintsUsed >= 3) || state.hintsUsed === 6) {{
                if (state.gameMode === 'word-to-meaning') {{
                    const wrongMeanings = gameData
                        .filter(w => w.word !== state.currentWord.word && w.meaning.length > 10)
                        .sort(() => Math.random() - 0.5)
                        .slice(0, 3)
                        .map(w => w.meaning);
                    
                    multipleChoiceOptions = [...wrongMeanings, state.currentWord.meaning].sort(() => Math.random() - 0.5);
                }} else {{
                    const wrongOptions = gameData
                        .filter(w => w.word !== state.currentWord.word && w.word.length >= state.currentWord.word.length - 2 && w.word.length <= state.currentWord.word.length + 2)
                        .sort(() => Math.random() - 0.5)
                        .slice(0, 3)
                        .map(w => w.word);
                    
                    multipleChoiceOptions = [...wrongOptions, state.currentWord.word].sort(() => Math.random() - 0.5);
                }}
            }}
            
            let hints = [];
            
            if (state.gameMode === 'word-to-meaning') {{
                hints = [
                    '💡 Hint ' + state.hintsUsed + ': This word is often used when talking about ' + getContextClue(state.currentWord),
                    '💡 Hint ' + state.hintsUsed + ': It means something similar to: ' + state.currentWord.synonyms.slice(0, 2).join(' or '),
                    '🎯 Multiple Choice Time! Pick the correct meaning:',
                    '', // Multiple choice shows on hint 3, so skip individual hints
                    '', // Skip hint 5
                    '🎯 Final Hint: Choose one of these options: ' + multipleChoiceOptions.join(' | ')
                ];
            }} else {{
                hints = [
                    '💡 Hint ' + state.hintsUsed + ': The word has ' + state.currentWord.word.length + ' letters',
                    '💡 Hint ' + state.hintsUsed + ': It starts with "' + state.currentWord.word[0].toUpperCase() + '"',
                    '💡 Hint ' + state.hintsUsed + ': Synonyms include: ' + state.currentWord.synonyms.slice(0, 2).join(', '),
                    '💡 Hint ' + state.hintsUsed + ': It\\'s NOT the same as: ' + state.currentWord.antonyms.slice(0, 2).join(', '),
                    '💡 Hint ' + state.hintsUsed + ': ' + state.currentWord.origin.substring(0, 50) + '...',
                    '🎯 Final Hint: Choose one of these options: ' + multipleChoiceOptions.join(' | ')
                ];
            }}
            
            if (state.hintsUsed <= hints.length) {{
                const shouldShowMultipleChoice = (state.gameMode === 'word-to-meaning' && state.hintsUsed >= 3) || state.hintsUsed === 6;
                
                if (shouldShowMultipleChoice && multipleChoiceOptions.length > 0) {{
                    // Special styling for multiple choice hint
                    clue.className = 'clue multiple-choice-clue';
                    clue.innerHTML = (state.gameMode === 'word-to-meaning' && state.hintsUsed === 3) ? 
                        '🎯 Multiple Choice Time! Pick the correct meaning:' : 
                        '🎯 Final Hint: Choose the correct ' + (state.gameMode === 'word-to-meaning' ? 'meaning' : 'word') + ':';
                    
                    // Create clickable options
                    const optionsDiv = document.createElement('div');
                    optionsDiv.className = 'choice-options';
                    
                    multipleChoiceOptions.forEach(option => {{
                        const optionDiv = document.createElement('div');
                        optionDiv.className = 'choice-option';
                        optionDiv.textContent = option;
                        optionDiv.onclick = function() {{
                            const answerInput = document.getElementById('classic-answer-input');
                            answerInput.value = option;
                            answerInput.focus();
                            answerInput.dispatchEvent(new Event('input'));
                            document.querySelectorAll('.choice-option').forEach(opt => opt.classList.remove('selected'));
                            optionDiv.classList.add('selected');
                        }};
                        optionsDiv.appendChild(optionDiv);
                    }});
                    
                    clue.appendChild(optionsDiv);
                    
                    // For word-to-meaning mode, disable further hints after multiple choice appears
                    if (state.gameMode === 'word-to-meaning' && state.hintsUsed >= 3) {{
                        document.getElementById('classic-hint-btn').disabled = true;
                    }}
                }} else if (hints[state.hintsUsed - 1] && hints[state.hintsUsed - 1] !== '') {{
                    clue.textContent = hints[state.hintsUsed - 1];
                }} else {{
                    // Skip empty hints and try next one
                    if (state.hintsUsed < 6) {{
                        state.hintsUsed++;
                        showClassicHint();
                        return;
                    }}
                }}
                
                document.getElementById('classic-clues-area').appendChild(clue);
                clue.classList.add('bounce');
            }}
            
            if (state.hintsUsed >= 6) {{
                document.getElementById('classic-hint-btn').disabled = true;
            }}
        }}
        
        function checkClassicAnswer() {{
            const state = gameStates.classic;
            const userAnswer = state.selectedAnswer;
            
            if (!userAnswer) {{
                alert('Please select an answer first!');
                return;
            }}
            
            const isCorrect = userAnswer === state.correctAnswer;
            
            state.totalQuestions++;
            
            if (isCorrect) {{
                state.correctAnswers++;
                state.currentStreak++;
                showClassicFeedback(true);
            }} else {{
                state.currentStreak = 0;
                showClassicFeedback(false);
            }}
            
            updateClassicScores();
            disableClassicInputs();
        }}
        
        function showClassicSpecialFeedback(type) {{
            const state = gameStates.classic;
            const feedback = document.createElement('div');
            feedback.className = 'feedback incorrect';
            
            if (type === 'word-instead-of-meaning') {{
                feedback.innerHTML = '🤔 Close! You typed the word "' + state.currentWord.word + '" but I need its <strong>meaning</strong>!<br>💡 Try: "' + state.currentWord.meaning + '"';
            }}
            
            document.getElementById('classic-feedback-area').innerHTML = '';
            document.getElementById('classic-feedback-area').appendChild(feedback);
            
            setTimeout(() => {{
                feedback.innerHTML += '<br><br>🎯 Try again! What does "' + state.currentWord.word + '" mean?';
            }}, 2000);
        }}
        
        function showClassicFeedback(correct) {{
            const state = gameStates.classic;
            const feedback = document.createElement('div');
            feedback.className = 'feedback ' + (correct ? 'correct' : 'incorrect');
            
            if (correct) {{
                const messages = ['🎉 Excellent!', '✨ Perfect!', '🚀 Amazing!', '🏆 Brilliant!', '⭐ Outstanding!'];
                feedback.innerHTML = messages[Math.floor(Math.random() * messages.length)];
            }} else {{
                feedback.innerHTML = '❌ Not quite right. The correct answer was: <strong>' + state.correctAnswer + '</strong>';
            }}
            
            document.getElementById('classic-feedback-area').innerHTML = '';
            document.getElementById('classic-feedback-area').appendChild(feedback);
            
            setTimeout(() => {{
                showClassicWordDetails();
            }}, 1000);
        }}
        
        function showClassicWordDetails() {{
            const state = gameStates.classic;
            const details = document.createElement('div');
            details.className = 'answer-reveal';
            
            let detailsHTML = '<h3>' + state.currentWord.word + '</h3><div class="word-details">';
            detailsHTML += '<div class="detail-section"><span class="detail-title">Meaning:</span> ' + state.currentWord.meaning + '</div>';
            
            if (state.currentWord.synonyms.length) {{
                detailsHTML += '<div class="detail-section"><span class="detail-title">Synonyms:</span><br>';
                detailsHTML += state.currentWord.synonyms.map(syn => '<span class="synonym-tag">' + syn + '</span>').join('');
                detailsHTML += '</div>';
            }}
            
            if (state.currentWord.antonyms.length) {{
                detailsHTML += '<div class="detail-section"><span class="detail-title">Antonyms:</span><br>';
                detailsHTML += state.currentWord.antonyms.map(ant => '<span class="antonym-tag">' + ant + '</span>').join('');
                detailsHTML += '</div>';
            }}
            
            if (state.currentWord.sentences.length) {{
                detailsHTML += '<div class="detail-section"><span class="detail-title">Example:</span>';
                detailsHTML += '<div class="example-sentence">' + state.currentWord.sentences[0] + '</div></div>';
            }}
            
            detailsHTML += '</div>';
            details.innerHTML = detailsHTML;
            document.getElementById('classic-feedback-area').appendChild(details);
        }}
        
        function skipClassicQuestion() {{
            const state = gameStates.classic;
            state.totalQuestions++;
            state.currentStreak = 0;
            showClassicFeedback(false);
            updateClassicScores();
            disableClassicInputs();
        }}
        
        function disableClassicInputs() {{
            // Disable all choice options
            document.querySelectorAll('#classic-clues-area .choice-option').forEach(opt => {{
                opt.style.pointerEvents = 'none';
                opt.style.opacity = '0.7';
            }});
            document.getElementById('classic-submit-btn').disabled = true;
            document.getElementById('classic-hint-btn').disabled = true;
            document.getElementById('classic-skip-btn').disabled = true;
        }}
        
        function updateClassicScores() {{
            const state = gameStates.classic;
            document.getElementById('classic-correct').textContent = state.correctAnswers;
            document.getElementById('classic-total').textContent = state.totalQuestions;
            document.getElementById('classic-streak').textContent = state.currentStreak;
        }}
        
        // Speed Mode Functions
        function initializeSpeedMode() {{
            document.getElementById('speed-start-btn').addEventListener('click', startSpeedChallenge);
            document.getElementById('speed-skip-btn').addEventListener('click', skipSpeedQuestion);
            
            // Add keyboard support for A, B, C, D keys
            document.addEventListener('keydown', (e) => {{
                if (!gameStates.speed.isActive || activeTab !== 'speed') return;
                
                const key = e.key.toUpperCase();
                if (['A', 'B', 'C', 'D'].includes(key)) {{
                    const options = document.querySelectorAll('#speed-feedback-area .choice-option');
                    const index = key.charCodeAt(0) - 65; // A=0, B=1, C=2, D=3
                    if (options[index]) {{
                        const answer = options[index].dataset.answer;
                        selectSpeedAnswer(answer);
                    }}
                }}
            }});
        }}
        
        function startSpeedChallenge() {{
            const state = gameStates.speed;
            state.timeLeft = state.totalTime;
            state.correctAnswers = 0;
            state.totalQuestions = 0;
            state.isActive = true;
            state.startTime = Date.now();
            
            document.getElementById('speed-start-btn').disabled = true;
            document.getElementById('speed-skip-btn').disabled = false;
            document.getElementById('speed-answer-input').style.display = 'none'; // Hide text input
            
            generateSpeedQuestion();
            
            state.timer = setInterval(() => {{
                state.timeLeft--;
                document.getElementById('speed-timer').textContent = state.timeLeft;
                document.getElementById('speed-progress').style.width = (state.timeLeft / state.totalTime * 100) + '%';
                
                if (state.timeLeft <= 0) {{
                    endSpeedChallenge();
                }}
            }}, 1000);
        }}
        
        function generateSpeedQuestion() {{
            const state = gameStates.speed;
            if (!state.isActive) return;
            
            const currentWord = gameData[Math.floor(Math.random() * gameData.length)];
            state.currentWord = currentWord;
            
            // Random question type for variety
            const questionTypes = ['word-to-meaning', 'meaning-to-word'];
            const questionType = questionTypes[Math.floor(Math.random() * questionTypes.length)];
            state.questionType = questionType;
            
            let options = [];
            let correctAnswer = '';
            
            const questionElement = document.getElementById('speed-question');
            if (questionType === 'word-to-meaning') {{
                // Show 4 meanings
                const wrongMeanings = gameData
                    .filter(w => w.word !== currentWord.word && w.meaning.length > 10)
                    .sort(() => Math.random() - 0.5)
                    .slice(0, 3)
                    .map(w => w.meaning);
                options = [...wrongMeanings, currentWord.meaning].sort(() => Math.random() - 0.5);
                correctAnswer = currentWord.meaning;
                questionElement.innerHTML = '<strong>What does "' + currentWord.word + '" mean?</strong>';
            }} else {{
                // Show 4 words
                const wrongWords = gameData
                    .filter(w => w.word !== currentWord.word)
                    .sort(() => Math.random() - 0.5)
                    .slice(0, 3)
                    .map(w => w.word);
                options = [...wrongWords, currentWord.word].sort(() => Math.random() - 0.5);
                correctAnswer = currentWord.word;
                questionElement.innerHTML = '<strong>Which word means:</strong><br>"' + currentWord.meaning + '"';
            }}
            
            state.correctAnswer = correctAnswer;
            state.selectedAnswer = null;
            
            // Display options with letters A, B, C, D for speed
            displaySpeedOptions(options);
        }}
        
        function displaySpeedOptions(options) {{
            const optionsArea = document.getElementById('speed-feedback-area');
            optionsArea.innerHTML = '';
            
            const optionsContainer = document.createElement('div');
            optionsContainer.style.cssText = 'display: flex; flex-direction: column; gap: 8px; margin: 15px 0;';
            
            options.forEach((option, index) => {{
                const optionDiv = document.createElement('div');
                optionDiv.className = 'choice-option';
                optionDiv.style.cssText = `
                    background: #38a169;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 10px;
                    cursor: pointer;
                    font-size: 0.9em;
                    transition: all 0.2s ease;
                    text-align: left;
                `;
                
                const letter = String.fromCharCode(65 + index); // A, B, C, D
                optionDiv.textContent = letter + '. ' + option;
                optionDiv.dataset.answer = option;
                optionDiv.dataset.key = letter;
                
                optionDiv.onclick = function() {{
                    selectSpeedAnswer(option);
                }};
                
                optionsContainer.appendChild(optionDiv);
            }});
            
            optionsArea.appendChild(optionsContainer);
            
            // Add keyboard hint
            const keyboardHint = document.createElement('div');
            keyboardHint.style.cssText = 'text-align: center; color: #666; font-size: 0.8em; margin-top: 10px;';
            keyboardHint.textContent = 'Click or press A, B, C, D keys';
            optionsArea.appendChild(keyboardHint);
        }}
        
        function selectSpeedAnswer(answer) {{
            const state = gameStates.speed;
            if (!state.isActive) return;
            
            state.selectedAnswer = answer;
            checkSpeedAnswer();
        }}
        
        function checkSpeedAnswer() {{
            const state = gameStates.speed;
            if (!state.isActive || !state.selectedAnswer) return;
            
            const isCorrect = state.selectedAnswer === state.correctAnswer;
            
            state.totalQuestions++;
            if (isCorrect) {{
                state.correctAnswers++;
                showSpeedFeedback(true);
            }} else {{
                showSpeedFeedback(false);
            }}
            
            updateSpeedScores();
            
            setTimeout(() => {{
                if (state.isActive) {{
                    generateSpeedQuestion();
                }}
            }}, 800);
        }}
        
        function skipSpeedQuestion() {{
            const state = gameStates.speed;
            if (!state.isActive) return;
            
            state.totalQuestions++;
            generateSpeedQuestion();
        }}
        
        function showSpeedFeedback(correct) {{
            const feedback = document.createElement('div');
            feedback.className = 'feedback ' + (correct ? 'correct' : 'incorrect');
            feedback.style.padding = '10px';
            feedback.style.margin = '10px 0';
            
            if (correct) {{
                feedback.innerHTML = '✅ Correct!';
            }} else {{
                feedback.innerHTML = '❌ Wrong';
            }}
            
            document.getElementById('speed-feedback-area').innerHTML = '';
            document.getElementById('speed-feedback-area').appendChild(feedback);
        }}
        
        function updateSpeedScores() {{
            const state = gameStates.speed;
            document.getElementById('speed-correct').textContent = state.correctAnswers;
            document.getElementById('speed-total').textContent = state.totalQuestions;
            
            // Calculate WPM (Words Per Minute)
            const elapsedMinutes = (Date.now() - state.startTime) / 1000 / 60;
            const wpm = Math.round(state.correctAnswers / Math.max(elapsedMinutes, 0.1));
            document.getElementById('speed-wpm').textContent = wpm;
        }}
        
        function endSpeedChallenge() {{
            const state = gameStates.speed;
            state.isActive = false;
            clearInterval(state.timer);
            
            document.getElementById('speed-start-btn').disabled = false;
            document.getElementById('speed-skip-btn').disabled = true;
            document.getElementById('speed-answer-input').style.display = 'none';
            
            const finalScore = Math.round((state.correctAnswers / Math.max(state.totalQuestions, 1)) * 100);
            
            const feedback = document.createElement('div');
            feedback.className = 'feedback correct';
            feedback.innerHTML = '<h3>⚡ Speed Challenge Complete!</h3>' +
                '<p><strong>Score:</strong> ' + state.correctAnswers + '/' + state.totalQuestions + ' (' + finalScore + '%)</p>' +
                '<p><strong>Speed:</strong> ' + document.getElementById('speed-wpm').textContent + ' WPM</p>' +
                '<p>Great job! Click "Start Speed Challenge" to try again.</p>';
            
            document.getElementById('speed-feedback-area').innerHTML = '';
            document.getElementById('speed-feedback-area').appendChild(feedback);
        }}
        
        // Quiz Mode Functions
        function initializeQuizMode() {{
            document.getElementById('quiz-start-btn').addEventListener('click', startQuiz);
            document.getElementById('quiz-next-btn').addEventListener('click', nextQuizQuestion);
        }}
        
        function startQuiz() {{
            const state = gameStates.quiz;
            state.currentQuestion = 0;
            state.correctAnswers = 0;
            state.questions = [];
            state.isActive = true;
            
            // Generate 10 random questions
            const shuffledWords = [...gameData].sort(() => Math.random() - 0.5).slice(0, 10);
            
            shuffledWords.forEach(word => {{
                // Create multiple choice options
                const wrongOptions = gameData
                    .filter(w => w.word !== word.word)
                    .sort(() => Math.random() - 0.5)
                    .slice(0, 3)
                    .map(w => w.meaning);
                
                const options = [...wrongOptions, word.meaning].sort(() => Math.random() - 0.5);
                
                state.questions.push({{
                    word: word.word,
                    correctMeaning: word.meaning,
                    options: options,
                    userAnswer: null,
                    isCorrect: false
                }});
            }});
            
            document.getElementById('quiz-start-btn').style.display = 'none';
            document.getElementById('quiz-next-btn').disabled = false;
            
            showQuizQuestion();
        }}
        
        function showQuizQuestion() {{
            const state = gameStates.quiz;
            const question = state.questions[state.currentQuestion];
            
            document.getElementById('quiz-question').innerHTML = 
                '<strong>Question ' + (state.currentQuestion + 1) + ' of 10:</strong><br>' +
                'What does "' + question.word + '" mean?';
            
            // Create options
            const optionsArea = document.getElementById('quiz-options-area');
            optionsArea.innerHTML = '';
            
            question.options.forEach((option, index) => {{
                const optionDiv = document.createElement('div');
                optionDiv.className = 'choice-option';
                optionDiv.style.margin = '10px 0';
                optionDiv.textContent = (index + 1) + '. ' + option;
                optionDiv.onclick = function() {{
                    // Clear previous selections
                    document.querySelectorAll('#quiz-options-area .choice-option').forEach(opt => {{
                        opt.classList.remove('selected');
                        opt.style.background = '#38a169';
                    }});
                    
                    // Mark this as selected
                    optionDiv.classList.add('selected');
                    optionDiv.style.background = '#2f855a';
                    
                    question.userAnswer = option;
                    question.isCorrect = option === question.correctMeaning;
                    
                    // Show immediate feedback
                    setTimeout(() => {{
                        showQuizFeedback(question.isCorrect, question.correctMeaning);
                    }}, 500);
                }};
                optionsArea.appendChild(optionDiv);
            }});
            
            // Update progress
            const progress = ((state.currentQuestion) / state.totalQuestions * 100);
            document.getElementById('quiz-progress-bar').style.width = progress + '%';
            document.getElementById('quiz-progress').textContent = (state.currentQuestion + 1) + '/10';
        }}
        
        function showQuizFeedback(correct, correctAnswer) {{
            const feedback = document.createElement('div');
            feedback.className = 'feedback ' + (correct ? 'correct' : 'incorrect');
            feedback.style.margin = '20px 0';
            
            if (correct) {{
                feedback.innerHTML = '✅ Correct! Well done!';
            }} else {{
                feedback.innerHTML = '❌ Incorrect. The correct answer was:<br><strong>' + correctAnswer + '</strong>';
            }}
            
            document.getElementById('quiz-feedback-area').innerHTML = '';
            document.getElementById('quiz-feedback-area').appendChild(feedback);
            
            // Disable options after answering
            document.querySelectorAll('#quiz-options-area .choice-option').forEach(opt => {{
                opt.style.pointerEvents = 'none';
                opt.style.opacity = '0.7';
            }});
        }}
        
        function nextQuizQuestion() {{
            const state = gameStates.quiz;
            
            // Count correct answer if applicable
            if (state.questions[state.currentQuestion] && state.questions[state.currentQuestion].isCorrect) {{
                state.correctAnswers++;
            }}
            
            state.currentQuestion++;
            
            if (state.currentQuestion >= state.totalQuestions) {{
                endQuiz();
            }} else {{
                document.getElementById('quiz-feedback-area').innerHTML = '';
                showQuizQuestion();
            }}
        }}
        
        function endQuiz() {{
            const state = gameStates.quiz;
            const score = Math.round((state.correctAnswers / state.totalQuestions) * 100);
            
            let grade = 'F';
            if (score >= 90) grade = 'A';
            else if (score >= 80) grade = 'B';
            else if (score >= 70) grade = 'C';
            else if (score >= 60) grade = 'D';
            
            document.getElementById('quiz-score').textContent = score + '%';
            document.getElementById('quiz-grade').textContent = grade;
            document.getElementById('quiz-progress-bar').style.width = '100%';
            
            const feedback = document.createElement('div');
            feedback.className = 'feedback correct';
            feedback.innerHTML = 
                '<h3>🧠 Quiz Complete!</h3>' +
                '<p><strong>Final Score:</strong> ' + state.correctAnswers + '/' + state.totalQuestions + ' (' + score + '%)</p>' +
                '<p><strong>Grade:</strong> ' + grade + '</p>' +
                '<p>' + (score >= 80 ? 'Excellent work! 🏆' : score >= 60 ? 'Good job! Keep practicing! 📚' : 'Keep studying and try again! 💪') + '</p>';
            
            document.getElementById('quiz-question').innerHTML = 'Quiz Completed!';
            document.getElementById('quiz-options-area').innerHTML = '';
            document.getElementById('quiz-feedback-area').innerHTML = '';
            document.getElementById('quiz-feedback-area').appendChild(feedback);
            
            document.getElementById('quiz-start-btn').style.display = 'inline-block';
            document.getElementById('quiz-next-btn').disabled = true;
        }}
        
        // Memory Game Functions
        function initializeMemoryMode() {{
            document.getElementById('memory-start-btn').addEventListener('click', startMemoryGame);
            document.getElementById('memory-shuffle-btn').addEventListener('click', shuffleMemoryCards);
        }}
        
        function startMemoryGame() {{
            const state = gameStates.memory;
            state.cards = [];
            state.flippedCards = [];
            state.matchedPairs = 0;
            state.attempts = 0;
            state.startTime = Date.now();
            state.isActive = true;
            
            // Select 8 random words for 16 cards (8 pairs)
            const selectedWords = gameData.sort(() => Math.random() - 0.5).slice(0, 8);
            
            // Create card pairs (word and meaning)
            selectedWords.forEach(word => {{
                state.cards.push({{
                    id: 'word-' + word.word,
                    type: 'word',
                    content: word.word,
                    pair: word.word,
                    isFlipped: false,
                    isMatched: false
                }});
                
                state.cards.push({{
                    id: 'meaning-' + word.word,
                    type: 'meaning',
                    content: word.meaning.length > 50 ? word.meaning.substring(0, 50) + '...' : word.meaning,
                    pair: word.word,
                    isFlipped: false,
                    isMatched: false
                }});
            }});
            
            // Shuffle cards
            state.cards = state.cards.sort(() => Math.random() - 0.5);
            
            document.getElementById('memory-start-btn').disabled = true;
            document.getElementById('memory-shuffle-btn').disabled = false;
            
            renderMemoryGrid();
            
            // Start timer
            state.timer = setInterval(updateMemoryTimer, 1000);
        }}
        
        function renderMemoryGrid() {{
            const state = gameStates.memory;
            const grid = document.getElementById('memory-grid');
            grid.innerHTML = '';
            
            state.cards.forEach((card, index) => {{
                const cardElement = document.createElement('div');
                cardElement.className = 'memory-card';
                let cardBg = '#667eea';
                let cardColor = 'white';
                let cardCursor = 'pointer';
                let cardBorder = 'transparent';
                
                if (card.isMatched) {{
                    cardBg = '#c6f6d5';
                    cardColor = '#22543d';
                    cardCursor = 'default';
                    cardBorder = '#38a169';
                }} else if (card.isFlipped) {{
                    cardBg = '#bee3f8';
                    cardColor = '#2a4365';
                }}
                
                cardElement.style.cssText = 
                    'background: ' + cardBg + ';' +
                    'color: ' + cardColor + ';' +
                    'padding: 15px;' +
                    'border-radius: 10px;' +
                    'text-align: center;' +
                    'cursor: ' + cardCursor + ';' +
                    'min-height: 80px;' +
                    'display: flex;' +
                    'align-items: center;' +
                    'justify-content: center;' +
                    'font-size: 0.9em;' +
                    'border: 2px solid ' + cardBorder + ';' +
                    'transition: all 0.3s ease;';
                
                if (card.isFlipped || card.isMatched) {{
                    cardElement.textContent = card.content;
                }} else {{
                    cardElement.innerHTML = '<strong>?</strong>';
                }}
                
                cardElement.onclick = () => flipMemoryCard(index);
                grid.appendChild(cardElement);
            }});
        }}
        
        function flipMemoryCard(index) {{
            const state = gameStates.memory;
            const card = state.cards[index];
            
            if (!state.isActive || card.isFlipped || card.isMatched || state.flippedCards.length >= 2) {{
                return;
            }}
            
            card.isFlipped = true;
            state.flippedCards.push(index);
            
            renderMemoryGrid();
            
            if (state.flippedCards.length === 2) {{
                state.attempts++;
                updateMemoryScores();
                
                setTimeout(() => {{
                    checkMemoryMatch();
                }}, 1000);
            }}
        }}
        
        function checkMemoryMatch() {{
            const state = gameStates.memory;
            const [index1, index2] = state.flippedCards;
            const card1 = state.cards[index1];
            const card2 = state.cards[index2];
            
            if (card1.pair === card2.pair) {{
                // Match found!
                card1.isMatched = true;
                card2.isMatched = true;
                state.matchedPairs++;
                
                showMemoryFeedback(true, card1.pair);
                
                if (state.matchedPairs === 8) {{
                    endMemoryGame();
                }}
            }} else {{
                // No match
                card1.isFlipped = false;
                card2.isFlipped = false;
                showMemoryFeedback(false);
            }}
            
            state.flippedCards = [];
            renderMemoryGrid();
        }}
        
        function showMemoryFeedback(match, word = '') {{
            const feedback = document.createElement('div');
            feedback.className = 'feedback ' + (match ? 'correct' : 'incorrect');
            feedback.style.padding = '10px';
            feedback.style.margin = '10px 0';
            
            if (match) {{
                feedback.innerHTML = '✅ Match found: ' + word + '!';
            }} else {{
                feedback.innerHTML = '❌ No match. Try again!';
            }}
            
            document.getElementById('memory-feedback-area').innerHTML = '';
            document.getElementById('memory-feedback-area').appendChild(feedback);
            
            setTimeout(() => {{
                document.getElementById('memory-feedback-area').innerHTML = '';
            }}, 2000);
        }}
        
        function updateMemoryTimer() {{
            const state = gameStates.memory;
            if (!state.isActive) return;
            
            const elapsed = Math.floor((Date.now() - state.startTime) / 1000);
            document.getElementById('memory-time').textContent = elapsed + 's';
        }}
        
        function updateMemoryScores() {{
            const state = gameStates.memory;
            document.getElementById('memory-matches').textContent = state.matchedPairs;
            document.getElementById('memory-attempts').textContent = state.attempts;
        }}
        
        function shuffleMemoryCards() {{
            const state = gameStates.memory;
            state.cards = state.cards.sort(() => Math.random() - 0.5);
            renderMemoryGrid();
        }}
        
        function endMemoryGame() {{
            const state = gameStates.memory;
            state.isActive = false;
            clearInterval(state.timer);
            
            const finalTime = Math.floor((Date.now() - state.startTime) / 1000);
            const efficiency = Math.round((8 / state.attempts) * 100);
            
            const feedback = document.createElement('div');
            feedback.className = 'feedback correct';
            feedback.innerHTML = 
                '<h3>🧩 Memory Game Complete!</h3>' +
                '<p><strong>Time:</strong> ' + finalTime + ' seconds</p>' +
                '<p><strong>Attempts:</strong> ' + state.attempts + '</p>' +
                '<p><strong>Efficiency:</strong> ' + efficiency + '%</p>' +
                '<p>' + (efficiency >= 80 ? 'Perfect memory! 🧠' : efficiency >= 60 ? 'Great job! 👍' : 'Good effort! Keep practicing! 💪') + '</p>';
            
            document.getElementById('memory-feedback-area').innerHTML = '';
            document.getElementById('memory-feedback-area').appendChild(feedback);
            
            document.getElementById('memory-start-btn').disabled = false;
            document.getElementById('memory-shuffle-btn').disabled = true;
        }}
        
        // Word Battle Functions
        function initializeBattleMode() {{
            document.getElementById('battle-start-btn').addEventListener('click', startWordBattle);
            document.getElementById('battle-surrender-btn').addEventListener('click', endWordBattle);
        }}
        
        function startWordBattle() {{
            const state = gameStates.battle;
            state.level = 1;
            state.lives = 3;
            state.score = 0;
            state.timeLeft = 10;
            state.isActive = true;
            state.currentWord = null;
            
            document.getElementById('battle-start-btn').disabled = true;
            document.getElementById('battle-surrender-btn').disabled = false;
            document.getElementById('battle-answer-input').style.display = 'none'; // Hide text input
            
            updateBattleUI();
            generateBattleQuestion();
            startBattleTimer();
        }}
        
        function generateBattleQuestion() {{
            const state = gameStates.battle;
            if (!state.isActive) return;
            
            // Filter words by level difficulty
            let filteredWords = gameData;
            if (state.level <= 3) {{
                filteredWords = gameData.filter(w => w.word.length <= 7);
            }} else if (state.level <= 6) {{
                filteredWords = gameData.filter(w => w.word.length <= 10);
            }} else {{
                filteredWords = gameData.filter(w => w.word.length > 8);
            }}
            
            state.currentWord = filteredWords[Math.floor(Math.random() * filteredWords.length)];
            
            // Random question type
            const questionTypes = ['word-to-meaning', 'meaning-to-word'];
            const questionType = questionTypes[Math.floor(Math.random() * questionTypes.length)];
            state.questionType = questionType;
            
            let options = [];
            let correctAnswer = '';
            
            const questionElement = document.getElementById('battle-question');
            if (questionType === 'word-to-meaning') {{
                // Show 4 meanings
                const wrongMeanings = gameData
                    .filter(w => w.word !== state.currentWord.word && w.meaning.length > 10)
                    .sort(() => Math.random() - 0.5)
                    .slice(0, 3)
                    .map(w => w.meaning);
                options = [...wrongMeanings, state.currentWord.meaning].sort(() => Math.random() - 0.5);
                correctAnswer = state.currentWord.meaning;
                questionElement.innerHTML = '<strong>Level ' + state.level + ':</strong><br>What does "' + state.currentWord.word + '" mean?';
            }} else {{
                // Show 4 words
                const wrongWords = gameData
                    .filter(w => w.word !== state.currentWord.word)
                    .sort(() => Math.random() - 0.5)
                    .slice(0, 3)
                    .map(w => w.word);
                options = [...wrongWords, state.currentWord.word].sort(() => Math.random() - 0.5);
                correctAnswer = state.currentWord.word;
                questionElement.innerHTML = '<strong>Level ' + state.level + ':</strong><br>Which word means: "' + state.currentWord.meaning + '"?';
            }}
            
            state.correctAnswer = correctAnswer;
            state.selectedAnswer = null;
            
            // Display options for battle mode
            displayBattleOptions(options);
            
            // Adjust timer based on level
            state.timeLeft = Math.max(8 - Math.floor(state.level / 3), 5);
            updateBattleUI();
        }}
        
        function displayBattleOptions(options) {{
            const optionsArea = document.getElementById('battle-feedback-area');
            optionsArea.innerHTML = '';
            
            const optionsContainer = document.createElement('div');
            optionsContainer.style.cssText = 'display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 15px 0;';
            
            options.forEach((option, index) => {{
                const optionDiv = document.createElement('div');
                optionDiv.className = 'choice-option';
                optionDiv.style.cssText = `
                    background: #667eea;
                    color: white;
                    padding: 10px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 0.85em;
                    transition: all 0.2s ease;
                    text-align: center;
                    border: 2px solid transparent;
                `;
                
                const letter = String.fromCharCode(65 + index); // A, B, C, D
                optionDiv.innerHTML = '<strong>' + letter + '</strong><br>' + (option.length > 40 ? option.substring(0, 40) + '...' : option);
                optionDiv.dataset.answer = option;
                
                optionDiv.onclick = function() {{
                    if (!gameStates.battle.isActive) return;
                    
                    // Visual feedback
                    document.querySelectorAll('#battle-feedback-area .choice-option').forEach(opt => {{
                        opt.style.background = '#667eea';
                        opt.style.border = '2px solid transparent';
                    }});
                    optionDiv.style.background = '#5a67d8';
                    optionDiv.style.border = '2px solid #4c51bf';
                    
                    gameStates.battle.selectedAnswer = option;
                    
                    // Auto-submit after selection
                    setTimeout(() => {{
                        checkBattleAnswer();
                    }}, 300);
                }};
                
                optionsContainer.appendChild(optionDiv);
            }});
            
            optionsArea.appendChild(optionsContainer);
        }}
        
        function startBattleTimer() {{
            const state = gameStates.battle;
            
            state.timer = setInterval(() => {{
                state.timeLeft--;
                updateBattleUI();
                
                if (state.timeLeft <= 0) {{
                    // Time's up - lose a life
                    loseLife();
                }}
            }}, 1000);
        }}
        
        function checkBattleAnswer() {{
            const state = gameStates.battle;
            if (!state.isActive || !state.selectedAnswer) return;
            
            const isCorrect = state.selectedAnswer === state.correctAnswer;
            
            if (isCorrect) {{
                // Correct answer
                state.score += state.level * 10;
                state.level++;
                showBattleFeedback(true);
                
                setTimeout(() => {{
                    if (state.isActive) {{
                        generateBattleQuestion();
                        startBattleTimer();
                    }}
                }}, 1000);
            }} else {{
                // Wrong answer
                loseLife();
            }}
            
            clearInterval(state.timer);
        }}
        
        function loseLife() {{
            const state = gameStates.battle;
            state.lives--;
            
            showBattleFeedback(false);
            
            if (state.lives <= 0) {{
                endWordBattle();
            }} else {{
                setTimeout(() => {{
                    if (state.isActive) {{
                        generateBattleQuestion();
                        startBattleTimer();
                    }}
                }}, 1500);
            }}
        }}
        
        function showBattleFeedback(correct) {{
            const feedback = document.createElement('div');
            feedback.className = 'feedback ' + (correct ? 'correct' : 'incorrect');
            feedback.style.padding = '10px';
            feedback.style.margin = '10px 0';
            
            if (correct) {{
                feedback.innerHTML = '✅ Correct! +' + (gameStates.battle.level * 10) + ' points!';
            }} else {{
                feedback.innerHTML = '❌ Wrong! The answer was: ' + 
                    (gameStates.battle.questionType === 'word-to-meaning' ? gameStates.battle.currentWord.meaning : gameStates.battle.currentWord.word);
            }}
            
            document.getElementById('battle-feedback-area').innerHTML = '';
            document.getElementById('battle-feedback-area').appendChild(feedback);
        }}
        
        function updateBattleUI() {{
            const state = gameStates.battle;
            document.getElementById('battle-level').textContent = state.level;
            document.getElementById('battle-lives').textContent = '❤️'.repeat(state.lives);
            document.getElementById('battle-score').textContent = state.score;
            document.getElementById('battle-timer').textContent = state.timeLeft;
            
            // Change timer color based on urgency
            const timerElement = document.getElementById('battle-timer');
            if (state.timeLeft <= 3) {{
                timerElement.style.color = '#e53e3e';
            }} else if (state.timeLeft <= 5) {{
                timerElement.style.color = '#ed8936';
            }} else {{
                timerElement.style.color = '#48bb78';
            }}
        }}
        
        function endWordBattle() {{
            const state = gameStates.battle;
            state.isActive = false;
            clearInterval(state.timer);
            
            document.getElementById('battle-start-btn').disabled = false;
            document.getElementById('battle-surrender-btn').disabled = true;
            document.getElementById('battle-answer-input').style.display = 'none';
            
            let rank = 'Novice';
            if (state.score >= 500) rank = 'Master';
            else if (state.score >= 300) rank = 'Expert';
            else if (state.score >= 150) rank = 'Advanced';
            else if (state.score >= 50) rank = 'Intermediate';
            
            const feedback = document.createElement('div');
            feedback.className = 'feedback correct';
            feedback.innerHTML = 
                '<h3>⚔️ Battle Over!</h3>' +
                '<p><strong>Final Score:</strong> ' + state.score + ' points</p>' +
                '<p><strong>Level Reached:</strong> ' + (state.level - 1) + '</p>' +
                '<p><strong>Rank:</strong> ' + rank + '</p>' +
                '<p>' + (state.score >= 300 ? 'Legendary warrior! 🏆' : state.score >= 100 ? 'Brave fighter! ⚔️' : 'Keep training, warrior! 💪') + '</p>';
            
            document.getElementById('battle-question').innerHTML = 'Battle Complete!';
            document.getElementById('battle-feedback-area').innerHTML = '';
            document.getElementById('battle-feedback-area').appendChild(feedback);
        }}
    </script>
</body>
</html>"""
    
    return html_content

def main():
    """Main function to generate the multi-game interface."""
    input_file = "enrichedpdfplan.txt"
    output_file = "word_games_collection.html"
    
    if not Path(input_file).exists():
        print(f"❌ Error: Input file '{input_file}' not found!")
        return
    
    print("🎮 Generating Word Games Collection...")
    
    # Read and parse the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = re.split(r'\n-{25,}\n', content)
    
    words_data = []
    print(f"Processing {len(entries)} entries...")
    
    for i, entry in enumerate(entries):
        if entry.strip():
            try:
                word_data = parse_word_entry(entry)
                if word_data['word'] and word_data['meaning']:
                    words_data.append(word_data)
            except Exception as e:
                print(f"Error processing entry {i}: {e}")
                continue
    
    print(f"Successfully processed {len(words_data)} words")
    
    # Generate the multi-game HTML
    html_content = create_multi_game_html(words_data)
    
    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Word Games Collection created!")
    print(f"📁 Output file: {output_file}")
    print(f"🎮 Open the file in your browser to play!")
    print(f"🎯 Features:")
    print(f"   📚 Classic Mode - Original word master with hints")
    print(f"   ⚡ Speed Challenge - 60-second vocabulary race")
    print(f"   🧠 Quiz Master - Comprehensive vocabulary tests")
    print(f"   🧩 Memory Game - Match words with meanings")
    print(f"   ⚔️ Word Battle - Survival vocabulary challenge")

if __name__ == "__main__":
    main()