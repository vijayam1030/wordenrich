# 🎮 Word Games Server

A mobile-friendly vocabulary games server built with Node.js and Express.

## 🚀 Quick Start

### Prerequisites
- Node.js (version 14 or higher)
- npm (comes with Node.js)

### Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Start the server:**
```bash
npm start
```

3. **For development (auto-restart on changes):**
```bash
npm run dev
```

The server will start on `http://localhost:3000`

## 🎯 Game Features

- **📚 Classic Mode**: Multiple choice vocabulary questions with scoring
- **⚡ Speed Challenge**: 60-second timed vocabulary quiz  
- **🧠 Quiz Master**: 10-question test with letter grades
- **📱 Mobile Responsive**: Works perfectly on all devices
- **🎨 Touch-Friendly**: Optimized for mobile interactions

## 📁 Project Structure

```
word-games-server/
├── server.js           # Express server
├── package.json        # Dependencies and scripts
├── deploy_games.html   # Main game HTML file
└── README.md          # This file
```

## 🌐 API Endpoints

- `GET /` - Main game page
- `GET /health` - Health check endpoint
- `GET /api/stats` - Game statistics

## 🚀 Deployment Options

### 1. Local Development
```bash
npm start
```
Access at: `http://localhost:3000`

### 2. Production Deployment

#### Heroku
```bash
# Install Heroku CLI, then:
heroku create your-word-games
git add .
git commit -m "Deploy word games"
git push heroku main
```

#### Vercel
```bash
# Install Vercel CLI, then:
npm i -g vercel
vercel
```

#### Railway
```bash
# Install Railway CLI, then:
railway login
railway init
railway up
```

#### DigitalOcean App Platform
1. Connect your GitHub repository
2. Select Node.js environment
3. Set build command: `npm install`
4. Set run command: `npm start`

### 3. Environment Variables

The server uses these environment variables:

- `PORT` - Server port (default: 3000)

Example `.env` file:
```
PORT=8080
```

## 🔧 Customization

### Adding More Words
Edit the `gameData` array in `deploy_games.html` around line 366.

### Changing Styles
Modify the CSS in the `<style>` section of `deploy_games.html`.

### Server Configuration
Update `server.js` to add new endpoints or middleware.

## 📊 Monitoring

Check server health:
```bash
curl http://localhost:3000/health
```

## 🛠️ Development

1. **Install nodemon for auto-restart:**
```bash
npm install -g nodemon
```

2. **Run in development mode:**
```bash
npm run dev
```

## 📱 Mobile Testing

Test on different devices:
- Chrome DevTools device emulation
- BrowserStack for real device testing
- Your phone's browser at `http://your-ip:3000`

## 🔒 Security Features

- CORS enabled for cross-origin requests
- Error handling middleware
- Graceful shutdown handling
- Static file serving security

## 📈 Performance

- Lightweight Express server
- Static file caching
- Mobile-optimized assets
- Efficient game logic

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Kill process on port 3000
npx kill-port 3000
```

**Module not found:**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

## 📝 License

MIT License - feel free to use for educational purposes!

---

**🎮 Enjoy playing the vocabulary games! 📚**