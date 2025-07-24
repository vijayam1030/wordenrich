#!/usr/bin/env python3
"""
Generate an interactive word guessing game from enrichedpdfplan.txt
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

def create_game_html(words_data):
    """Create the interactive game HTML."""
    
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
                'clues': clues
            })
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Word Master Game</title>
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
            max-width: 800px;
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
            margin-bottom: 20px;
        }}
        
        .mode-selector {{
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .mode-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: inherit;
        }}
        
        .mode-btn:hover {{
            background: #5a67d8;
            transform: translateY(-2px);
        }}
        
        .mode-btn.active {{
            background: #4c51bf;
            box-shadow: 0 5px 15px rgba(76, 81, 191, 0.4);
        }}
        
        .game-area {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
        }}
        
        .question-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            font-size: 1.3em;
            line-height: 1.6;
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
            
            .game-header, .game-area {{
                padding: 20px;
            }}
            
            .game-title {{
                font-size: 2em;
            }}
            
            .mode-selector {{
                flex-direction: column;
                align-items: center;
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
            <h1 class="game-title">🎮 Word Master</h1>
            <p class="game-subtitle">Test your vocabulary skills with fun clues and challenges!</p>
            
            <div class="mode-selector">
                <button class="mode-btn active" data-mode="word-to-meaning">📖 Word → Meaning</button>
                <button class="mode-btn" data-mode="meaning-to-word">🔍 Meaning → Word</button>
                <button class="mode-btn" data-mode="sentence-clue">💬 Sentence Clues</button>
                <button class="mode-btn" data-mode="fun-clues">🎭 Fun Clues</button>
            </div>
        </div>
        
        <div class="game-area">
            <div class="score-board">
                <div class="score-item">
                    <div class="score-number" id="correct-score">0</div>
                    <div class="score-label">Correct</div>
                </div>
                <div class="score-item">
                    <div class="score-number" id="total-score">0</div>
                    <div class="score-label">Total</div>
                </div>
                <div class="score-item">
                    <div class="score-number" id="streak-score">0</div>
                    <div class="score-label">Streak</div>
                </div>
            </div>
            
            <div id="question-area">
                <div class="question-card" id="question-text">
                    Click "New Question" to start playing!
                </div>
                
                <div id="clues-area"></div>
                
                <div class="input-area">
                    <input type="text" class="game-input" id="answer-input" placeholder="Type your answer here..." disabled>
                </div>
                
                <div class="btn-group">
                    <button class="game-btn submit-btn" id="submit-btn" disabled>Submit Answer</button>
                    <button class="game-btn hint-btn" id="hint-btn" disabled>Get Hint 💡</button>
                    <button class="game-btn skip-btn" id="skip-btn" disabled>Skip Question</button>
                </div>
                
                <div class="btn-group">
                    <button class="game-btn" id="new-question-btn" style="background: #667eea; color: white;">New Question 🎲</button>
                </div>
            </div>
            
            <div id="feedback-area"></div>
        </div>
    </div>

    <script>
        const gameData = {json.dumps(game_data)};
        
        let currentWord = null;
        let gameMode = 'word-to-meaning';
        let hintsUsed = 0;
        let correctAnswers = 0;
        let totalQuestions = 0;
        let currentStreak = 0;
        let maxStreak = 0;
        
        // DOM elements
        const modeButtons = document.querySelectorAll('.mode-btn');
        const questionText = document.getElementById('question-text');
        const cluesArea = document.getElementById('clues-area');
        const answerInput = document.getElementById('answer-input');
        const submitBtn = document.getElementById('submit-btn');
        const hintBtn = document.getElementById('hint-btn');
        const skipBtn = document.getElementById('skip-btn');
        const newQuestionBtn = document.getElementById('new-question-btn');
        const feedbackArea = document.getElementById('feedback-area');
        const correctScore = document.getElementById('correct-score');
        const totalScore = document.getElementById('total-score');
        const streakScore = document.getElementById('streak-score');
        
        // Event listeners
        modeButtons.forEach(btn => {{
            btn.addEventListener('click', () => {{
                modeButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                gameMode = btn.dataset.mode;
                generateNewQuestion();
            }});
        }});
        
        newQuestionBtn.addEventListener('click', generateNewQuestion);
        submitBtn.addEventListener('click', checkAnswer);
        hintBtn.addEventListener('click', showHint);
        skipBtn.addEventListener('click', skipQuestion);
        
        answerInput.addEventListener('keypress', (e) => {{
            if (e.key === 'Enter') {{
                checkAnswer();
            }}
        }});
        
        answerInput.addEventListener('input', () => {{
            submitBtn.disabled = answerInput.value.trim() === '';
        }});
        
        function generateNewQuestion() {{
            currentWord = gameData[Math.floor(Math.random() * gameData.length)];
            hintsUsed = 0;
            feedbackArea.innerHTML = '';
            cluesArea.innerHTML = '';
            answerInput.value = '';
            answerInput.disabled = false;
            submitBtn.disabled = true;
            hintBtn.disabled = false;
            skipBtn.disabled = false;
            answerInput.focus();
            
            switch(gameMode) {{
                case 'word-to-meaning':
                    questionText.innerHTML = '<strong>What does "' + currentWord.word + '" mean?</strong>';
                    break;
                case 'meaning-to-word':
                    questionText.innerHTML = '<strong>Which word means:</strong><br>"' + currentWord.meaning + '"';
                    break;
                case 'sentence-clue':
                    if (currentWord.sentences.length > 0) {{
                        const sentence = currentWord.sentences[Math.floor(Math.random() * currentWord.sentences.length)];
                        const hiddenSentence = sentence.replace(new RegExp(currentWord.word, 'gi'), '____');
                        questionText.innerHTML = '<strong>Fill in the blank:</strong><br>"' + hiddenSentence + '"';
                    }} else {{
                        questionText.innerHTML = '<strong>What does "' + currentWord.word + '" mean?</strong>';
                    }}
                    break;
                case 'fun-clues':
                    const randomClue = currentWord.clues[Math.floor(Math.random() * currentWord.clues.length)];
                    questionText.innerHTML = '<strong>Guess the word:</strong><br>' + randomClue;
                    break;
            }}
        }}
        
        function showHint() {{
            hintsUsed++;
            const clue = document.createElement('div');
            clue.className = 'clue';
            
            // Generate multiple choice options for the final hint
            let multipleChoiceOptions = [];
            if (hintsUsed === 6) {{
                if (gameMode === 'word-to-meaning') {{
                    // For word-to-meaning: show 4 different meanings
                    const wrongMeanings = gameData
                        .filter(w => w.word !== currentWord.word && w.meaning.length > 10)
                        .sort(() => Math.random() - 0.5)
                        .slice(0, 3)
                        .map(w => w.meaning);
                    
                    multipleChoiceOptions = [...wrongMeanings, currentWord.meaning].sort(() => Math.random() - 0.5);
                }} else {{
                    // For other modes: show 4 different words
                    const wrongOptions = gameData
                        .filter(w => w.word !== currentWord.word && w.word.length >= currentWord.word.length - 2 && w.word.length <= currentWord.word.length + 2)
                        .sort(() => Math.random() - 0.5)
                        .slice(0, 3)
                        .map(w => w.word);
                    
                    multipleChoiceOptions = [...wrongOptions, currentWord.word].sort(() => Math.random() - 0.5);
                }}
            }}
            
            let hints = [];
            
            if (gameMode === 'word-to-meaning') {{
                // For word-to-meaning: don't reveal the word in hints
                hints = [
                    '💡 Hint ' + hintsUsed + ': This definition has ' + currentWord.meaning.split(' ').length + ' words',
                    '💡 Hint ' + hintsUsed + ': Think about actions related to: ' + currentWord.synonyms.slice(0, 2).join(', '),
                    '💡 Hint ' + hintsUsed + ': It\\'s the opposite of: ' + currentWord.antonyms.slice(0, 2).join(', '),
                    '💡 Hint ' + hintsUsed + ': This word relates to: ' + currentWord.synonyms.slice(0, 3).join(', '),
                    '💡 Hint ' + hintsUsed + ': Etymology clue: ' + (currentWord.origin ? currentWord.origin.substring(0, 40) + '...' : 'Ancient origins'),
                    '🎯 Final Hint: Choose one of these options: ' + multipleChoiceOptions.join(' | ')
                ];
            }} else {{
                // For other modes: use original hints with word details
                hints = [
                    '💡 Hint ' + hintsUsed + ': The word has ' + currentWord.word.length + ' letters',
                    '💡 Hint ' + hintsUsed + ': It starts with "' + currentWord.word[0].toUpperCase() + '"',
                    '💡 Hint ' + hintsUsed + ': Synonyms include: ' + currentWord.synonyms.slice(0, 2).join(', '),
                    '💡 Hint ' + hintsUsed + ': It\\'s NOT the same as: ' + currentWord.antonyms.slice(0, 2).join(', '),
                    '💡 Hint ' + hintsUsed + ': ' + currentWord.origin.substring(0, 50) + '...',
                    '🎯 Final Hint: Choose one of these options: ' + multipleChoiceOptions.join(' | ')
                ];
            }}
            
            if (hintsUsed <= hints.length) {{
                if (hintsUsed === 6) {{
                    // Special styling for multiple choice hint
                    clue.className = 'clue multiple-choice-clue';
                    clue.innerHTML = '🎯 Final Hint: Choose the correct word:';
                    
                    // Create clickable options
                    const optionsDiv = document.createElement('div');
                    optionsDiv.className = 'choice-options';
                    
                    multipleChoiceOptions.forEach(option => {{
                        const optionDiv = document.createElement('div');
                        optionDiv.className = 'choice-option';
                        optionDiv.textContent = option;
                        optionDiv.onclick = function() {{
                            answerInput.value = option;
                            answerInput.focus();
                            // Trigger input event to enable submit button
                            answerInput.dispatchEvent(new Event('input'));
                            // Highlight selected option
                            document.querySelectorAll('.choice-option').forEach(opt => opt.classList.remove('selected'));
                            optionDiv.classList.add('selected');
                        }};
                        optionsDiv.appendChild(optionDiv);
                    }});
                    
                    clue.appendChild(optionsDiv);
                }} else {{
                    clue.textContent = hints[hintsUsed - 1];
                }}
                
                cluesArea.appendChild(clue);
                clue.classList.add('bounce');
            }}
            
            if (hintsUsed >= 6) {{
                hintBtn.disabled = true;
            }}
        }}
        
        function checkAnswer() {{
            const userAnswer = answerInput.value.trim().toLowerCase();
            let isCorrect = false;
            
            // Debug logging
            console.log('Game Mode:', gameMode);
            console.log('User Answer:', userAnswer);
            console.log('Correct Answer:', gameMode === 'word-to-meaning' ? currentWord.meaning : currentWord.word);
            
            switch(gameMode) {{
                case 'word-to-meaning':
                    const meaningLower = currentWord.meaning.toLowerCase();
                    
                    // Check if user typed the word instead of meaning
                    if (userAnswer === currentWord.word.toLowerCase()) {{
                        // Special feedback for typing the word instead of meaning
                        showSpecialFeedback('word-instead-of-meaning');
                        return;
                    }}
                    
                    // Check for correct answers (handle periods and exact matches)
                    const cleanMeaning = meaningLower.replace(/[.,;!?]/g, '').trim();
                    const cleanUserAnswer = userAnswer.replace(/[.,;!?]/g, '').trim();
                    
                    isCorrect = meaningLower === userAnswer ||
                               cleanMeaning === cleanUserAnswer ||
                               meaningLower.includes(userAnswer) || 
                               cleanMeaning.includes(cleanUserAnswer) ||
                               currentWord.synonyms.some(syn => syn.toLowerCase() === userAnswer) ||
                               (userAnswer.length >= 3 && meaningLower.split(' ').some(word => word.replace(/[.,;!?]/g, '') === userAnswer));
                    break;
                case 'meaning-to-word':
                case 'sentence-clue':
                case 'fun-clues':
                    isCorrect = currentWord.word.toLowerCase() === userAnswer;
                    break;
            }}
            
            console.log('Is Correct:', isCorrect);
            
            totalQuestions++;
            
            if (isCorrect) {{
                correctAnswers++;
                currentStreak++;
                maxStreak = Math.max(maxStreak, currentStreak);
                showFeedback(true);
            }} else {{
                currentStreak = 0;
                showFeedback(false);
            }}
            
            updateScores();
            disableInputs();
        }}
        
        function showSpecialFeedback(type) {{
            const feedback = document.createElement('div');
            feedback.className = 'feedback incorrect';
            
            if (type === 'word-instead-of-meaning') {{
                feedback.innerHTML = '🤔 Close! You typed the word "' + currentWord.word + '" but I need its <strong>meaning</strong>!<br>💡 Try: "' + currentWord.meaning + '"';
            }}
            
            feedbackArea.innerHTML = '';
            feedbackArea.appendChild(feedback);
            
            // Don't count as wrong answer, just give them another chance
            setTimeout(() => {{
                feedback.innerHTML += '<br><br>🎯 Try again! What does "' + currentWord.word + '" mean?';
            }}, 2000);
        }}
        
        function showFeedback(correct) {{
            const feedback = document.createElement('div');
            feedback.className = 'feedback ' + (correct ? 'correct' : 'incorrect');
            
            if (correct) {{
                const messages = ['🎉 Excellent!', '✨ Perfect!', '🚀 Amazing!', '🏆 Brilliant!', '⭐ Outstanding!'];
                feedback.innerHTML = messages[Math.floor(Math.random() * messages.length)];
            }} else {{
                feedback.innerHTML = '❌ Not quite right. The answer was: <strong>' + (gameMode === 'word-to-meaning' ? currentWord.meaning : currentWord.word) + '</strong>';
            }}
            
            feedbackArea.innerHTML = '';
            feedbackArea.appendChild(feedback);
            
            // Show word details
            setTimeout(() => {{
                showWordDetails();
            }}, 1000);
        }}
        
        function showWordDetails() {{
            const details = document.createElement('div');
            details.className = 'answer-reveal';
            let detailsHTML = '<h3>' + currentWord.word + '</h3><div class="word-details">';
            detailsHTML += '<div class="detail-section"><span class="detail-title">Meaning:</span> ' + currentWord.meaning + '</div>';
            
            if (currentWord.synonyms.length) {{
                detailsHTML += '<div class="detail-section"><span class="detail-title">Synonyms:</span><br>';
                detailsHTML += currentWord.synonyms.map(syn => '<span class="synonym-tag">' + syn + '</span>').join('');
                detailsHTML += '</div>';
            }}
            
            if (currentWord.antonyms.length) {{
                detailsHTML += '<div class="detail-section"><span class="detail-title">Antonyms:</span><br>';
                detailsHTML += currentWord.antonyms.map(ant => '<span class="antonym-tag">' + ant + '</span>').join('');
                detailsHTML += '</div>';
            }}
            
            if (currentWord.sentences.length) {{
                detailsHTML += '<div class="detail-section"><span class="detail-title">Example:</span>';
                detailsHTML += '<div class="example-sentence">' + currentWord.sentences[0] + '</div></div>';
            }}
            
            detailsHTML += '</div>';
            details.innerHTML = detailsHTML;
            feedbackArea.appendChild(details);
        }}
        
        function skipQuestion() {{
            totalQuestions++;
            currentStreak = 0;
            showFeedback(false);
            updateScores();
            disableInputs();
        }}
        
        function disableInputs() {{
            answerInput.disabled = true;
            submitBtn.disabled = true;
            hintBtn.disabled = true;
            skipBtn.disabled = true;
        }}
        
        function updateScores() {{
            correctScore.textContent = correctAnswers;
            totalScore.textContent = totalQuestions;
            streakScore.textContent = currentStreak;
        }}
        
        // Initialize game
        generateNewQuestion();
    </script>
</body>
</html>"""
    
    return html_content

def main():
    """Main function to generate the word game."""
    input_file = "enrichedpdfplan.txt"
    output_file = "word_master_game.html"
    
    if not Path(input_file).exists():
        print(f"❌ Error: Input file '{input_file}' not found!")
        return
    
    print("🎮 Generating Word Master Game...")
    
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
    
    # Generate the game HTML
    html_content = create_game_html(words_data)
    
    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Word Master Game created!")
    print(f"📁 Output file: {output_file}")
    print(f"🎮 Open the file in your browser to play!")
    print(f"📊 Game includes {len(words_data)} words with multiple game modes")

if __name__ == "__main__":
    main()