const genreInput = document.querySelector('.input-box:nth-of-type(1)');
const dateInput = document.querySelector('.input-box:nth-of-type(2)');
const priceInput = document.querySelector('.input-box:nth-of-type(3)');
const distanceInput = document.querySelector('.input-box:nth-of-type(4)');
const form = document.querySelector('.form');
const submitButton = document.querySelector('.submit-button');

//Function to retrieve the ZIP-CODE of the USER
const findMyState = () => {
    const status = document.querySelector('.status');

    const success = (position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const geoApiURL = `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`

        fetch(geoApiURL)
            .then(res => res.json())
            .then(data => {
                const location = data;
                const postData = {
                    latitude: location.latitude,
                    longitude: location.longitude
                };

                fetch('/api/location', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(postData)
                    })
                    .then(res => res.json())
                    .then(data => {
                        const latitudeSpan = document.querySelector('#latitude');
                        const longitudeSpan = document.querySelector('#longitude');
                        latitudeSpan.textContent = `Latitude: ${latitude}`;
                        longitudeSpan.textContent = `Longitude: ${longitude}`;
                    });
            });
    }

    const error = () => {
        status.textContent = "Unable";
    }

    navigator.geolocation.getCurrentPosition(success, error);
}

document.querySelector(".location-button").addEventListener("click", findMyState);