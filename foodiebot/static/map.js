let map, infoWindow;
let marker;
let geocoder;
let responseDiv;
let response;
let cityCircle;

let editable = false;

if (login) {
    editable = true;
}


function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 25.04625, lng: 121.51753 },
        zoom: 15,
    });
    infoWindow = new google.maps.InfoWindow();

    const locationButton = document.createElement("button");

    locationButton.textContent = "目前位置";
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




    map.controls[google.maps.ControlPosition.TOP_LEFT].push(inputText);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(submitButton);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(clearButton);



    marker = new google.maps.Marker({
        map,
    });

    cityCircle = new google.maps.Circle({
        strokeColor: "#FF0000",
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: "#FF0000",
        fillOpacity: 0.35,
        map: map,
        editable: editable,
        draggable: true,
        radius: 500,
    });


    cityCircle.addListener("radius_changed", () => {
        radius = cityCircle.getRadius();
    });


    cityCircle.addListener("center_changed", () => {
        marker.setPosition(cityCircle.getCenter());
    });


    map.addListener("click", (e) => {
        geocode({ location: e.latLng });
        cityCircle.setCenter(e.latLng);
    });


    marker.addListener("position_changed", () => {
        myLocation = marker.getPosition();
    });


    submitButton.addEventListener("click", () => {
        geocode({ address: inputText.value });
    }
    );
    clearButton.addEventListener("click", () => {
        clear();
        cityCircle.setCenter(null);
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
    marker.setPosition(null);
}

function geocode(request) {
    clear();
    geocoder
        .geocode(request)
        .then((result) => {
            const { results } = result;
            const position = results[0].geometry.location;
            map.setCenter(position);
            cityCircle.setCenter(position);
        })
        .catch((e) => {
            alert("Geocode was not successful for the following reason: " + e);
        });
}

window.initMap = initMap;





