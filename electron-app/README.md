# 🎮 Word Games Collection - Electron App

A desktop application featuring multiple interactive word games to help you master vocabulary. Built with Electron, this app includes 5 engaging game modes using a rich dataset of nearly 5,000 enriched vocabulary words.

## 📋 Table of Contents

- [Features](#features)
- [Game Modes](#game-modes)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Project Structure](#project-structure)
- [Data Format](#data-format)
- [Development](#development)
- [Technologies Used](#technologies-used)

## ✨ Features

- **5 Different Game Modes** - Multiple ways to learn and practice vocabulary
- **4,963 Enriched Words** - Comprehensive word database with:
  - Detailed meanings
  - Synonyms and antonyms
  - Example sentences
  - Word origins
- **Desktop Application** - Native desktop experience powered by Electron
- **Responsive UI** - Beautiful gradient design with intuitive navigation
- **Progress Tracking** - Track your performance across different game modes

## 🎯 Game Modes

### 1. 📚 Classic Mode
Traditional vocabulary learning with flashcards showing word definitions, synonyms, antonyms, and example usage.

### 2. ⚡ Speed Challenge
Test your vocabulary skills against the clock. Quick-fire questions to improve reaction time and word recognition.

### 3. 🧠 Quiz Master
Multiple-choice quiz format to test your understanding of word meanings and usage.

### 4. 🧩 Memory Game
Match words with their meanings in a memory-style card matching game.

### 5. ⚔️ Word Battle
Competitive mode where you battle against word challenges to prove your vocabulary mastery.

## 🚀 Installation

### Prerequisites

- **Node.js** (v14 or higher)
- **npm** (comes with Node.js)

### Steps

1. **Navigate to the electron-app directory:**
   ```bash
   cd c:\Users\wanth\hharry\harry\ai\ml\python\wordenricher\electron-app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

   This will install:
   - Electron (v30.0.0)

## 🎮 Running the App

### Start the Application

```bash
npm start
```

Or using electron directly:
```bash
npx electron .
```

The app will launch in a desktop window (1100x800 pixels by default).

## 📁 Project Structure

```
electron-app/
├── main.js                      # Electron main process
├── package.json                 # Project dependencies and scripts
├── word_games_collection.html   # Main game interface
├── main_game.js                 # Game logic and interactions
├── game_words_data.js          # Word database (4,963 words)
└── README.md                    # This file
```

### Key Files

- **main.js**: Electron entry point that creates the browser window and loads the HTML file
- **word_games_collection.html**: Complete game UI with all 5 game modes
- **game_words_data.js**: JSON array containing all enriched word data
- **main_game.js**: Game mechanics, event handlers, and interactive features
- **package.json**: NPM configuration with Electron dependency

## 📊 Data Format

Each word in `game_words_data.js` follows this structure:

```javascript
{
    "word": "abase",
    "meaning": "To lower in position, estimation, or the like; degrade.",
    "synonyms": ["debase", "demean", "degrade", "humble", "demote"],
    "antonyms": ["elevate", "exalt", "ennoble", "dignify", "promote"],
    "sentences": [
        "The politician's scandalous behavior caused her to abase herself before the public.",
        "The teacher tried to abase his student's ego...",
        "The dictator's actions would eventually abase him..."
    ],
    "origin": "From Old French 'abaser', from Latin 'abasare'..."
}
```

**Total Words**: 4,963

## 🛠️ Development

### Modifying the App

1. **Update Game UI**: Edit `word_games_collection.html`
2. **Change Game Logic**: Modify `main_game.js`
3. **Update Word Data**: Edit `game_words_data.js`
4. **Window Settings**: Adjust window size/preferences in `main.js`

### Electron Configuration

Current window settings in `main.js`:
- Width: 1100px
- Height: 800px
- Node Integration: Disabled for security
- Context Isolation: False

### Building for Distribution

To package the app for distribution, you can add electron-builder:

```bash
npm install --save-dev electron-builder
```

Add to `package.json`:
```json
"scripts": {
  "start": "electron .",
  "build": "electron-builder"
}
```

Then run:
```bash
npm run build
```

## 🔧 Technologies Used

- **Electron** (v30.0.0) - Desktop application framework
- **HTML5** - Structure and markup
- **CSS3** - Styling with gradients and animations
- **JavaScript (ES6+)** - Game logic and interactivity
- **Comic Sans MS** - Fun, playful typography

## 📝 Notes

- The original word data was generated from `enrichedpdfplan.txt`
- This is a standalone Electron app version of the web-based word games
- Files are copied from the main project folder, so keep them synchronized if updates are made

## 🎨 UI Design

- **Color Scheme**: Purple gradient background (#667eea to #764ba2)
- **Layout**: Tabbed interface for easy navigation between game modes
- **Icons**: Emoji-based icons for visual appeal
- **Typography**: Comic Sans MS for a friendly, approachable feel

## 📞 Support

If you encounter any issues:
1. Make sure Node.js and npm are properly installed
2. Delete `node_modules` and run `npm install` again
3. Check that all files are present in the electron-app directory
4. Verify that `game_words_data.js` is not corrupted

## 🎓 Educational Value

This app is ideal for:
- GRE/SAT preparation
- Vocabulary building
- English language learners
- Anyone looking to improve their word knowledge

---

**Created**: Few months ago  
**Last Updated**: January 2026  
**Version**: 1.0.0
