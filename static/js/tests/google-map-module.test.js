/**
 * @jest-environment jsdom
 */

const { initMap } = require('../google-map-module');

beforeAll(() => {
    document.body.innerHTML = '<div id="map"></div>';

    // Mock google object and google.maps
    global.google = {
        maps: {
            Map: jest.fn(function (element, options) {
                // Mock Map constructor behavior
                // Store the map element for reference
                this.element = element;
                // Store the map options (zoom, center, etc.)
                this.options = options;
            }),
            Marker: jest.fn(function (options) {
                // Mock Marker constructor behavior
                // Store marker position
                this.position = options.position;
                // Store map reference
                this.map = options.map;
                // Store marker title
                this.title = options.title;
            }),
            importLibrary: jest.fn(async (library) => {
                if (library === "maps") {
                    return {
                        // return the mocked Map constructor
                        Map: global.google.maps.Map
                    };
                }
            }),
        },
    };
});

describe('Google Map', () => {
    test('should initialize Google Map', async () => {
        // Await the async initMap function
        await initMap();

        // Check if Map and Marker constructors were called
        expect(global.google.maps.Map).toHaveBeenCalled();
        expect(global.google.maps.Marker).toHaveBeenCalled();
    });
});