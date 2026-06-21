import httpx

def get_location_context(latitude: float, longitude: float) -> str:
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain"],
            "timezone": "Asia/Kolkata",
            "forecast_days": 1,
        }
        resp = httpx.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        current = data.get("current", {})
        temp = current.get("temperature_2m", "unknown")
        humidity = current.get("relative_humidity_2m", "unknown")
        rain = current.get("rain", "unknown")

        return (
            f"Farmer location context: "
            f"Temperature: {temp}°C, "
            f"Humidity: {humidity}%, "
            f"Recent rainfall: {rain}mm. "
            f"Use this to refine your diagnosis — for example, high humidity increases fungal disease risk."
        )
    except Exception:
        return ""
