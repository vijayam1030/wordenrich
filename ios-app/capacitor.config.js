const config = {
  appId: 'com.wordgames.app',
  appName: 'Word Games',
  webDir: 'www',
  bundledWebRuntime: false,
  backgroundColor: '#667eea',
  ios: {
    contentInset: 'automatic',
    scrollEnabled: true,
    backgroundColor: '#667eea'
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: '#667eea',
      showSpinner: false,
      androidSpinnerStyle: 'small',
      iosSpinnerStyle: 'small'
    }
  }
};

module.exports = config;
