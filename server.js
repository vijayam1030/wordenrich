const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Serve the main game page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'complete_games_5k.html'));
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        timestamp: new Date().toISOString(),
        message: 'Word Games Server is running!'
    });
});

// API endpoint for game statistics (optional future feature)
app.get('/api/stats', (req, res) => {
    res.json({
        totalWords: 4963,
        gameModes: ['Classic', 'Speed Challenge', 'Quiz Master', 'Word Battle', 'Endurance Mode'],
        features: ['Mobile Responsive', 'Multiple Choice', 'Real-time Scoring', 'Multiplayer Battle', 'Progressive Difficulty', 'No Word Repetition', 'Global Shuffling']
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ 
        error: 'Page not found',
        message: 'The requested resource does not exist.'
    });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Server Error:', err.stack);
    res.status(500).json({ 
        error: 'Internal Server Error',
        message: 'Something went wrong on the server.'
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🎮 Word Games Server is running!`);
    console.log(`📱 Local: http://localhost:${PORT}`);
    console.log(`🌐 Network: http://0.0.0.0:${PORT}`);
    console.log(`📊 Health Check: http://localhost:${PORT}/health`);
    console.log(`🎯 Games ready at: http://localhost:${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('👋 Received SIGTERM, shutting down gracefully...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('👋 Received SIGINT, shutting down gracefully...');
    process.exit(0);
});