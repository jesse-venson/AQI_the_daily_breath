const config = {
    API_URL: (() => {
        if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
            return 'https://aqithedailybreath-production.up.railway.app';
        }
        return 'http://localhost:5000';
    })(),
    APP_NAME: 'The Daily Breath',
    VERSION: '1.0.0'
};

window.APP_CONFIG = config;
