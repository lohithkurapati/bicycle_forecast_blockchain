document.addEventListener("DOMContentLoaded", function () {
    const forecastTable = document.getElementById("forecast-table");
    const forecastList = document.getElementById("forecast-list");
    const forecastForm = document.getElementById("forecast-form");
    const forecastPlotContainer = document.getElementById("forecast-plot");
    const forecastAccuracy = document.getElementById("forecast-accuracy");

    function validateForm() {
        const startSource = document.getElementById("start-source").value;
        const endSource = document.getElementById("end-source").value;
        const startForecast = document.getElementById("start-forecast").value;
        const endForecast = document.getElementById("end-forecast").value;

        if (!startSource || !endSource || !startForecast || !endForecast) {
            alert("All date fields must be filled out.");
            return false;
        }

        const startSourceDate = new Date(startSource);
        const endSourceDate = new Date(endSource);
        const startForecastDate = new Date(startForecast);
        const endForecastDate = new Date(endForecast);

        if (endSourceDate > new Date()) {
            alert("End date for historical data cannot be in the future.");
            return false;
        }

        if (startSourceDate > endSourceDate) {
            alert("Start date for historical data must be before the end date.");
            return false;
        }

        if (startForecastDate !== endSourceDate) {
            alert("Start date for forecast must match the historical end date.");
            return false;
        }

        if (startForecastDate > endForecastDate) {
            alert("Start date for forecast must be before the end date.");
            return false;
        }

        if ((endSourceDate - startSourceDate) / (1000 * 60 * 60 * 24) > 180) {
            alert("Historical range must not exceed 6 months.");
            return false;
        }

        if ((endForecastDate - startForecastDate) / (1000 * 60 * 60 * 24) > 90) {
            alert("Forecast range must not exceed 3 months.");
            return false;
        }

        return true;
    }

    forecastForm.addEventListener("submit", function (e) {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        alert("Forecast submitted successfully.");
        forecastForm.reset();
    });

    forecastList.addEventListener("click", function (e) {
        if (e.target.tagName === "A") {
            e.preventDefault();
            const forecastId = e.target.getAttribute("data-forecast-id");
            loadForecastDetails(forecastId);
        }
    });

    function loadForecastDetails(forecastId) {
        alert(`Load details for forecast ID: ${forecastId}`);
        populateTable([]); // Replace with dynamic data in the future
        renderPlot("placeholder.png"); // Replace with dynamic plot rendering in the future
        forecastAccuracy.textContent = "Accuracy: --%";
    }

    function populateTable(data) {
        forecastTable.innerHTML = "";

        if (data.length === 0) {
            forecastTable.innerHTML = "<tr><td colspan='7'>No data available for this forecast.</td></tr>";
            return;
        }

        data.forEach(row => {
            const tableRow = document.createElement("tr");
            tableRow.className = row.is_forecasted ? "forecasted-row" : "historical-row";

            tableRow.innerHTML = `
                <td>${row.date || "N/A"}</td>
                <td>${row.product || "N/A"}</td>
                <td>${row.order_quantity || "N/A"}</td>
                <td>${row.unit_cost || "N/A"}</td>
                <td>${row.unit_price || "N/A"}</td>
                <td>${row.profit || "N/A"}</td>
                <td>${row.revenue || "N/A"}</td>
            `;

            forecastTable.appendChild(tableRow);
        });
    }

    function renderPlot(plotPath) {
        forecastPlotContainer.innerHTML = "";

        if (!plotPath) {
            forecastPlotContainer.innerHTML = "<p>No plot available for this forecast.</p>";
            return;
        }

        const plotImage = document.createElement("img");
        plotImage.src = `/static/forecast_plots/${plotPath}`; // Adjust path if necessary
        plotImage.alt = "Forecast Plot";
        plotImage.style.width = "100%";
        forecastPlotContainer.appendChild(plotImage);
    }
});
