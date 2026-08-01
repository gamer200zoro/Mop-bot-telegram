"""Currency conversion service for Jarvis."""

from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(slots=True)
class CurrencyQuote:
    """A currency conversion result."""

    from_currency: str
    to_currency: str
    amount: float
    converted_amount: float
    rate: float


class CurrencyService:
    """Fetch live exchange rates from frankfurter.app."""

    async def convert(self, amount: float, from_currency: str, to_currency: str) -> CurrencyQuote:
        """Convert an amount between two currencies."""

        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                "https://api.frankfurter.app/latest",
                params={"amount": amount, "from": from_currency, "to": to_currency},
            )
            response.raise_for_status()
            data = response.json()

        rates = data.get("rates") or {}
        converted = float(rates.get(to_currency, 0.0))
        rate = converted / amount if amount else 0.0
        return CurrencyQuote(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            converted_amount=converted,
            rate=rate,
        )
