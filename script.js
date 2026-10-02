const API_URL = "http://127.0.0.1:5000";


// ---------------------------------------------------------
// MAP
// ---------------------------------------------------------

const map = L.map("map").setView(
    [17.4065, 78.4772],
    14
);


L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution: "&copy; OpenStreetMap contributors"
    }
).addTo(map);


let locations = {};

let routeLine = null;

let markers = [];


// ---------------------------------------------------------
// LOAD LOCATIONS
// ---------------------------------------------------------

async function loadLocations() {

    try {

        const response =
            await fetch(`${API_URL}/api/locations`);

        locations =
            await response.json();

        addMarkers();

    }

    catch (error) {

        console.error(
            "Could not load locations:",
            error
        );

    }

}


// ---------------------------------------------------------
// ADD MARKERS
// ---------------------------------------------------------

function addMarkers() {

    for (const name in locations) {

        const location = locations[name];

        const marker = L.marker([
            location.lat,
            location.lon
        ])
        .addTo(map)
        .bindPopup(`<b>${name}</b>`);

        markers.push(marker);
    }

}


// ---------------------------------------------------------
// FIND ROUTE
// ---------------------------------------------------------

async function findRoute() {

    const start =
        document.getElementById("start").value;

    const goal =
        document.getElementById("destination").value;

    const algorithm =
        document.getElementById("algorithm").value;


    if (start === goal) {

        alert(
            "Start and destination cannot be the same."
        );

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/api/route`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    start: start,
                    goal: goal,
                    algorithm: algorithm
                })
            }
        );


        const data = await response.json();


        if (data.error) {

            alert(data.error);

            return;
        }


        displayResult(
            data,
            algorithm
        );


        drawRoute(data.path);

    }

    catch (error) {

        console.error(error);

        alert(
            "Backend server is not running."
        );

    }

}


// ---------------------------------------------------------
// DISPLAY RESULT
// ---------------------------------------------------------

function displayResult(
    data,
    algorithm
) {

    const result =
        document.getElementById("result");


    result.innerHTML = `

        <div class="result-card">

            <div class="route">

                🚑 Route:

                ${data.path.join(" → ")}

            </div>


            <div class="stats">

                <div class="stat">

                    <strong>
                        ${data.distance} km
                    </strong>

                    Distance

                </div>


                <div class="stat">

                    <strong>
                        ${data.time} min
                    </strong>

                    Travel Time

                </div>


                <div class="stat">

                    <strong>
                        ${data.nodes_explored}
                    </strong>

                    Nodes Explored

                </div>

            </div>


            <br>

            <b>Algorithm:</b>
            ${algorithm.toUpperCase()}

        </div>
    `;

}


// ---------------------------------------------------------
// DRAW ROUTE ON MAP
// ---------------------------------------------------------

function drawRoute(path) {

    if (routeLine) {

        map.removeLayer(routeLine);

    }


    const coordinates = [];


    path.forEach(
        name => {

            if (locations[name]) {

                coordinates.push([
                    locations[name].lat,
                    locations[name].lon
                ]);

            }

        }
    );


    routeLine = L.polyline(
        coordinates,
        {
            weight: 6
        }
    ).addTo(map);


    map.fitBounds(
        routeLine.getBounds(),
        {
            padding: [30, 30]
        }
    );

}


// ---------------------------------------------------------
// COMPARE ALGORITHMS
// ---------------------------------------------------------

async function compareAlgorithms() {

    const start =
        document.getElementById("start").value;

    const goal =
        document.getElementById("destination").value;


    if (start === goal) {

        alert(
            "Start and destination cannot be the same."
        );

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/api/compare`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    start: start,
                    goal: goal
                })
            }
        );


        const data =
            await response.json();


        displayComparison(data);

    }

    catch (error) {

        console.error(error);

        alert(
            "Backend server is not running."
        );

    }

}


// ---------------------------------------------------------
// DISPLAY COMPARISON
// ---------------------------------------------------------

function displayComparison(data) {

    const comparison =
        document.getElementById("comparison");


    let html = `

        <table>

            <tr>

                <th>Algorithm</th>

                <th>Distance</th>

                <th>Travel Time</th>

                <th>Nodes Explored</th>

            </tr>
    `;


    for (
        const algorithm in data
    ) {

        const result =
            data[algorithm];


        html += `

            <tr>

                <td>
                    <b>${algorithm}</b>
                </td>

                <td>
                    ${result.distance} km
                </td>

                <td>
                    ${result.time} min
                </td>

                <td>
                    ${result.nodes_explored}
                </td>

            </tr>
        `;

    }


    html += `</table>`;


    comparison.innerHTML = html;

}


// ---------------------------------------------------------
// START
// ---------------------------------------------------------

loadLocations();