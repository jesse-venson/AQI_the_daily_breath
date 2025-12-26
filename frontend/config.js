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
        // Check for environment variable (Vercel sets this)
        if (typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_URL) {
            return process.env.REACT_APP_API_URL;
        }

        // Check for global window variable (alternative method)
        if (window.__API_URL__) {
            return window.__API_URL__;
        }

        // Default to localhost for development
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
