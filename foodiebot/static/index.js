let map, infoWindow;
let marker;
let geocoder;
let responseDiv;
let response;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 25.04625, lng: 121.51753 },
        zoom: 17,
    });
    infoWindow = new google.maps.InfoWindow();

    const locationButton = document.createElement("button");

    locationButton.textContent = "裝置目前位置";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.RIGHT_TOP].push(locationButton);
    locationButton.addEventListener("click", () => {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    /*
                    infoWindow.setPosition(pos);
                    infoWindow.setContent("你在這裡");
                    infoWindow.open(map);
                    map.setCenter(pos);
                    */

                    geocode({ location: pos });
                    map.setCenter(pos);
                },
                () => {
                    handleLocationError(true, infoWindow, map.getCenter());
                },
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
        }
    });

    geocoder = new google.maps.Geocoder();

    const inputText = document.createElement("input");

    inputText.type = "text";
    inputText.placeholder = "搜尋地點";

    const submitButton = document.createElement("input");

    submitButton.type = "button";
    submitButton.value = "搜尋";
    submitButton.classList.add("button", "button-primary");

    const clearButton = document.createElement("input");

    clearButton.type = "button";
    clearButton.value = "清除地點";
    clearButton.classList.add("button", "button-secondary");
    response = document.createElement("pre");
    response.id = "response";
    response.innerText = "";

    responseDiv = document.createElement("div");
    responseDiv.id = "response-container";
    responseDiv.appendChild(response);

    const instructionsElement = document.createElement("p");

    /*
    instructionsElement.id = "instructions";
    instructionsElement.innerHTML =
        "<strong>Instructions</strong>: Enter an address in the textbox to geocode or click on the map to reverse geocode.";
        */
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(inputText);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(submitButton);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(clearButton);
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(instructionsElement);


    //map.controls[google.maps.ControlPosition.LEFT_TOP].push(responseDiv);
    marker = new google.maps.Marker({
        map,
    });
    map.addListener("click", (e) => {
        geocode({ location: e.latLng });
    });
    submitButton.addEventListener("click", () =>
        geocode({ address: inputText.value }),
    );
    clearButton.addEventListener("click", () => {
        clear();
    });
    clear();

}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation.",
    );
    infoWindow.open(map);
}


function clear() {
    marker.setMap(null);
    responseDiv.style.display = "none";
}

function geocode(request) {
    clear();
    geocoder
        .geocode(request)
        .then((result) => {
            const { results } = result;

            //map.setCenter(results[0].geometry.location);

            //經緯度資訊在此
            marker.setPosition(results[0].geometry.location);
            marker.setMap(map);
            responseDiv.style.display = "block";
            response.innerText = JSON.stringify(result, null, 2);
            myLocation = JSON.stringify(results[0].geometry.location);
            return results;
        })
        .catch((e) => {
            alert("Geocode was not successful for the following reason: " + e);
        });
}

window.initMap = initMap;