async function fetchAiSummary() {
    const urlParams = new URLSearchParams(window.location.search);
    const lat = urlParams.get('lat');
    const lng = urlParams.get('lng');
    const city = urlParams.get('city') || '';
    const report = urlParams.get('report') || 'current';

    const textEl = document.getElementById('ai-summary-text');
    if (!textEl) return;
    try {
        const qs = new URLSearchParams({ city, lat, lng, report });
        const resp = await fetch(`/ai_description?${qs.toString()}`);
        if (!resp.ok) throw new Error('Network response was not ok');
        const data = await resp.json();
        const text = (data && data.ai_description) ? String(data.ai_description).trim() : '';
        if (text) {
            textEl.classList.remove('text-muted');
            textEl.textContent = text;
        } else {
            textEl.classList.add('text-muted');
            textEl.textContent = 'AI summary is not available right now.';
        }
    } catch (e) {
        textEl.classList.add('text-muted');
        textEl.textContent = 'AI summary is not available right now.';
    }
}

window.onload = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const lat = urlParams.get('lat');
    const lng = urlParams.get('lng');
    let map = L.map('map').setView([lat, lng], 10);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    L.marker([lat, lng]).addTo(map);

    // Kick off AI summary fetch after page and map init
    fetchAiSummary();
}
// Detect keyboard navigation for accessibility focus styles
function handleFirstTab(e) {
    if (e.keyCode === 9) { // Tab key
        document.body.classList.add('using-keyboard');
        window.removeEventListener('keydown', handleFirstTab);
        window.addEventListener('mousedown', handleMouseDownOnce);
    }
}

function handleMouseDownOnce() {
    document.body.classList.remove('using-keyboard');
    window.removeEventListener('mousedown', handleMouseDownOnce);
    window.addEventListener('keydown', handleFirstTab);
}

window.addEventListener('keydown', handleFirstTab);
