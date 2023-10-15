function citySearch() {
    text = document.getElementById("city").value
    if (text.length < 3) {
        return;
    }
    document.getElementById("cityList").hidden = false;
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/autocomplete?name=" + text, true);

    xhr.onload = () => {
        data = JSON.parse(xhr.responseText);
        search = document.getElementById("cityList");
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
    const ix = city.indexOf("(")
    const lat = city.substring(ix + 1, city.length - 1).split(",")[0]
    const lng = city.substring(ix + 1, city.length - 1).split(",")[1]
    const report = document.getElementById("report1").value;
    window.location = `/generate_report?lat=${lat}&lng=${lng}&report=${report}`;
}

window.onload = () => {
    document.getElementById("cityList").addEventListener("click", onItemClick)
    document.getElementById("main-button").addEventListener("click", getReport)
 }

