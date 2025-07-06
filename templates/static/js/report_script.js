window.onload = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const lat = urlParams.get('lat');
    const lng = urlParams.get('lng');
    let map = L.map('map').setView([lat, lng], 10);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    let marker = L.marker([lat, lng]).addTo(map);
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

// Rest of your report_script.js code will go here
