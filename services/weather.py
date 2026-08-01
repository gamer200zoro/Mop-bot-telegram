"""Weather lookup service for Jarvis."""

from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(slots=True)
class WeatherReport:
    """A concise weather summary."""

    location: str
    temperature_c: float
    wind_speed_kph: float
    weather_code: int
    summary: str


_WEATHER_DESCRIPTIONS: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Rain showers",
    81: "Heavy rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}


class WeatherService:
    """Fetch weather details from Open-Meteo."""

    async def lookup(self, location: str) -> WeatherReport:
        """Resolve a location name and return current weather."""

        async with httpx.AsyncClient(timeout=20.0) as client:
            geocode_response = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": location, "count": 1, "language": "en", "format": "json"},
            )
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()
            results = geocode_data.get("results") or []
            if not results:
                raise ValueError(f"Location not found: {location}")

            best = results[0]
            latitude = best["latitude"]
            longitude = best["longitude"]
            display_name = ", ".join(
                part
                for part in [best.get("name"), best.get("admin1"), best.get("country")]
                if part
            )

            weather_response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current_weather": True,
                    "timezone": "auto",
                },
            )
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            current = weather_data.get("current_weather") or {}
            code = int(current.get("weathercode", 0))
            summary = _WEATHER_DESCRIPTIONS.get(code, "Weather data available")
            return WeatherReport(
                location=display_name,
                temperature_c=float(current.get("temperature", 0.0)),
                wind_speed_kph=float(current.get("windspeed", 0.0)),
                weather_code=code,
                summary=summary,
            )
