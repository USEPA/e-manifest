// Copy button toast notification
document.addEventListener('DOMContentLoaded', () => {
    // Initialize toast
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    const toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl)
    });

    // Add event listener to copy buttons
    const copyButtons = document.querySelectorAll('.btn-secondary');
    copyButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            toastList.forEach(function (toast) {
                toast.show();
            });
        });
    });
});

class ApiClient {

    static fetchSiteExists = (epaId) => {
        return async () => {
            return await this.#fetchData(`http://localhost:8080/api/site/${epaId}/exists`);
        }
    }

    static fetchSite = (epaId) => {
        return async () => {
            return await this.#fetchData(`http://localhost:8080/api/site/${epaId}`);
        }
    }
    static fetchLookup = (lookup) => {
        return async () => {
            return await this.#fetchData(`http://localhost:8080/api/lookup/${lookup}`);
        }
    }

    static #fetchData = async (url) => {
        const response = await fetch(url);
        if (response.status >= 400) {
            alert('Error fetching data');
            return;
        }
        return await response.json();
    }

    static #displayData = (elementId, data) => {
        document.getElementById(elementId).value = JSON.stringify(data, null, 2);
    }
}


function copyToClipboard(elementId) {
    const copyText = document.getElementById(elementId);
    navigator.clipboard.writeText(copyText.value);
}

function startCountdown(dateString) {
    const countDownDate = new Date(dateString).getTime();

    const countdownFunction = setInterval(function () {
        const now = new Date().getTime();
        const distance = countDownDate - now;
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById("countdown").innerText = minutes + "m " + seconds + "s ";

        if (distance < 0) {
            clearInterval(countdownFunction);
            document.getElementById("countdown").innerText = "EXPIRED"
        }
    }, 1000);
}
