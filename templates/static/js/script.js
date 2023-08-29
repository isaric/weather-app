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
            li.textContent = city
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

window.onload = () => {
    document.getElementById("cityList").addEventListener("click", onItemClick)
 }

