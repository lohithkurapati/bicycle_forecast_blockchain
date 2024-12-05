// forecast_app/blockchain/bike_forecast.sol
pragma solidity ^0.8.0;

contract BikeForecast {
    struct Forecast {
        uint id;
        string forecastData;
        uint timestamp;
    }

    Forecast[] public forecasts;
    mapping(uint => uint) public forecastIndex;  // Mapping for lookup by id

    event ForecastStored(uint id, string forecastData, uint timestamp);

    function storeForecast(uint id, string memory data) public {
        uint timestamp = block.timestamp;
        forecasts.push(Forecast(id, data, timestamp));
        forecastIndex[id] = forecasts.length - 1;
        emit ForecastStored(id, data, timestamp);
    }

    function getForecast(uint id) public view returns (string memory, uint) {
        uint index = forecastIndex[id];
        Forecast memory forecast = forecasts[index];
        return (forecast.forecastData, forecast.timestamp);
    }
}
