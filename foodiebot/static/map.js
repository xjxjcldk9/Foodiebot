let map, infoWindow;
let marker;
let geocoder;
let cityCircle;

let editable = true;


function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        //center: { lat: 25.04625, lng: 121.51753 }
        center: myLocation,
        zoom: 15,
        disableDefaultUI: true,
    });
    infoWindow = new google.maps.InfoWindow();

    const locationButton = document.createElement("button");
    locationButton.textContent = "目前位置";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(locationButton);
    locationButton.addEventListener("click", () => {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };

                    map.setCenter(pos);
                    cityCircle.setCenter(pos);

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




    const clearButton = document.createElement("input");

    clearButton.type = "button";
    clearButton.value = "清除地點";
    clearButton.classList.add("button", "button-secondary");



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
        radius: radius,
    });


    cityCircle.addListener("radius_changed", () => {
        radius = cityCircle.getRadius();
    });


    cityCircle.addListener("center_changed", () => {
        marker.setPosition(cityCircle.getCenter());
    });


    map.addListener("click", (e) => {
        cityCircle.setCenter(e.latLng);
    });


    marker.addListener("position_changed", () => {
        myLocation = marker.getPosition();
    });



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
            ? "錯誤：無法取得地點，請檢查瀏覽器設定"
            : "Error: Your browser doesn't support geolocation.",
    );
    infoWindow.open(map);
}


function clear() {
    marker.setPosition(null);
}


window.initMap = initMap;





