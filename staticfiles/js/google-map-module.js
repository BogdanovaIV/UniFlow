let map;

async function initMap() {
    // The location of the Medical University
    const position = { lat: 43.259116, lng: 76.933178};
    // Request needed libraries from Google Maps API
    const { Map } = await google.maps.importLibrary("maps");

    // Create a new map centered at the specified location (Medical University)
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
}

// Check if we are running in a browser environment and auto-call `initMap`
if (typeof window !== 'undefined' && typeof document !== 'undefined') {
    window.onload = initMap;
}

module.exports = {
    initMap
};
