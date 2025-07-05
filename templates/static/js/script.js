function citySearch() {
    let text = document.getElementById("city").value
    if (text.length < 3) {
        return;
    }
    document.getElementById("cityList").hidden = false;
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/autocomplete?name=" + text, true);

    xhr.onload = () => {
        let data = JSON.parse(xhr.responseText);
        let search = document.getElementById("cityList");
        search.innerHTML = "";
        for (city of data) {
            const li = document.createElement("li");
            li.textContent = `${city.name}, ${city.country} (${city.lat},${city.lng})`;
            search.appendChild(li);
        }

    };
    xhr.send(null);
}

function onItemClick(e) {
    const search = document.getElementById("city");
    search.value = e.target.textContent
    document.getElementById("cityList").hidden = true;
}

function getReport(e) {
    e.preventDefault();
    const search = document.getElementById("city");
    const city = search.value;

    // Check if we're using geolocation or city search

    // Extract coordinates from the city string
    const ix = city.indexOf("(")
    const lat = city.substring(ix + 1, city.length - 1).split(",")[0]
    const lng = city.substring(ix + 1, city.length - 1).split(",")[1]
    const report = document.querySelector('input[name="report"]:checked').value;
    window.location = `/generate_report?lat=${encodeURIComponent(lat.trim())}&lng=${encodeURIComponent(lng.trim())}&report=${report}&city=${encodeURIComponent(city.substring(0, ix))}`;
}

function getCurrentLocation() {
    if (navigator.geolocation) {
        document.getElementById("location-status").textContent = "Getting your location...";
        navigator.geolocation.getCurrentPosition(
            async function (position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;

                const response = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`);
                const data = await response.json();

                // Store the coordinates in hidden fields
                document.getElementById("lat").value = lat;
                document.getElementById("lng").value = lng;

                // Update the city input field to show we're using the current location
                document.getElementById("city").value = data.address.town + `(${lat}, ${lng})`;
                document.getElementById("location-status").textContent = "Location found!";

                // Hide the city list if it's visible
                document.getElementById("cityList").hidden = true;
            },
            function (error) {
                let errorMessage = "Error getting location: ";
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage += "Permission denied";
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage += "Position unavailable";
                        break;
                    case error.TIMEOUT:
                        errorMessage += "Timeout";
                        break;
                    default:
                        errorMessage += "Unknown error";
                }
                document.getElementById("location-status").textContent = errorMessage;
                console.error(errorMessage);
            }
        );
    } else {
        document.getElementById("location-status").textContent = "Geolocation is not supported by this browser.";
        console.error("Geolocation is not supported by this browser.");
    }
}

window.onload = () => {
    document.getElementById("cityList").addEventListener("click", onItemClick);
    document.getElementById("main-button").addEventListener("click", getReport);
    document.getElementById("location-button").addEventListener("click", function (e) {
        e.preventDefault();
        getCurrentLocation();
    });
}
