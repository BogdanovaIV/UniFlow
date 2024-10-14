let map;

async function initMap() {
    // The location of Uluru
    const position = { lat: 43.259116, lng: 76.933178};
    // Request needed libraries.
    //@ts-ignore
    const { Map } = await google.maps.importLibrary("maps");
    
    // The map, centered at Uluru
    map = new Map(document.getElementById("map"), {
        zoom: 12,
        center: position,
        mapId: "MAP_ID",
    });
    // Create marker
    var marker = new google.maps.Marker({
            position: { lat: 43.25911614460168, lng: 76.9331789342499 },
            map: map,
            title: "Medical University"
    });

    locations.map(marker);
}

initMap();