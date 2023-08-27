function citySearch() {
    text = document.getElementById("city").value
    if (text.length < 3) {
        return;
    }
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/autocomplete?name=" + text, true);

    xhr.onload = () => {
        data = JSON.parse(xhr.responseText);
        search = document.getElementById("cityList");
        search.innerHTML = "";
        for (city of data) {
            const opt = document.createElement("option");
            opt.value = city;
            search.appendChild(opt);
        }
        
    };
    xhr.send(null);
}
