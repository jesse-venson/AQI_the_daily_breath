/**
 * Frontend Configuration
 *
 * This file handles environment-specific configuration.
 * Development: Uses localhost:5000
 * Production: Uses environment variable REACT_APP_API_URL
 */

const config = {
    // API endpoint for predictions
    API_URL: (() => {
        // Production: Use Railway backend when not on localhost
        if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
            return 'https://aqithedailybreath-production.up.railway.app';
        }

        // Development: Use localhost
        return 'http://localhost:5000';
    })(),

    // Application name
    APP_NAME: 'The Daily Breath',

    // Version
    VERSION: '1.0.0'
};

console.log(`[Config] API URL: ${config.API_URL}`);
console.log(`[Config] Environment: ${config.API_URL.includes('localhost') ? 'development' : 'production'}`);

// Export for use in other scripts
window.APP_CONFIG = config;
