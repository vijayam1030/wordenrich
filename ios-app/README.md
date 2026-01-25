# 📱 Word Games iOS App

A standalone iOS vocabulary learning app with 4,963 enriched words.

## 🚀 Quick Start

### Prerequisites
- Node.js 14+ installed
- Xcode installed (for iOS development)
- An Apple Developer account (for App Store submission)

### Setup Instructions

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Add iOS Platform**
   ```bash
   npm run install:ios
   ```

3. **Open in Xcode**
   ```bash
   npm run open:ios
   ```

4. **Build and Run**
   - In Xcode, select a simulator or connected device
   - Click the Play button to build and run

## 📦 What's Included

- **www/index.html** - Complete standalone game (no backend required)
- **package.json** - Project dependencies
- **capacitor.config.ts** - iOS app configuration

## 🎮 Features

- 📚 Classic Mode - Flashcard learning
- ⚡ Speed Challenge - Timed questions
- 🧠 Quiz Master - Multiple choice tests
- ⚔️ Word Battle - Two-player mode
- 🏃 Endurance Mode - Survival challenge
- 📖 Dictionary - Browse all 4,963 words

## 🍎 App Store Preparation

### Before Submitting

1. **Update App Identifier**
   - Change `appId` in `capacitor.config.ts` to your bundle ID
   - Example: `com.yourcompany.wordgames`

2. **Add App Icons**
   - After running Xcode, add icons in Assets.xcassets
   - Sizes: 1024x1024, 180x180, 120x120, 87x87, etc.

3. **Configure in Xcode**
   - Set proper app name
   - Add privacy descriptions if needed
   - Configure signing & capabilities
   - Set version and build number

4. **Test Thoroughly**
   - Test on multiple devices
   - Check all game modes
   - Verify offline functionality

### App Store Guidelines Compliance

✅ **Follows Apple Guidelines:**
- Standalone app (no backend dependencies)
- Works completely offline
- No in-app purchases or ads
- Educational content
- Privacy-friendly (no data collection)
- iPhone optimized with safe areas
- Responsive design for all screen sizes

## 🔧 Development

### Sync Changes
After modifying `www/index.html`:
```bash
npm run sync
```

### Build for Device
```bash
npm run build
```

## 📱 File Structure

```
ios-app/
├── www/
│   └── index.html          # Your complete game
├── ios/                    # (Created after install:ios)
├── capacitor.config.ts     # App configuration
├── package.json           # Dependencies
└── README.md              # This file
```

## 🎯 Next Steps

1. Run `npm install`
2. Run `npm run install:ios`
3. Run `npm run open:ios`
4. Build in Xcode and test on simulator
5. Configure app details in Xcode
6. Add app icons
7. Submit to App Store!

## 📝 Notes

- The game is 100% self-contained in index.html
- No server or API required
- All 4,963 words embedded in the file
- Works completely offline
- File size: ~5-10 MB (manageable for App Store)
