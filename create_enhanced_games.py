#!/usr/bin/env python3
"""
Create enhanced word games with detailed explanations including origin data
"""

import json
from pathlib import Path

def create_enhanced_html():
    """Create enhanced HTML with detailed word explanations."""
    
    # Read the JavaScript data
    with open('game_words_data.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Extract just the JSON data
    start_marker = 'const gameData = '
    end_marker = ';\n\n// Export for Node.js'
    
    start_idx = js_content.find(start_marker) + len(start_marker)
    end_idx = js_content.find(end_marker)
    
    json_data = js_content[start_idx:end_idx]
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Enhanced Word Games - Full Explanations</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .game-container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 10px;
        }}
        
        .game-header {{
            text-align: center;
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .game-title {{
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 8px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        }}
        
        .game-subtitle {{
            font-size: 1.1em;
            color: #666;
        }}
        
        .word-count {{
            font-size: 0.9em;
            color: #888;
            margin-top: 5px;
        }}
        
        .tab-container {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .tab-nav {{
            display: flex;
            background: #f8f9fa;
            flex-wrap: wrap;
            justify-content: center;
        }}
        
        .tab-btn {{
            flex: 1;
            min-width: 100px;
            padding: 12px 8px;
            background: none;
            border: none;
            font-size: 0.8em;
            font-weight: bold;
            color: #666;
            cursor: pointer;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
            font-family: inherit;
            user-select: none;
        }}
        
        .tab-btn:hover {{ background: #e9ecef; color: #333; }}
        .tab-btn.active {{ color: #667eea; background: white; border-bottom-color: #667eea; }}
        .tab-btn:active {{ transform: scale(0.95); }}
        
        .tab-icon {{ font-size: 1.1em; margin-bottom: 2px; display: block; }}
        .tab-label {{ font-size: 0.75em; display: block; }}
        
        .tab-content {{ display: none; padding: 20px; }}
        .tab-content.active {{ display: block; }}
        
        .game-description {{
            background: linear-gradient(135deg, #e8f5e8 0%, #c6f6d5 100%);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #38a169;
        }}
        
        .question-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            font-size: 1.2em;
            text-align: center;
            line-height: 1.5;
        }}
        
        .choice-option {{
            background: #38a169;
            color: white;
            padding: 15px;
            margin: 8px 0;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            border: 2px solid transparent;
            font-size: 1em;
            line-height: 1.4;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
        }}
        
        .choice-option:hover {{ background: #2f855a; transform: translateY(-2px); }}
        .choice-option:active {{ transform: scale(0.98); }}
        .choice-option.selected {{ background: #2f855a; border-color: #22543d; }}
        
        .score-board {{
            display: flex;
            justify-content: space-around;
            background: #f7fafc;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .score-item {{ text-align: center; flex: 1; min-width: 70px; }}
        .score-number {{ font-size: 1.6em; font-weight: bold; color: #667eea; }}
        .score-label {{ color: #666; font-size: 0.8em; }}
        
        .btn-group {{
            display: flex;
            gap: 8px;
            justify-content: center;
            margin: 15px 0;
            flex-wrap: wrap;
        }}
        
        .game-btn {{
            padding: 10px 18px;
            font-size: 0.9em;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-family: inherit;
            transition: all 0.3s ease;
            font-weight: bold;
            min-width: 110px;
            user-select: none;
        }}
        
        .game-btn:active {{ transform: scale(0.95); }}
        .primary-btn {{ background: #667eea; color: white; }}
        .primary-btn:hover {{ background: #5a67d8; }}
        
        .feedback {{
            padding: 15px;
            border-radius: 12px;
            margin: 15px 0;
            font-size: 1.1em;
            font-weight: bold;
            text-align: center;
        }}
        
        .correct {{ background: #c6f6d5; color: #22543d; border: 2px solid #38a169; }}
        .incorrect {{ background: #fed7d7; color: #742a2a; border: 2px solid #e53e3e; }}
        
        .word-explanation {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 12px;
            margin: 15px 0;
            text-align: left;
            border: 2px solid #e2e8f0;
        }}
        
        .word-title {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 15px;
            text-align: center;
        }}
        
        .explanation-section {{
            margin: 12px 0;
            padding: 10px;
            background: white;
            border-radius: 8px;
        }}
        
        .section-title {{
            font-weight: bold;
            color: #4a5568;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .section-content {{
            color: #2d3748;
            line-height: 1.5;
        }}
        
        .synonym-tag, .antonym-tag {{
            display: inline-block;
            padding: 4px 8px;
            margin: 2px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 500;
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
            background: #edf2f7;
            padding: 10px;
            border-radius: 6px;
            font-style: italic;
            border-left: 3px solid #667eea;
            margin: 5px 0;
        }}
        
        .origin-box {{
            background: linear-gradient(135deg, #fef5e7 0%, #fed7aa 100%);
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #f6ad55;
        }}
        
        .timer-display {{
            font-size: 2em;
            font-weight: bold;
            text-align: center;
            margin: 15px 0;
            color: #48bb78;
        }}
        
        .progress-bar {{
            background: #e2e8f0;
            border-radius: 25px;
            overflow: hidden;
            height: 8px;
            margin: 15px 0;
        }}
        
        .progress-fill {{
            background: linear-gradient(90deg, #48bb78, #38a169);
            height: 100%;
            transition: width 0.3s ease;
        }}
        
        .battle-area {{
            display: flex;
            justify-content: space-between;
            gap: 15px;
            margin: 20px 0;
        }}
        
        .player-card {{
            flex: 1;
            background: #f7fafc;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            border: 2px solid #e2e8f0;
        }}
        
        .player-card.active {{
            border-color: #667eea;
            background: #edf2f7;
        }}
        
        .player-name {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .endurance-stats {{
            background: #f7fafc;
            padding: 15px;
            border-radius: 12px;
            margin: 15px 0;
        }}
        
        .stat-row {{
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
        }}
        
        /* Mobile Responsive */
        @media (max-width: 768px) {{
            .game-container {{ padding: 5px; }}
            .game-header {{ padding: 15px; margin-bottom: 15px; }}
            .tab-content {{ padding: 15px; }}
            .game-title {{ font-size: 2em; }}
            .tab-btn {{ padding: 10px 6px; font-size: 0.75em; min-width: 80px; }}
            .question-card {{ padding: 15px; font-size: 1em; }}
            .choice-option {{ padding: 12px; font-size: 0.9em; min-height: 50px; }}
            .game-btn {{ padding: 10px 15px; min-width: 100px; font-size: 0.85em; }}
            .battle-area {{ flex-direction: column; }}
            .word-explanation {{ padding: 15px; }}
            .word-title {{ font-size: 1.3em; }}
        }}
        
        @media (max-width: 480px) {{
            .game-title {{ font-size: 1.5em; }}
            .tab-btn {{ flex-basis: 32%; margin: 1px; }}
        }}
        
        @media (hover: none) and (pointer: coarse) {{
            .choice-option {{ min-height: 60px; padding: 15px; }}
            .game-btn {{ min-height: 45px; padding: 12px 18px; }}
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-header">
            <h1 class="game-title">🎮 Enhanced Word Games</h1>
            <p class="game-subtitle">Complete Vocabulary Learning with Detailed Explanations</p>
            <div class="word-count">📚 4,963 Words • 🌍 Origins • 📖 Full Explanations</div>
        </div>
        
        <div class="tab-container">
            <div class="tab-nav">
                <button class="tab-btn active" data-tab="classic">
                    <span class="tab-icon">📚</span>
                    <span class="tab-label">Classic</span>
                </button>
                <button class="tab-btn" data-tab="speed">
                    <span class="tab-icon">⚡</span>
                    <span class="tab-label">Speed</span>
                </button>
                <button class="tab-btn" data-tab="quiz">
                    <span class="tab-icon">🧠</span>
                    <span class="tab-label">Quiz</span>
                </button>
                <button class="tab-btn" data-tab="battle">
                    <span class="tab-icon">⚔️</span>
                    <span class="tab-label">Battle</span>
                </button>
                <button class="tab-btn" data-tab="endurance">
                    <span class="tab-icon">🏃</span>
                    <span class="tab-label">Endure</span>
                </button>
            </div>
            
            <!-- Classic Mode -->
            <div class="tab-content active" id="classic-tab">
                <div class="game-description">
                    <h3>📚 Classic Word Game</h3>
                    <p>Learn vocabulary with detailed explanations, origins, and examples after each answer.</p>
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
                
                <div class="question-card" id="classic-question">
                    Click "New Question" to start learning!
                </div>
                
                <div id="classic-options-area"></div>
                
                <div class="btn-group">
                    <button class="game-btn primary-btn" id="classic-submit" disabled>Submit Answer</button>
                    <button class="game-btn primary-btn" id="classic-new">New Question 🎲</button>
                </div>
                
                <div id="classic-feedback"></div>
            </div>
            
            <!-- Speed Challenge -->
            <div class="tab-content" id="speed-tab">
                <div class="game-description">
                    <h3>⚡ Speed Challenge</h3>
                    <p>Quick vocabulary test with instant explanations. Learn fast!</p>
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
                        <div class="score-label">Total</div>
                    </div>
                    <div class="score-item">
                        <div class="score-number" id="speed-wpm">0</div>
                        <div class="score-label">WPM</div>
                    </div>
                </div>
                
                <div class="question-card" id="speed-question">
                    Click "Start Speed Challenge" to begin!
                </div>
                
                <div id="speed-options-area"></div>
                
                <div class="btn-group">
                    <button class="game-btn primary-btn" id="speed-start">Start Challenge ⚡</button>
                </div>
                
                <div id="speed-feedback"></div>
            </div>
            
            <!-- Quiz Mode -->
            <div class="tab-content" id="quiz-tab">
                <div class="game-description">
                    <h3>🧠 Quiz Master</h3>
                    <p>Comprehensive 10-question test with detailed explanations for each word.</p>
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
                    Click "Start Quiz" to begin!
                </div>
                
                <div id="quiz-options-area"></div>
                
                <div class="btn-group">
                    <button class="game-btn primary-btn" id="quiz-start">Start Quiz 🧠</button>
                    <button class="game-btn primary-btn" id="quiz-next" disabled>Next Question →</button>
                </div>
                
                <div id="quiz-feedback"></div>
            </div>
            
            <!-- Word Battle -->
            <div class="tab-content" id="battle-tab">
                <div class="game-description">
                    <h3>⚔️ Word Battle</h3>
                    <p>Competitive learning! Each answer reveals detailed word information.</p>
                </div>
                
                <div class="battle-area">
                    <div class="player-card active" id="player1-card">
                        <div class="player-name">Player 1</div>
                        <div class="score-number" id="battle-p1-score">0</div>
                    </div>
                    <div class="player-card" id="player2-card">
                        <div class="player-name">Player 2</div>
                        <div class="score-number" id="battle-p2-score">0</div>
                    </div>
                </div>
                
                <div class="question-card" id="battle-question">
                    Click "Start Battle" to begin the learning battle!
                </div>
                
                <div id="battle-options-area"></div>
                
                <div class="btn-group">
                    <button class="game-btn primary-btn" id="battle-start">Start Battle ⚔️</button>
                    <button class="game-btn primary-btn" id="battle-reset">Reset Game 🔄</button>
                </div>
                
                <div id="battle-feedback"></div>
            </div>
            
            <!-- Endurance Mode -->
            <div class="tab-content" id="endurance-tab">
                <div class="game-description">
                    <h3>🏃 Endurance Mode</h3>
                    <p>Survival learning mode with comprehensive word explanations at every step!</p>
                </div>
                
                <div class="endurance-stats">
                    <div class="stat-row">
                        <span>Level:</span>
                        <span id="endurance-level">1</span>
                    </div>
                    <div class="stat-row">
                        <span>Lives:</span>
                        <span id="endurance-lives">❤️❤️❤️</span>
                    </div>
                    <div class="stat-row">
                        <span>Score:</span>
                        <span id="endurance-score">0</span>
                    </div>
                </div>
                
                <div class="question-card" id="endurance-question">
                    Click "Start Endurance" to test your vocabulary limits!
                </div>
                
                <div id="endurance-options-area"></div>
                
                <div class="btn-group">
                    <button class="game-btn primary-btn" id="endurance-start">Start Endurance 🏃</button>
                    <button class="game-btn primary-btn" id="endurance-restart">Restart 🔄</button>
                </div>
                
                <div id="endurance-feedback"></div>
            </div>
        </div>
    </div>

    <script>
        // Full word dataset with origins, sentences, and complete information
        const gameData = {json_data};
        
        let activeTab = 'classic';
        let gameStates = {{
            classic: {{ currentWord: null, correctAnswers: 0, totalQuestions: 0, currentStreak: 0, selectedAnswer: null, usedWords: [] }},
            speed: {{ timeLeft: 60, correctAnswers: 0, totalQuestions: 0, isActive: false, timer: null, startTime: null, usedWords: [] }},
            quiz: {{ currentQuestion: 0, correctAnswers: 0, questions: [], isActive: false, usedWords: [] }},
            battle: {{ currentPlayer: 1, player1Score: 0, player2Score: 0, currentWord: null, isActive: false, selectedAnswer: null, usedWords: [] }},
            endurance: {{ level: 1, lives: 3, score: 0, currentWord: null, isActive: false, selectedAnswer: null, usedWords: [] }}
        }};
        
        // Global shuffled word array
        let shuffledWords = [...gameData].sort(() => Math.random() - 0.5);
        let globalWordIndex = 0;
        
        function getNextWord() {{
            if (globalWordIndex >= shuffledWords.length) {{
                shuffledWords = [...gameData].sort(() => Math.random() - 0.5);
                globalWordIndex = 0;
                console.log("🔄 Reshuffled word database - starting fresh!");
            }}
            
            const word = shuffledWords[globalWordIndex];
            globalWordIndex++;
            return word;
        }}
        
        // Enhanced feedback with detailed word explanation
        function showDetailedFeedback(elementId, isCorrect, word, userAnswer) {{
            const feedback = document.createElement('div');
            feedback.className = 'feedback ' + (isCorrect ? 'correct' : 'incorrect');
            
            // Basic feedback
            if (isCorrect) {{
                feedback.innerHTML = '🎉 <strong>Excellent!</strong> You got it right!';
            }} else {{
                feedback.innerHTML = '❌ <strong>Not quite right.</strong><br>You selected: <em>' + userAnswer + '</em><br>Correct answer: <strong>' + word.meaning + '</strong>';
            }}
            
            const feedbackArea = document.getElementById(elementId);
            feedbackArea.innerHTML = '';
            feedbackArea.appendChild(feedback);
            
            // Add detailed word explanation
            setTimeout(() => {{
                showWordExplanation(elementId, word);
            }}, 1000);
        }}
        
        function showWordExplanation(elementId, word) {{
            const explanation = document.createElement('div');
            explanation.className = 'word-explanation';
            
            let explanationHTML = '<div class="word-title">📖 ' + word.word.toUpperCase() + '</div>';
            
            // Meaning
            explanationHTML += '<div class="explanation-section">';
            explanationHTML += '<div class="section-title">💭 Definition</div>';
            explanationHTML += '<div class="section-content">' + word.meaning + '</div>';
            explanationHTML += '</div>';
            
            // Synonyms
            if (word.synonyms && word.synonyms.length > 0) {{
                explanationHTML += '<div class="explanation-section">';
                explanationHTML += '<div class="section-title">🔗 Synonyms (Similar Words)</div>';
                explanationHTML += '<div class="section-content">';
                word.synonyms.forEach(syn => {{
                    explanationHTML += '<span class="synonym-tag">' + syn + '</span>';
                }});
                explanationHTML += '</div></div>';
            }}
            
            // Antonyms
            if (word.antonyms && word.antonyms.length > 0) {{
                explanationHTML += '<div class="explanation-section">';
                explanationHTML += '<div class="section-title">⚡ Antonyms (Opposite Words)</div>';
                explanationHTML += '<div class="section-content">';
                word.antonyms.forEach(ant => {{
                    explanationHTML += '<span class="antonym-tag">' + ant + '</span>';
                }});
                explanationHTML += '</div></div>';
            }}
            
            // Example sentences
            if (word.sentences && word.sentences.length > 0) {{
                explanationHTML += '<div class="explanation-section">';
                explanationHTML += '<div class="section-title">💬 Example Usage</div>';
                explanationHTML += '<div class="section-content">';
                word.sentences.forEach(sentence => {{
                    explanationHTML += '<div class="example-sentence">"' + sentence + '"</div>';
                }});
                explanationHTML += '</div></div>';
            }}
            
            // Origin/Etymology
            if (word.origin && word.origin.trim()) {{
                explanationHTML += '<div class="explanation-section">';
                explanationHTML += '<div class="section-title">🌍 Word Origin & Etymology</div>';
                explanationHTML += '<div class="section-content">';
                explanationHTML += '<div class="origin-box">' + word.origin + '</div>';
                explanationHTML += '</div></div>';
            }}
            
            explanation.innerHTML = explanationHTML;
            document.getElementById(elementId).appendChild(explanation);
        }}
        
        // Tab functionality
        document.querySelectorAll('.tab-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
                
                btn.classList.add('active');
                document.getElementById(btn.dataset.tab + '-tab').classList.add('active');
                activeTab = btn.dataset.tab;
            }});
        }});
        
        // Classic Mode
        document.getElementById('classic-new').addEventListener('click', generateClassicQuestion);
        document.getElementById('classic-submit').addEventListener('click', checkClassicAnswer);
        
        function generateClassicQuestion() {{
            const state = gameStates.classic;
            state.currentWord = getNextWord();
            state.selectedAnswer = null;
            
            document.getElementById('classic-feedback').innerHTML = '';
            document.getElementById('classic-submit').disabled = true;
            
            const wrongMeanings = [];
            const usedMeanings = new Set([state.currentWord.meaning]);
            
            let attempts = 0;
            while (wrongMeanings.length < 3 && attempts < 100) {{
                const randomWord = gameData[Math.floor(Math.random() * gameData.length)];
                if (!usedMeanings.has(randomWord.meaning)) {{
                    wrongMeanings.push(randomWord.meaning);
                    usedMeanings.add(randomWord.meaning);
                }}
                attempts++;
            }}
            
            const options = [...wrongMeanings, state.currentWord.meaning].sort(() => Math.random() - 0.5);
            state.correctAnswer = state.currentWord.meaning;
            
            document.getElementById('classic-question').innerHTML = '<strong>What does "' + state.currentWord.word + '" mean?</strong>';
            displayOptions('classic-options-area', options, (option) => {{
                state.selectedAnswer = option;
                document.getElementById('classic-submit').disabled = false;
            }});
        }}
        
        function checkClassicAnswer() {{
            const state = gameStates.classic;
            if (!state.selectedAnswer) return;
            
            const isCorrect = state.selectedAnswer === state.correctAnswer;
            state.totalQuestions++;
            
            if (isCorrect) {{
                state.correctAnswers++;
                state.currentStreak++;
            }} else {{
                state.currentStreak = 0;
            }}
            
            showDetailedFeedback('classic-feedback', isCorrect, state.currentWord, state.selectedAnswer);
            updateScores('classic');
            disableOptions('classic-options-area');
            document.getElementById('classic-submit').disabled = true;
        }}
        
        // Speed Challenge (shortened explanation due to time constraints)
        document.getElementById('speed-start').addEventListener('click', startSpeedChallenge);
        
        function startSpeedChallenge() {{
            const state = gameStates.speed;
            state.timeLeft = 60;
            state.correctAnswers = 0;
            state.totalQuestions = 0;
            state.isActive = true;
            state.startTime = Date.now();
            
            document.getElementById('speed-start').disabled = true;
            generateSpeedQuestion();
            
            state.timer = setInterval(() => {{
                state.timeLeft--;
                document.getElementById('speed-timer').textContent = state.timeLeft;
                document.getElementById('speed-progress').style.width = (state.timeLeft / 60 * 100) + '%';
                
                if (state.timeLeft <= 0) {{
                    endSpeedChallenge();
                }}
            }}, 1000);
        }}
        
        function generateSpeedQuestion() {{
            const state = gameStates.speed;
            if (!state.isActive) return;
            
            state.currentWord = getNextWord();
            
            const wrongMeanings = [];
            const usedMeanings = new Set([state.currentWord.meaning]);
            
            let attempts = 0;
            while (wrongMeanings.length < 3 && attempts < 50) {{
                const randomWord = gameData[Math.floor(Math.random() * gameData.length)];
                if (!usedMeanings.has(randomWord.meaning)) {{
                    wrongMeanings.push(randomWord.meaning);
                    usedMeanings.add(randomWord.meaning);
                }}
                attempts++;
            }}
            
            const options = [...wrongMeanings, state.currentWord.meaning].sort(() => Math.random() - 0.5);
            state.correctAnswer = state.currentWord.meaning;
            
            document.getElementById('speed-question').innerHTML = '<strong>What does "' + state.currentWord.word + '" mean?</strong>';
            displayOptions('speed-options-area', options, (option) => {{
                checkSpeedAnswer(option);
            }});
        }}
        
        function checkSpeedAnswer(selectedAnswer) {{
            const state = gameStates.speed;
            if (!state.isActive) return;
            
            const isCorrect = selectedAnswer === state.correctAnswer;
            state.totalQuestions++;
            if (isCorrect) state.correctAnswers++;
            
            // Quick feedback for speed mode
            const feedback = document.createElement('div');
            feedback.className = 'feedback ' + (isCorrect ? 'correct' : 'incorrect');
            feedback.innerHTML = isCorrect ? '✅ Correct!' : '❌ ' + state.currentWord.meaning;
            
            document.getElementById('speed-feedback').innerHTML = '';
            document.getElementById('speed-feedback').appendChild(feedback);
            
            updateScores('speed');
            
            setTimeout(() => {{
                if (state.isActive) {{
                    generateSpeedQuestion();
                    document.getElementById('speed-feedback').innerHTML = '';
                }}
            }}, 800);
        }}
        
        function endSpeedChallenge() {{
            const state = gameStates.speed;
            state.isActive = false;
            clearInterval(state.timer);
            
            const finalScore = Math.round((state.correctAnswers / Math.max(state.totalQuestions, 1)) * 100);
            
            const feedback = document.createElement('div');
            feedback.className = 'feedback correct';
            feedback.innerHTML = '<h3>⚡ Challenge Complete!</h3>' +
                '<p>Score: ' + state.correctAnswers + '/' + state.totalQuestions + ' (' + finalScore + '%)</p>' +
                '<p>Great job learning at speed! 🎯</p>';
            
            document.getElementById('speed-feedback').innerHTML = '';
            document.getElementById('speed-feedback').appendChild(feedback);
            document.getElementById('speed-start').disabled = false;
        }}
        
        // Quiz Mode with detailed explanations
        document.getElementById('quiz-start').addEventListener('click', startQuiz);
        document.getElementById('quiz-next').addEventListener('click', nextQuizQuestion);
        
        function startQuiz() {{
            const state = gameStates.quiz;
            state.currentQuestion = 0;
            state.correctAnswers = 0;
            state.questions = [];
            state.isActive = true;
            
            // Generate 10 unique questions
            for (let i = 0; i < 10; i++) {{
                const word = getNextWord();
                
                const wrongMeanings = [];
                const usedMeanings = new Set([word.meaning]);
                
                let attempts = 0;
                while (wrongMeanings.length < 3 && attempts < 50) {{
                    const randomWord = gameData[Math.floor(Math.random() * gameData.length)];
                    if (!usedMeanings.has(randomWord.meaning)) {{
                        wrongMeanings.push(randomWord.meaning);
                        usedMeanings.add(randomWord.meaning);
                    }}
                    attempts++;
                }}
                
                const options = [...wrongMeanings, word.meaning].sort(() => Math.random() - 0.5);
                
                state.questions.push({{
                    word: word.word,
                    correctMeaning: word.meaning,
                    options: options,
                    userAnswer: null,
                    isCorrect: false,
                    wordData: word
                }});
            }}
            
            document.getElementById('quiz-start').style.display = 'none';
            document.getElementById('quiz-next').disabled = false;
            showQuizQuestion();
        }}
        
        function showQuizQuestion() {{
            const state = gameStates.quiz;
            const question = state.questions[state.currentQuestion];
            
            document.getElementById('quiz-question').innerHTML = 
                '<strong>Question ' + (state.currentQuestion + 1) + ' of 10:</strong><br>' +
                'What does "' + question.word + '" mean?';
            
            displayOptions('quiz-options-area', question.options, (option) => {{
                question.userAnswer = option;
                question.isCorrect = option === question.correctMeaning;
                disableOptions('quiz-options-area');
                setTimeout(() => {{
                    showDetailedFeedback('quiz-feedback', question.isCorrect, question.wordData, question.userAnswer);
                }}, 500);
            }});
            
            const progress = ((state.currentQuestion) / 10 * 100);
            document.getElementById('quiz-progress-bar').style.width = progress + '%';
            document.getElementById('quiz-progress').textContent = (state.currentQuestion + 1) + '/10';
        }}
        
        function nextQuizQuestion() {{
            const state = gameStates.quiz;
            
            if (state.questions[state.currentQuestion] && state.questions[state.currentQuestion].isCorrect) {{
                state.correctAnswers++;
            }}
            
            state.currentQuestion++;
            
            if (state.currentQuestion >= 10) {{
                endQuiz();
            }} else {{
                document.getElementById('quiz-feedback').innerHTML = '';
                showQuizQuestion();
            }}
        }}
        
        function endQuiz() {{
            const state = gameStates.quiz;
            const score = Math.round((state.correctAnswers / 10) * 100);
            
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
            feedback.innerHTML = '<h3>🧠 Quiz Complete!</h3>' +
                '<p>Final Score: ' + state.correctAnswers + '/10 (' + score + '%)</p>' +
                '<p>Grade: ' + grade + '</p>' +
                '<p>' + (score >= 80 ? 'Excellent vocabulary knowledge! 🏆' : 'Keep learning with our detailed explanations! 📚') + '</p>';
            
            document.getElementById('quiz-feedback').innerHTML = '';
            document.getElementById('quiz-feedback').appendChild(feedback);
            
            document.getElementById('quiz-question').innerHTML = 'Quiz Completed!';
            document.getElementById('quiz-options-area').innerHTML = '';
            document.getElementById('quiz-start').style.display = 'inline-block';
            document.getElementById('quiz-next').disabled = true;
        }}
        
        // Battle Mode with explanations
        document.getElementById('battle-start').addEventListener('click', startBattle);
        document.getElementById('battle-reset').addEventListener('click', resetBattle);
        
        function startBattle() {{
            const state = gameStates.battle;
            state.currentPlayer = 1;
            state.player1Score = 0;
            state.player2Score = 0;
            state.isActive = true;
            
            updateBattleDisplay();
            generateBattleQuestion();
            document.getElementById('battle-start').disabled = true;
        }}
        
        function generateBattleQuestion() {{
            const state = gameStates.battle;
            if (!state.isActive) return;
            
            state.currentWord = getNextWord();
            state.selectedAnswer = null;
            
            const wrongMeanings = [];
            const usedMeanings = new Set([state.currentWord.meaning]);
            
            let attempts = 0;
            while (wrongMeanings.length < 3 && attempts < 50) {{
                const randomWord = gameData[Math.floor(Math.random() * gameData.length)];
                if (!usedMeanings.has(randomWord.meaning)) {{
                    wrongMeanings.push(randomWord.meaning);
                    usedMeanings.add(randomWord.meaning);
                }}
                attempts++;
            }}
            
            const options = [...wrongMeanings, state.currentWord.meaning].sort(() => Math.random() - 0.5);
            
            document.getElementById('battle-question').innerHTML = 
                '<strong>Player ' + state.currentPlayer + ', what does "' + state.currentWord.word + '" mean?</strong>';
            
            displayOptions('battle-options-area', options, (option) => {{
                checkBattleAnswer(option);
            }});
        }}
        
        function checkBattleAnswer(selectedAnswer) {{
            const state = gameStates.battle;
            const isCorrect = selectedAnswer === state.currentWord.meaning;
            
            if (isCorrect) {{
                if (state.currentPlayer === 1) {{
                    state.player1Score++;
                }} else {{
                    state.player2Score++;
                }}
            }}
            
            showDetailedFeedback('battle-feedback', isCorrect, state.currentWord, selectedAnswer);
            updateBattleDisplay();
            disableOptions('battle-options-area');
            
            // Check for winner
            if (state.player1Score >= 5 || state.player2Score >= 5) {{
                const winner = state.player1Score >= 5 ? 1 : 2;
                setTimeout(() => {{
                    const winFeedback = document.createElement('div');
                    winFeedback.className = 'feedback correct';
                    winFeedback.innerHTML = '<h3>🏆 Player ' + winner + ' Wins!</h3>' +
                        '<p>Final Score: ' + state.player1Score + ' - ' + state.player2Score + '</p>' +
                        '<p>Great vocabulary battle! 🎓</p>';
                    
                    document.getElementById('battle-feedback').appendChild(winFeedback);
                    state.isActive = false;
                    document.getElementById('battle-start').disabled = false;
                }}, 3000);
                return;
            }}
            
            // Switch players
            state.currentPlayer = state.currentPlayer === 1 ? 2 : 1;
            setTimeout(() => {{
                if (state.isActive) {{
                    generateBattleQuestion();
                    document.getElementById('battle-feedback').innerHTML = '';
                }}
            }}, 4000);
        }}
        
        function updateBattleDisplay() {{
            const state = gameStates.battle;
            document.getElementById('battle-p1-score').textContent = state.player1Score;
            document.getElementById('battle-p2-score').textContent = state.player2Score;
            
            document.getElementById('player1-card').classList.toggle('active', state.currentPlayer === 1);
            document.getElementById('player2-card').classList.toggle('active', state.currentPlayer === 2);
        }}
        
        function resetBattle() {{
            const state = gameStates.battle;
            state.isActive = false;
            state.currentPlayer = 1;
            state.player1Score = 0;
            state.player2Score = 0;
            
            updateBattleDisplay();
            document.getElementById('battle-question').innerHTML = 'Click "Start Battle" to begin the learning battle!';
            document.getElementById('battle-options-area').innerHTML = '';
            document.getElementById('battle-feedback').innerHTML = '';
            document.getElementById('battle-start').disabled = false;
        }}
        
        // Endurance Mode with full explanations
        document.getElementById('endurance-start').addEventListener('click', startEndurance);
        document.getElementById('endurance-restart').addEventListener('click', restartEndurance);
        
        function startEndurance() {{
            const state = gameStates.endurance;
            state.level = 1;
            state.lives = 3;
            state.score = 0;
            state.isActive = true;
            
            updateEnduranceDisplay();
            generateEnduranceQuestion();
            document.getElementById('endurance-start').disabled = true;
        }}
        
        function generateEnduranceQuestion() {{
            const state = gameStates.endurance;
            if (!state.isActive) return;
            
            const minLength = Math.min(state.level * 8, 60);
            const availableWords = gameData.filter(w => w.meaning.length >= minLength);
            state.currentWord = availableWords.length > 0 ? 
                availableWords[Math.floor(Math.random() * availableWords.length)] : 
                getNextWord();
            
            const wrongCount = Math.min(3, 2 + Math.floor(state.level / 3));
            const wrongMeanings = [];
            const usedMeanings = new Set([state.currentWord.meaning]);
            
            let attempts = 0;
            while (wrongMeanings.length < wrongCount && attempts < 50) {{
                const randomWord = gameData[Math.floor(Math.random() * gameData.length)];
                if (!usedMeanings.has(randomWord.meaning)) {{
                    wrongMeanings.push(randomWord.meaning);
                    usedMeanings.add(randomWord.meaning);
                }}
                attempts++;
            }}
            
            const options = [...wrongMeanings, state.currentWord.meaning].sort(() => Math.random() - 0.5);
            
            document.getElementById('endurance-question').innerHTML = 
                '<strong>Level ' + state.level + ': What does "' + state.currentWord.word + '" mean?</strong>';
            
            displayOptions('endurance-options-area', options, (option) => {{
                checkEnduranceAnswer(option);
            }});
        }}
        
        function checkEnduranceAnswer(selectedAnswer) {{
            const state = gameStates.endurance;
            const isCorrect = selectedAnswer === state.currentWord.meaning;
            
            if (isCorrect) {{
                state.score += state.level * 10;
                state.level++;
            }} else {{
                state.lives--;
                
                if (state.lives <= 0) {{
                    showDetailedFeedback('endurance-feedback', isCorrect, state.currentWord, selectedAnswer);
                    setTimeout(() => {{
                        const gameOverFeedback = document.createElement('div');
                        gameOverFeedback.className = 'feedback incorrect';
                        gameOverFeedback.innerHTML = '<h3>💀 Game Over!</h3>' +
                            '<p>Final Level: ' + state.level + '</p>' +
                            '<p>Final Score: ' + state.score + '</p>' +
                            '<p>Keep learning with detailed explanations! 📚</p>';
                        
                        document.getElementById('endurance-feedback').appendChild(gameOverFeedback);
                        state.isActive = false;
                        document.getElementById('endurance-start').disabled = false;
                    }}, 3000);
                    return;
                }}
            }}
            
            showDetailedFeedback('endurance-feedback', isCorrect, state.currentWord, selectedAnswer);
            updateEnduranceDisplay();
            disableOptions('endurance-options-area');
            
            setTimeout(() => {{
                if (state.isActive) {{
                    generateEnduranceQuestion();
                    document.getElementById('endurance-feedback').innerHTML = '';
                }}
            }}, 4000);
        }}
        
        function updateEnduranceDisplay() {{
            const state = gameStates.endurance;
            document.getElementById('endurance-level').textContent = state.level;
            document.getElementById('endurance-score').textContent = state.score;
            document.getElementById('endurance-lives').textContent = '❤️'.repeat(state.lives);
        }}
        
        function restartEndurance() {{
            const state = gameStates.endurance;
            state.isActive = false;
            state.level = 1;
            state.lives = 3;
            state.score = 0;
            
            updateEnduranceDisplay();
            document.getElementById('endurance-question').innerHTML = 'Click "Start Endurance" to test your vocabulary limits!';
            document.getElementById('endurance-options-area').innerHTML = '';
            document.getElementById('endurance-feedback').innerHTML = '';
            document.getElementById('endurance-start').disabled = false;
        }}
        
        // Utility functions
        function displayOptions(containerId, options, onSelect) {{
            const optionsArea = document.getElementById(containerId);
            optionsArea.innerHTML = '';
            
            options.forEach((option, index) => {{
                const optionDiv = document.createElement('div');
                optionDiv.className = 'choice-option';
                optionDiv.textContent = (index + 1) + '. ' + option;
                
                optionDiv.onclick = function() {{
                    document.querySelectorAll('#' + containerId + ' .choice-option').forEach(opt => {{
                        opt.classList.remove('selected');
                    }});
                    optionDiv.classList.add('selected');
                    onSelect(option);
                }};
                
                optionsArea.appendChild(optionDiv);
            }});
        }}
        
        function disableOptions(containerId) {{
            document.querySelectorAll('#' + containerId + ' .choice-option').forEach(opt => {{
                opt.style.pointerEvents = 'none';
                opt.style.opacity = '0.7';
            }});
        }}
        
        function updateScores(gameType) {{
            const state = gameStates[gameType];
            document.getElementById(gameType + '-correct').textContent = state.correctAnswers;
            document.getElementById(gameType + '-total').textContent = state.totalQuestions;
            if (gameType === 'classic') {{
                document.getElementById(gameType + '-streak').textContent = state.currentStreak;
            }}
            if (gameType === 'speed') {{
                const elapsedMinutes = (Date.now() - state.startTime) / 1000 / 60;
                const wpm = Math.round(state.correctAnswers / Math.max(elapsedMinutes, 0.1));
                document.getElementById('speed-wpm').textContent = wpm;
            }}
        }}
        
        // Initialize
        console.log('🎮 Enhanced Word Games loaded with ' + gameData.length + ' words!');
        console.log('📚 Full explanations with origins, synonyms, antonyms, and examples!');
        generateClassicQuestion();
    </script>
</body>
</html>'''
    
    # Write the enhanced HTML file
    with open('enhanced_word_games.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Enhanced HTML created: enhanced_word_games.html")
    print(f"🎯 New Features:")
    print(f"   • Detailed word explanations after each answer")
    print(f"   • Origin/etymology information included")
    print(f"   • Synonyms and antonyms displayed")
    print(f"   • Example sentences shown")
    print(f"   • Enhanced feedback for all 5 game modes")
    print(f"   • Mobile-optimized explanation layout")

if __name__ == "__main__":
    create_enhanced_html()