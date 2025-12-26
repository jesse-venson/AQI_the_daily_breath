function setCurrentDate() {
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    const today = new Date();
    const formatted = today.toLocaleDateString('en-US', options).toUpperCase();
    document.getElementById('current-date').textContent = formatted;
}

function getAQIInfo(aqi) {
    if (aqi <= 50) return {
        category: 'Good — Safe for all outdoor activities',
        color: '#2d5a3d',
        position: (aqi / 50) * 16.66
    };
    if (aqi <= 100) return {
        category: 'Moderate — Acceptable air quality',
        color: '#8b7355',
        position: 16.66 + ((aqi - 50) / 50) * 16.66
    };
    if (aqi <= 150) return {
        category: 'Unhealthy for Sensitive Groups — Exercise caution',
        color: '#b8860b',
        position: 33.32 + ((aqi - 100) / 50) * 16.66
    };
    if (aqi <= 200) return {
        category: 'Unhealthy — Health effects possible for all',
        color: '#9b1b30',
        position: 49.98 + ((aqi - 150) / 50) * 16.66
    };
    if (aqi <= 300) return {
        category: 'Very Unhealthy — Health alert for everyone',
        color: '#6b1320',
        position: 66.64 + ((aqi - 200) / 100) * 16.66
    };
    return {
        category: 'HAZARDOUS — Emergency conditions!',
        color: '#2d1b2d',
        position: 83.3 + Math.min((aqi - 300) / 200, 1) * 16.66
    };
}

function getPollutantStatus(pollutant, value) {
    const thresholds = {
        PM25: [30, 60, 90, 120],
        PM10: [50, 100, 250, 350],
        NO2: [40, 80, 180, 280],
        SO2: [40, 80, 380, 800],
        CO: [4400, 9400, 12400, 15400],
        O3: [50, 100, 168, 208]
    };

    const levels = ['GOOD', 'FAIR', 'POOR', 'BAD', 'SEVERE'];
    const classes = ['status-good', 'status-moderate', 'status-poor', 'status-bad', 'status-severe'];

    const pollutantThresholds = thresholds[pollutant] || [50, 100, 150, 200];

    for (let i = 0; i < pollutantThresholds.length; i++) {
        if (value <= pollutantThresholds[i]) {
            return { text: levels[i], class: classes[i] };
        }
    }
    return { text: levels[4], class: classes[4] };
}

function typewriterNumber(element, number, duration = 1500) {
    const start = performance.now();
    const startValue = 0;

    function update(currentTime) {
        const elapsed = currentTime - start;
        const progress = Math.min(elapsed / duration, 1);
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(startValue + (number * easeOut));

        element.textContent = current;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

async function predictAQI() {
    const age = document.getElementById('age-input').value;
    const genderEnc = document.getElementById('gender-input').value;
    const parentEnc = document.getElementById('parent-input').value;

    if (!age || age < 1 || age > 120) {
        alert('ATTENTION READER: Please enter a valid age (1-120)');
        return;
    }
    if (genderEnc === '') {
        alert('ATTENTION READER: Please select your gender');
        return;
    }
    if (parentEnc === '') {
        alert('ATTENTION READER: Please indicate parent status');
        return;
    }

    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');

    try {
        const apiUrl = window.APP_CONFIG?.API_URL || 'http://localhost:5000';
        const response = await fetch(`${apiUrl}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                age: parseInt(age),
                gender_enc: parseInt(genderEnc),
                parent_enc: parseInt(parentEnc)
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to fetch');
        }

        const data = await response.json();
        document.getElementById('loading').classList.add('hidden');
        displayResults(data);

    } catch (error) {
        document.getElementById('loading').classList.add('hidden');
        alert('BREAKING: Connection Failed!\n\n' + error.message + '\n\nEnsure the backend press is running at localhost:5000');
    }
}

function displayResults(data) {
    const results = document.getElementById('results');
    results.classList.remove('hidden');

    const aqiEl = document.getElementById('aqi-value');
    typewriterNumber(aqiEl, data.aqi, 2000);

    const aqiInfo = getAQIInfo(data.aqi);
    document.getElementById('aqi-category').textContent = aqiInfo.category;
    document.getElementById('aqi-category').style.color = aqiInfo.color;

    const indicator = document.getElementById('scale-indicator');
    setTimeout(() => {
        indicator.style.left = `calc(${aqiInfo.position}% - 8px)`;
    }, 100);

    const pollutants = [
        { id: 'pm25', key: 'PM25', value: data.pollutants.PM25 },
        { id: 'pm10', key: 'PM10', value: data.pollutants.PM10 },
        { id: 'no2', key: 'NO2', value: data.pollutants.NO2 },
        { id: 'so2', key: 'SO2', value: data.pollutants.SO2 },
        { id: 'co', key: 'CO', value: data.pollutants.CO },
        { id: 'o3', key: 'O3', value: data.pollutants.O3 }
    ];

    pollutants.forEach((p, index) => {
        setTimeout(() => {
            document.getElementById(p.id).textContent = p.value;
            const status = getPollutantStatus(p.key, p.value);
            const statusEl = document.getElementById(`${p.id}-status`);
            statusEl.textContent = status.text;
            statusEl.className = `pollutant-status ${status.class}`;
        }, index * 100);
    });

    document.getElementById('temp').textContent = data.weather.temp;
    document.getElementById('humidity').textContent = data.weather.humidity;
    document.getElementById('pressure').textContent = data.weather.pressure;
    document.getElementById('wind-speed').textContent = data.weather.wind_speed;

    displayHealthRisks(data.health_risks);

    document.getElementById('recommendations-text').textContent = data.recommendations;

    const now = new Date();
    document.getElementById('report-time').textContent = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });

    // Scroll to results
    setTimeout(() => {
        results.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
}

// Display health risks as newspaper articles
function displayHealthRisks(risks) {
    const container = document.getElementById('health-risks-list');
    container.innerHTML = '';

    let delay = 0;
    for (const [symptom, risk] of Object.entries(risks)) {
        const article = document.createElement('div');
        article.className = `risk-article risk-${risk.risk_level.toLowerCase()}`;
        article.style.animationDelay = `${delay}ms`;

        const headline = document.createElement('div');
        headline.className = 'risk-headline';
        headline.textContent = symptom.replace(/_/g, ' ');

        const meta = document.createElement('div');
        meta.className = 'risk-meta';

        const probability = document.createElement('span');
        probability.textContent = `${(risk.probability * 100).toFixed(0)}% probability`;

        const badge = document.createElement('span');
        badge.className = `risk-badge ${risk.risk_level.toLowerCase()}`;
        badge.textContent = risk.risk_level;

        meta.appendChild(probability);
        meta.appendChild(badge);

        article.appendChild(headline);
        article.appendChild(meta);
        container.appendChild(article);

        delay += 150;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setCurrentDate();

    // Enter key triggers prediction
    document.getElementById('age-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') predictAQI();
    });
});
