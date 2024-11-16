/* jshint esversion: 11, sub:true */

(g => {
    var h, a, p = "The Google Maps JavaScript API",
        c = "google", l = "importLibrary", q = "__ib__", m = document,
        b = window;
    b = b[c] || (b[c] = {});
    var d = b.maps || (b.maps = {});
    var r = new Set();
    var e = new URLSearchParams();
    var u = () => h || (
            h = new Promise(async (f, n) => {
                await (a = m.createElement("script"));
                e.set("libraries", [...r] + "");
                e.set("key", googleMapsApiKey);
                e.set("callback", c + ".maps." + q);
                a.src = `https://maps.${c}apis.com/maps/api/js?` + e;
                d[q] = f;
                a.onerror = () => h = n(Error(p + " could not load."));
                a.nonce = m.querySelector("script[nonce]")?.nonce || "";
                m.head.append(a);
            })
        );
    if (d[l]) {
        console.warn(p + " only loads once. Ignoring:", g);
    } else {
        d[l] = (f, ...n) => r.add(f) && u().then(() => d[l](f, ...n));
    }

})({
    v: "weekly",
});
